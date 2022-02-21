import json
import sqlite3
from datetime import datetime
from typing import List

import requests
from flask import request

ROOMS = [
    {"floor": 2, "beds": 1, "guestNum": 2, "price": 100},
    {"floor": 2, "beds": 2, "guestNum": 4, "price": 200},
    {"floor": 2, "beds": 2, "guestNum": 5, "price": 300},
    {"floor": 2, "beds": 3, "guestNum": 4, "price": 400},
    {"floor": 2, "beds": 4, "guestNum": 5, "price": 500}
]

BOOKINGS = [
    {'room_id': 3, 'checkInDate': 20200308, 'checkOutDate': 20200311, 'guest_id': 1},
    {'room_id': 3, 'checkInDate': 20220411, 'checkOutDate': 20220412, 'guest_id': 2},
    {'room_id': 4, 'checkInDate': 20220308, 'checkOutDate': 20220311, 'guest_id': 1}]

GUESTS = [
    {'firstName': 'qwerty', 'lastName': 'aaa'},
    {'firstName': 'asdfgh', 'lastName': 'bbb'}
]


class Room:
    def __init__(self, roomId: int, floor: int, beds: int, guestNum: int, price) -> None:
        self.floor = floor
        self.beds = beds
        self.guestNum = guestNum
        self.price = price
        self.roomId = roomId

    def room_to_dict(self) -> dict:
        return {"floor": self.floor,
                "guestNum": self.guestNum,
                "beds": self.beds,
                "price": self.price,
                "roomId": self.roomId}


def init_db_guests(initial_guests: List[dict]) -> None:
    with sqlite3.connect('table_guests.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DROP TABLE IF EXISTS `table_guests`"
        )
        cursor.execute(
            "CREATE TABLE `table_guests`"
            "(guest_id INTEGER PRIMARY KEY AUTOINCREMENT, firstName, lastName)")

        cursor.executemany(
            'INSERT INTO `table_guests` '
            '(firstName, lastName) VALUES (?, ?)',
            [(item['firstName'], item['lastName'])
             for item in initial_guests]
        )


def init_db_bookings(initial_bookings: List[dict]) -> None:
    with sqlite3.connect('table_bookings.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DROP TABLE IF EXISTS `table_bookings`"
        )
        cursor.execute(
            "CREATE TABLE `table_bookings`"
            "(booking_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "room_id, checkInDate INTEGER, checkOutDate INTEGER , guest_id)")

        cursor.executemany(
            'INSERT INTO `table_bookings` '
            '(room_id, checkInDate, checkOutDate, guest_id) VALUES (?, ?, ?, ?)',
            [(item['room_id'], item['checkInDate'], item['checkOutDate'], item['guest_id'])
             for item in initial_bookings]
        )


def init_db_rooms(initial_rooms: List[dict]) -> None:
    with sqlite3.connect('table_rooms.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE `table_rooms`'
            '(roomId INTEGER PRIMARY KEY AUTOINCREMENT, floor, beds, guestNum, price)'
        )

        cursor.executemany(
            'INSERT INTO `table_rooms` '
            '(floor, beds, guestNum, price) VALUES (?, ?, ?, ?)',
            [(item['floor'], item['beds'], item['guestNum'], item['price'])
             for item in initial_rooms]
        )


def init_db() -> None:
    with sqlite3.connect('table_rooms.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='table_rooms'"
        )
        exists = cursor.fetchone()
        if not exists:
            init_db_rooms(ROOMS)
            init_db_bookings(BOOKINGS)
            init_db_guests(GUESTS)


def get_all_rooms() -> json:
    rooms_list = {"rooms": []}
    with sqlite3.connect('table_rooms.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from `table_rooms`')
        rooms = cursor.fetchall()
        for record in rooms:
            room = Room.room_to_dict(Room(record[0], record[1], record[2], record[3], record[4]))
            rooms_list["rooms"].append(room)
    return json.dumps(rooms_list, indent=4)


def add_new_room() -> json:
    request_data = request.get_json()
    with sqlite3.connect('table_rooms.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO `table_rooms` '
                       '(floor, beds, guestNum, price) '
                       'VALUES (?, ?, ?, ?)',
                       (request_data["floor"],
                        request_data["beds"],
                        request_data["guestNum"],
                        request_data["price"]))
    return f'Room with {json.dumps(request_data, indent=4)} was added', 200


