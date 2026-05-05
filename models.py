from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from database import Base




class Task(Base):
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)             
    description = Column(String, nullable=True)      
    is_completed = Column(Boolean, default=False)    