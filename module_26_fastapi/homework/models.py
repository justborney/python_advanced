from sqlalchemy import Column, String, Integer, Text, Time

from database import Base


class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cooking_time = Column(String, index=True, nullable=False)
    # cooking_time = Column(Time, index=True, nullable=False)
    ingredients = Column(String, index=True, nullable=False)
    description = Column(Text(), index=True)
    view_count = Column(Integer, index=True)
