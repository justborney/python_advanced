import requests
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Boolean, JSON, ARRAY
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import time
import random
from flask import Flask
import logging
from typing import Tuple, Dict, Any

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://admin:admin@localhost')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# app.config['DEBUG'] = True


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
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    relationship('Coffee', backref='users')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


# @app.before_request
# def before_request_func():
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#     # res = requests.get('https://random-data-api.com/api/coffee/random_coffee?size=10')
#     session.commit()


@app.route('/all')
def get_all():
    products = session.query(Coffee).all()
    products_list = []
    for p in products:
        product_obj = p.to_json()
        product_obj['user'] = p.user.to_json()
        products_list.append(product_obj)
    return products_list


@app.route('/one')
def the_first() -> Tuple[str, int]:
    logging.info('one')
    time.sleep(random.random() * 0.2)
    return 'ok', 201


@app.route('/two')
def the_second() -> Tuple[str, int]:
    logging.info('two')
    time.sleep(random.random() * 0.4)
    return 'ok', 202


@app.route('/three')
def the_third() -> Tuple[str, int]:
    logging.info('three')
    time.sleep(random.random() * 0.6)
    return 'ok', 203


@app.route('/four')
def the_fourth() -> Tuple[str, int]:
    logging.info('four')
    time.sleep(random.random() * 0.8)
    return 'ok', 204


@app.route('/five')
def the_fiveth() -> Tuple[str, int]:
    logging.info('five')
    time.sleep(random.random())
    return 'ok', 205


@app.route('/error')
def error() -> Tuple[str, int]:
    logging.info('error')
    a = 1 / 0
    return 'error', 500


if __name__ == "__main__":
    app.run()
