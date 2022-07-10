import factory
import factory.fuzzy as fuzzy
import random

from ..app import db
from ..models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = fuzzy.FuzzyChoice(['fake_credit_card', None])
    car_number = fuzzy.FuzzyText(length=10)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = fuzzy.FuzzyText(length=100)
    opened = fuzzy.FuzzyChoice([True, False])
    count_places = fuzzy.FuzzyInteger(200)
    count_available_places = factory.LazyAttribute(lambda x: random.randrange(0, 100))
