from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import models
from ..security import verify_password, create_access_token

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.username==user_data.username).first()

    if user is None:
        raise HTTPException(status_code = 401,detail="Invalid username or password")

    if not verify_password(user_data.password,user.password):
        raise HTTPException(status_code = 401,detail="Invalid username or password")

    data={"sub":str(user.id)}

    token=create_access_token(data)

    return {"access_token": token,"token_type": "bearer" }