def check_room_is_free(rooms_id: List, checkIn: int, checkOut: int) -> List[int]:
    free_rooms_id = []
    with sqlite3.connect('table_bookings.db') as conn:
        cursor = conn.cursor()
        for room_id in rooms_id:
            cursor.execute(
                "SELECT * from `table_bookings`"
                "WHERE room_id = ?"
                "ORDER BY checkOutDate DESC",
                (room_id,)
            )
            bookings = cursor.fetchall()
            if len(bookings) == 0:
                free_rooms_id.append(room_id)
            else:
                if int(bookings[0][3]) <= checkIn:
                    free_rooms_id.append(room_id)
                for i in range(1, len(bookings)):
                    if int(bookings[i][3]) <= checkIn and int(bookings[i - 1][2]) >= checkOut:
                        free_rooms_id.append(room_id)
                        break
    return free_rooms_id


def check_dates_are_correct(checkIn: int, checkOut: int) -> bool:
    if checkOut <= checkIn or datetime.strptime(str(checkIn), "%Y%m%d").date() < datetime.today().date():
        return False
    return True


def get_a_room() -> json:
    rooms_id = []
    rooms_list = {"rooms": []}
    checkIn = int(request.args.get('checkIn'))
    checkOut = int(request.args.get('checkOut'))
    guestsNum = int(request.args.get('guestsNum'))

    if not check_dates_are_correct(checkIn, checkOut):
        rooms_list['rooms'].append('Wrong date')
        return rooms_list, 200

    with sqlite3.connect('table_rooms.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from `table_rooms`'
                       'WHERE guestNum >= ?'
                       'ORDER BY guestNum',
                       (guestsNum,)
                       )
        rooms = cursor.fetchall()
        for record in rooms:
            rooms_id.append(record[0])

    free_rooms_id = check_room_is_free(rooms_id, checkIn, checkOut)

    for room in rooms:
        if room[0] in free_rooms_id:
            free_room = Room.room_to_dict(
                Room(room[0], room[1], room[2], room[3], room[4]))
            rooms_list["rooms"].append(free_room)

    return json.dumps(rooms_list, indent=4)


def check_guest_in_db(firstName: str, lastName: str) -> int:
    with sqlite3.connect('table_guests.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from `table_guests`'
                       'WHERE firstName = ? AND lastName = ?',
                       (firstName, lastName)
                       )
        exist = cursor.fetchone()
        if not exist:
            return 0
        return exist[0]


def add_guest_in_db(firstName: str, lastName: str) -> int:
    with sqlite3.connect('table_guests.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO `table_guests` (firstName, lastName) VALUES (?, ?)',
                       (firstName, lastName)
                       )
    return check_guest_in_db(firstName, lastName)


def book_the_room(roomId: int, checkIn: int, checkOut: int, guestId: int) -> None:
    with sqlite3.connect('table_bookings.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO `table_bookings` (room_id, checkInDate, checkOutDate, guest_id) VALUES (?, ?, ?, ?)',
            (roomId, checkIn, checkOut, guestId)
        )


def booking_room():
    if request.cookies.get('token'):
        request_data = request.json
        checkIn = request_data['bookingDates']['checkIn']
        checkOut = request_data['bookingDates']['checkOut']
        roomId = int(request_data['roomId'])
        firstName = request_data['firstName']
        lastName = request_data['lastName']
        if check_dates_are_correct(checkIn, checkOut):
            if roomId in check_room_is_free([roomId], checkIn, checkOut):
                guestId = check_guest_in_db(firstName, lastName)
                if guestId == 0:
                    guestId = add_guest_in_db(firstName, lastName)
                book_the_room(roomId, int(checkIn), int(checkOut), int(guestId))
                return json.dumps(f'Room with id {roomId} was booked '
                                  f'for {firstName} {lastName} '
                                  f'from {datetime.strptime(str(checkIn), "%Y%m%d").date()} '
                                  f'to {datetime.strptime(str(checkOut), "%Y%m%d").date()}', indent=4), 200
            return 'Room is booked yet', 409
        return 'Wrong date', 409
    return 'No token', 409
