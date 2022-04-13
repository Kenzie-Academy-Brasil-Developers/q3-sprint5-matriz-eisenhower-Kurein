from sqlalchemy import TEXT, VARCHAR, Column, Integer
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class Category(db.Model):

    category_id: int
    name: str
    description: str

    __tablename__= "categories"

    category_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    description = Column(TEXT)