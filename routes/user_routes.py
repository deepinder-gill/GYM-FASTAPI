from fastapi import APIRouter, HTTPException
from app.Schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password

router = APIRouter()

fake_user_db = []

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):

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

@router.post("/login")
def login(user: UserCreate):
    for existing_user in fake_user_db:
        if existing_user['email'] == user.email:

            if verify_password(user.password, existing_user['hash_password']):
                return {"message" : "Login Successful"}

            break

    raise HTTPException(status_code=400, detail="Invalid Credentials")