from sqlalchemy import VARCHAR, Column, Integer
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Eisenhower(db.Model):

    category_id: int
    type: str

    __tablename__= "eisenhowers"

    eisenhower_id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(100), nullable=False, unique=True)