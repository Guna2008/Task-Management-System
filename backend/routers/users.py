from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..schemas import UserCreate
from ..security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
def create_user(user:UserCreate, db:Session = Depends(get_db)):

    hashed_password= hash_password(user.password)

    new_user=models.User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user