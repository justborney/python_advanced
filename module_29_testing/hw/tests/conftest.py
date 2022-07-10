from datetime import datetime

import pytest
from ..app import create_app, db as _db
from ..models import Client, Parking, ClientParking


@pytest.fixture
def app():
    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with test_app.app_context():
        _db.create_all()
        client = Client(id=1,
                        name="Ivan",
                        surname="Ivanov",
                        credit_card="1234567890123456",
                        car_number="A111AA178"
                        )
        parking = Parking(id=1,
                          address="Saint-Petersburg, Palace Square, 1",
                          opened=True,
                          count_places=100,
                          count_available_places=50
                          )
        client_parking = ClientParking(id=1,
                                       client_id=1,
                                       parking_id=1,
                                       time_in=datetime.fromisoformat('2021-07-01T10:05:20'),
                                       time_out=datetime.fromisoformat('2021-07-01T14:03:15')
                                       )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()
        yield test_app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
