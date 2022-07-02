import random
from typing import Dict, Any

import requests
from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, JSON, ARRAY, insert, func, cast
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://admin:admin@postgres')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
app.config['DEBUG'] = True


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String))

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    user = relationship('Coffee', backref='users')
    patronymic = Column(String(50))

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


@app.before_first_request
def before_first_request_func():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    coffee_data = requests.get('https://random-data-api.com/api/coffee/random_coffee?size=10').json()
    all_coffee = []
    for coffee in coffee_data:
        all_coffee.append(
            Coffee(title=coffee['blend_name'],
                   origin=coffee['origin'],
                   notes=coffee['notes'],
                   intensifier=coffee['intensifier']))
    session.bulk_save_objects(all_coffee)
    user_address = requests.get('https://random-data-api.com/api/address/random_address?size=10').json()
    all_users = []
    for user in user_address:
        all_users.append(
            User(
                name=requests.get('https://random-data-api.com/api/name/random_name').json()['name'],
                address={'city': user['city'],
                         'street_name': user['street_name'],
                         'building_number': user['building_number'],
                         'secondary_address': user['secondary_address'],
                         'country': user['country']},
                coffee_id=random.randint(1, 10)
            ))
    session.bulk_save_objects(all_users)
    session.commit()


@app.route('/add_user/<name>', methods=['POST'])
def add_user(name: str):
    user_data = request.json
    try:
        if user_data['address']['city'] \
                and user_data['address']['street_name'] \
                and user_data['address']['building_number'] \
                and user_data['address']['secondary_address'] \
                and user_data['address']['country']:
            session.execute(insert(User).values(name=name,
                                                address=user_data['address'],
                                                coffee_id=user_data['coffee_id']))
            session.commit()
            return jsonify({'new_user_name': name,
                            'new_user_address': user_data['address'],
                            'new_user_coffee': user_data['coffee_id']}), 200
    except KeyError:
        return 'Wrong input data', 500


@app.route('/looking_coffee/<coffee_name>')
def find_coffee_by_name(coffee_name: str):
    all_coffee = session.query(Coffee).filter(
        func.to_tsvector(Coffee.title).match(cast(func.plainto_tsquery(coffee_name), String))).all()
    coffee_list = []
    for coffee in all_coffee:
        json_coffee = coffee.to_json()
        json_coffee['notes'] = ''.join(coffee.notes)
        coffee_list.append(json_coffee)
    return jsonify(coffee_list=coffee_list), 200


@app.route('/notes')
def find_unique_coffee_note():
    all_notes = session.query(Coffee.notes).all()
    notes_list = set()
    for note_string in all_notes:
        note_record = ''
        for symbol in note_string:
            note_record = ''.join(symbol)
        for note in note_record.split(', '):
            notes_list.add(note)
    return jsonify(notes_list=list(notes_list)), 200


@app.route('/looking_users/<users_country>')
def find_users_by_country(users_country: str):
    all_users = session.query(User).filter(User.address['country'].as_string() == users_country).all()
    user_list = []
    for user in all_users:
        json_user = user.to_json()
        user_list.append(json_user)
    return jsonify(user_list=user_list), 200


if __name__ == "__main__":
    app.run()
