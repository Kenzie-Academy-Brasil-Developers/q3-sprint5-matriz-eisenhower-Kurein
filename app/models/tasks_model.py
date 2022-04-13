from sqlalchemy import TEXT, VARCHAR, Column, ForeignKey, Integer
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Task(db.Model):

    category_id: int
    name: str
    description: str

    __tablename__= "tasks"

    task_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    description = Column(TEXT)
    importance = Column(Integer)
    urgency = Column(Integer)

    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.eisenhower_id"), nullable=False)