from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str 

    model_config=ConfigDict(from_attributes=True)   

class UserLogin(BaseModel):
    username:str
    password:str    

class Task(BaseModel): 
    title: str
    completed: bool

class TaskResponse(BaseModel):
    id:int
    title:str
    completed:bool

    model_config=ConfigDict(from_attribute=True)    