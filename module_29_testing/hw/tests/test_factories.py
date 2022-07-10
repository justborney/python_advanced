from .factories import ClientFactory, ParkingFactory
from ..models import Client, Parking


def test_factories_create_client(app, db):
    client = ClientFactory()
    db.session.commit()
    assert client.id is not None
    assert client.name is not None
    assert client.surname is not None
    assert len(db.session.query(Client).all()) == 2


def test_factories_create_parking(app, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert parking.address is not None
    assert parking.count_places is not None
    assert parking.count_available_places is not None
    assert len(db.session.query(Parking).all()) == 2
