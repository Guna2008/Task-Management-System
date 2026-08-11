from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import get_db
from . import models
from .security import oauth2_scheme, SECRET_KEY, ALGORITHM


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate credentials")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401,detail="Could not validate credentials")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()

    if user is None:
        raise HTTPException( status_code=401,detail="Could not validate credentials")

    return user