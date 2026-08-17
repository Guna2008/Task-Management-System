from fastapi import FastAPI
from .database import engine,Base
from . import models
from .routers import tasks,users,auth

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Task Management API is running"}
    
