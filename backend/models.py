from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    tasks= relationship("Task",back_populates="owner")

class Task(Base):
    __tablename__ ="tasks"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    completed = Column(Boolean,default=False)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    owner= relationship("User",back_populates="tasks")


