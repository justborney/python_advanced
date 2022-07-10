import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///prod.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=['GET'])
    def get_all_clients():
        clients = db.session.query(Client).all()
        clients_list = [client.to_json() for client in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_client_by_id(client_id: int):
        client = db.session.query(Client).get(client_id)
        return jsonify(client), 200

    @app.route("/clients", methods=['POST'])
    def add_new_client():
        credit_card = ''
        car_number = ''
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        if request.form.get('credit_card', type=str):
            credit_card = request.form.get('credit_card', type=str)
        if request.form.get('car_number', type=str):
            car_number = request.form.get('car_number', type=str)
        new_client = Client(name=name,
                            surname=surname,
                            credit_card=credit_card,
                            car_number=car_number)
        db.session.add(new_client)
        db.session.commit()
        return '', 201

    @app.route("/parkings", methods=['POST'])
    def add_new_parking():
        opened = False
        address = request.form.get('address', type=str)
        count_places = request.form.get('count_places', type=int)
        if request.form.get('opened', type=bool):
            opened = request.form.get('opened', type=bool)
        new_parking = Parking(address=address,
                              opened=opened,
                              count_places=count_places,
                              count_available_places=count_places)
        db.session.add(new_parking)
        db.session.commit()
        return '', 201

    @app.route("/client_parkings", methods=['POST'])
    def add_new_parking_client():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        parking = db.session.query(Parking).get(parking_id)
        if parking.to_json()['opened']:
            if parking.to_json()['count_available_places'] > 0:
                parking.count_available_places -= 1
                new_parking_client = ClientParking(client_id=client_id,
                                                   parking_id=parking_id,
                                                   time_in=datetime.datetime.now())
                db.session.add(new_parking_client)
                db.session.commit()
                return jsonify('', 200)
            return jsonify('No one parking place is available'), 202
        return jsonify('Parking is closed'), 202

    @app.route("/client_parkings", methods=['DELETE'])
    def delete_parking_client():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        parking = db.session.query(Parking).get(parking_id)
        if db.session.query(Client).get(client_id).to_json()['credit_card']:
            parking_client = db.session.query(ClientParking). \
                filter((ClientParking.client_id == client_id) and (ClientParking.parking_id == parking_id)). \
                order_by(desc(ClientParking.time_in)).first()
            time_out = datetime.datetime.now()
            parking_client.time_out = time_out
            make_payment(client_id, parking_id)
            parking.count_available_places += 1
            db.session.commit()
            return jsonify('', 200)
        return 'No credit card added', 202

    def make_payment(client_id, parking_id):
        pass

    return app
