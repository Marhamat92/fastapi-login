from pydantic import BaseModel


class UserSchema(BaseModel):
    content: dict = {
        "name_surname": "",
        "email": "",
        "password": ""
    }
