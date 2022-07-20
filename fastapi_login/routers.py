from datetime import datetime, timedelta

from cryptography.fernet import Fernet

import jwt
from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from base_engine import SessionLocal, SECRET_KEY, FERNET_KEY_PASS, ACCESS_TOKEN_EXPIRE_MINUTES

from functions import check_token
from models import mUser
from schemas import UserSchema

router = APIRouter()


@router.post("/register", summary="User Register")
def user_register(user_data: UserSchema):
    db = SessionLocal()
    encrypt_password = Fernet(FERNET_KEY_PASS).encrypt(str(user_data.content["password"]).encode()).decode()

    content = {
        "name_surname": user_data.content["name_surname"],
        "email": user_data.content["email"],
        "password": encrypt_password
    }

    db.add(mUser(content=content))
    db.commit()
    db.close()
    return {'status': 'created'}


@router.post("/login", summary="User Login")
def user_login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    get_user = db.query(mUser).filter(mUser.content["email"].astext == form.username).first()

    if not get_user:
        db.close()
        return JSONResponse(status_code=400, content={'status': 'user_not_found'})

    decrypt_password = Fernet(FERNET_KEY_PASS).decrypt(str(get_user.content["password"]).encode()).decode()
    if form.password != decrypt_password:
        db.close()
        return JSONResponse(status_code=400, content={'status': 'password_does_not_match'})

    time_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
    expire = datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"time": time_now, "exp": expire, "expire": str(expire), "email": form.username}

    access_token = jwt.encode(to_encode, SECRET_KEY)

    db.close()
    return {"access_token": access_token, "user_id": get_user.id, "user_name": get_user.content["name_surname"]}


@router.get("/list/users", summary="List Users")
def user_list(get_user: UserSchema = Depends(check_token)):
    ###################################################################
    get_user_info, db = get_user
    if not get_user_info:
        db.close()
        return JSONResponse(status_code=401, content={'status': False, 'message': 'staff_not_found'})
    ###################################################################

    customers = db.execute(f"select * from users order by id desc ;").fetchall()
    if not customers:
        db.close()
        return {'status': 'customer_not_found'}
    db.close()
    return customers
