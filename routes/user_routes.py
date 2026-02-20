from fastapi import APIRouter, HTTPException, Depends, Request
from app.Schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, RefreshToken
from app.core.dependencies import get_current_user
from jose import jwt, JWTError

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
    db_user = db.query(User).filter(User.email == user.email).first()


    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": db_user.email})

    db_refresh = RefreshToken(
        token = access_token,
        user_id = user.id
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        stored_token = db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first
        if not stored_token:
            raise HTTPException(status_code=400, detail="Invalid Refresh Token")

        new_access_token = create_access_token(data={"sub": email})


        return {"access_token": new_access_token }

    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid Refreshing Token")

@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return {"message": "You have been logged out"}
