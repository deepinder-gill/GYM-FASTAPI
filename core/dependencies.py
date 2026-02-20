from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="INVALID TOKEN")
    except JWTError:
        raise HTTPException(status_code=400, detail="INVALID TOKEN")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=400, detail="user not found")

    return user

 