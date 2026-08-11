from pydantic import BaseModel

class UserCreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str    

class Task(BaseModel): 
    title: str
    completed: bool