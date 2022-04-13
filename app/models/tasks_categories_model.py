from sqlalchemy import Column, Integer, ForeignKey
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Task_Category(db.Model):

    task_category_id: int
    task_id: int
    category_id: int

    __tablename__= "task_category"

    task_category_id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)