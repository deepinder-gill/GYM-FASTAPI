from fastapi import APIRouter, HTTPException, Depends
from app.Schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = User(
        email = user.email,
        hashed_password = hashed_pw
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()


    if not existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    return {"message": "Login Successful"}