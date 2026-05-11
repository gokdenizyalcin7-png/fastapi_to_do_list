from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import DeclarativeBase
from database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
   
    tasks = relationship("Task", back_populates="owner")



class Task(Base):
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)             
    description = Column(String, nullable=True)      
    is_completed = Column(Boolean, default=False)    
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="tasks")