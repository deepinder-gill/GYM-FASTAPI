from fastapi import APIRouter, HTTPException
from app.models.user import usercreate, userout
from app.core.security import hash_password

router = APIRouter()

fake_user_db = []

@router.post("/register", response_model=userout)
def register(user: usercreate):

    for existing_user in fake_user_db:
        if existing_user['email'] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = {
        "email": user.email,
        "hash_password": hashed_pw
    }

    fake_user_db.append(new_user)

    return {"email": user.email}