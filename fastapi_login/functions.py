from datetime import datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from base_engine import SessionLocal, SECRET_KEY
from models import mUser


def check_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"/login"))):
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_signature": False})
        email = payload.get("email")
        expire = datetime.strptime(payload.get("expire"), "%Y-%m-%d %H:%M:%S.%f")
        get_user = db.query(mUser).filter(mUser.content["email"].astext == email).first()

        if not get_user or expire < datetime.now():
            return False, db

        return get_user, db
    except:
        return False, db
