from fastapi.testclient import TestClient

from ..src import models
from ..src.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./hw_app.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()
Base = declarative_base()


def test_bd_connection():
    with TestClient(app) as client:
        response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


def test_getting_all_recipes_sorted_by_popularity():
    session.add_all(
        [
            models.Recipe(
                title="dish_1",
                cooking_time="25.5",
                ingredients="a, b, c",
                description="text_1",
                view_count=2,
            ),
            models.Recipe(
                title="dish_2",
                cooking_time="50",
                ingredients="d, e, f",
                description="text_2",
                view_count=5,
            ),
            models.Recipe(
                title="dish_3",
                cooking_time="25",
                ingredients="g, h, i",
                description="text_3",
                view_count=5,
            ),
        ]
    )
    session.commit()
    with TestClient(app) as client:
        response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == [
        {"cooking_time": "00:00:25", "title": "dish_3", "view_count": 5},
        {"cooking_time": "00:00:50", "title": "dish_2", "view_count": 5},
        {"cooking_time": "00:00:25.500000", "title": "dish_1", "view_count": 2},
    ]


def test_getting_recipe_with_id_2():
    with TestClient(app) as client:
        response = client.get("/2")
    assert response.status_code == 200
    assert response.json() == {
        "cooking_time": "00:00:50",
        "description": "text_2",
        "ingredients": "d, e, f",
        "title": "dish_2",
    }
    session.query(models.Recipe).delete()
    session.commit()
