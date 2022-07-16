from sqlalchemy import Column, Integer, String, Text

from ..src.database import declarative_base

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "Recipe"
    Base.metadata.clear()
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cooking_time = Column(String, index=True, nullable=False)
    ingredients = Column(String, index=True, nullable=False)
    description = Column(Text(), index=True)
    view_count = Column(Integer, index=True)
