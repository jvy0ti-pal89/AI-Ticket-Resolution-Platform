from pydantic import BaseModel, EmailStr, constr


class Login(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str
