from pydantic import BaseModel, EmailStr

class usercreate(BaseModel):
    email: EmailStr
    password: str

class userout(BaseModel):
    email: EmailStr