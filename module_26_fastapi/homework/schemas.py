from datetime import time
from typing import Text

from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str
    cooking_time: time


class AllRecipes(BaseRecipe):
    view_count: int

    class Config:
        orm_mode = True


class RecipeDetail(BaseRecipe):
    ingredients: str
    description: Text

    class Config:
        orm_mode = True
