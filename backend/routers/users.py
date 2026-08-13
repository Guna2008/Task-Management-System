from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..schemas import UserCreate,UserResponse
from ..security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Username already exists")
    
    hashed_password= hash_password(user.password)

    new_user=models.User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user