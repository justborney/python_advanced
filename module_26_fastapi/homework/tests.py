from fastapi.testclient import TestClient
from main import app
import models
from database import session

client = TestClient(app)


def test_bd_connection():
    response = client.get('/recipes')
    assert response.status_code == 200
    assert response.json() == []


def test_getting_all_recipes_sorted_by_popularity():
    session.add_all([
        models.Recipe(title="dish_1", cooking_time="25.5",
                      ingredients="a, b, c", description="text_1",
                      view_count=2),
        models.Recipe(title="dish_2", cooking_time="50",
                      ingredients="d, e, f", description="text_2",
                      view_count=5),
        models.Recipe(title="dish_3", cooking_time="25",
                      ingredients="g, h, i", description="text_3",
                      view_count=5)
    ])
    session.commit()
    response = client.get('/recipes')
    assert response.status_code == 200
    assert response.json() == [{'cooking_time': '00:00:25',
                                'title': 'dish_3', 'view_count': 5},
                               {'cooking_time': '00:00:50',
                                'title': 'dish_2', 'view_count': 5},
                               {'cooking_time': '00:00:25.500000',
                                'title': 'dish_1', 'view_count': 2}]


def test_getting_recipe_with_id_2():
    response = client.get('/2')
    assert response.status_code == 200
    assert response.json() == {'cooking_time': '00:00:50',
                               'description': 'text_2',
                               'ingredients': 'd, e, f',
                               'title': 'dish_2'}
