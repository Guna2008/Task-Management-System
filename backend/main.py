from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models
from .schemas import Task,UserCreate
from .security import (hash_password,verify_password,create_access_token,oauth2_scheme,SECRET_KEY,ALGORITHM)
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()
Base.metadata.create_all(bind=engine)

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

@app.get("/")
def home():
    return{"message": "Task Management API is running"}
 
@app.get("/tasks")
def get_tasks(db:Session = Depends(get_db),current_user:models.User=Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.user_id==current_user.id).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db:Session = Depends(get_db),current_user:models.User=Depends(get_current_user)):

    task= db.query(models.Task).filter(models.Task.id == task_id,models.Task.user_id==current_user.id).first()

    if task is None:
       raise HTTPException(status_code=404,detail="Task not found")
    
    return task

@app.post("/tasks")
def create_tasks(task: Task,db:Session = Depends(get_db),current_user: models.User=Depends(get_current_user)):
    new_task = models.Task(
        title = task.title,
        completed= task.completed,
        user_id= current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id:int, task: Task, db: Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    existing_task= db.query(models.Task).filter(models.Task.id == task_id,models.Task.user_id==current_user.id).first()
    if existing_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    existing_task.title=task.title
    existing_task.completed=task.completed

    db.commit()
    db.refresh(existing_task)
    return existing_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,db: Session = Depends(get_db),current_user:models.User=Depends(get_current_user)):
    removing_task=db.query(models.Task).filter(models.Task.id == task_id,models.Task.user_id==current_user.id).first()

    if removing_task is None:            
         raise HTTPException(status_code=404, detail="task not found")   

    db.delete(removing_task)
    db.commit()
    return {"message":"successfully deleted the task"} 

@app.post("/users")
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

@app.post("/login")
def login(user_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.username==user_data.username).first()

    if user is None:
        raise HTTPException(status_code = 401,detail="Invalid username or password")

    if not verify_password(user_data.password,user.password):
        raise HTTPException(status_code = 401,detail="Invalid username or password")

    data={"sub":str(user.id)}

    token=create_access_token(data)

    return {"access_token": token,"token_type": "bearer" }

