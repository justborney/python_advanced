from typing import List

from fastapi import FastAPI, Path
from sqlalchemy import desc
from sqlalchemy.future import select

from ..src import models, schemas
from ..src.database import engine, session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()


@app.get("/recipes", response_model=List[schemas.AllRecipes])
async def all_recipes() -> List[models.Recipe]:
    res = await session.execute(
        select(models.Recipe).order_by(
            desc(models.Recipe.view_count), models.Recipe.cooking_time
        )
    )
    return res.scalars().all()


@app.get("/{recipe_id}", response_model=schemas.RecipeDetail)
async def recipe_detail(
    recipe_id: int = Path(title="Recipe id", ge=1)
) -> models.Recipe:
    res = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    return res.scalars().one()
