import pytest

from module_29_testing.hw.models import Parking, Client, ClientParking


@pytest.mark.parametrize("route", ["/clients", "/clients/0"])
def test_route_status(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client):
    client_data = {"name": "Pavel",
                   "surname": "Pavlov",
                   "credit_card": "test_client_credit_card",
                   "car_number": "B1234BB123"}
    response = client.post("/clients", data=client_data)
    assert response.status_code == 201


def test_create_parking(client):
    parking_data = {"address": "Saint-Petersburg, Nevsky Avenue, 10",
                    "opened": "True",
                    "count_places": "75",
                    "count_available_places": "50"}
    response = client.post("/parkings", data=parking_data)
    assert response.status_code == 201


@pytest.mark.parking
def test_create_parking_client(client, db):
    client_parking_data = {"client_id": "1",
                           "parking_id": "1"}
    assert db.session.query(Parking).get(client_parking_data["parking_id"]).to_json()["opened"]
    count_available_places_before_entering = db.session.query(Parking).get(
        client_parking_data["parking_id"]).to_json()["count_available_places"]
    assert count_available_places_before_entering >= 1
    response = client.post("/client_parkings", data=client_parking_data)
    assert response.status_code == 200
    count_available_places_after_entering = db.session.query(Parking).get(
        client_parking_data["parking_id"]).to_json()["count_available_places"]
    assert count_available_places_before_entering - count_available_places_after_entering == 1


@pytest.mark.parking
def test_delete_parking_client(client, db):
    client_parking_data = {"client_id": "1",
                           "parking_id": "1"}
    count_available_places_before_deleting = db.session.query(Parking).get(
        client_parking_data["parking_id"]).to_json()["count_available_places"]
    response = client.delete("/client_parkings", data=client_parking_data)
    assert response.status_code == 200
    count_available_places_after_deleting = db.session.query(Parking).get(
        client_parking_data["parking_id"]).to_json()["count_available_places"]
    assert count_available_places_after_deleting - count_available_places_before_deleting == 1
    assert db.session.query(ClientParking).get(client_parking_data["parking_id"]).to_json()["time_out"] > \
           db.session.query(ClientParking).get(client_parking_data["parking_id"]).to_json()["time_in"]
    assert db.session.query(Client).get(client_parking_data["client_id"]).to_json()["credit_card"]
