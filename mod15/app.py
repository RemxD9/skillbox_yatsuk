from flask import jsonify, request
from models import Room, app


@app.route('/get-room')
def get_rooms():
    rooms = Room.get_all_rooms()
    return jsonify({'rooms': [{'roomId': room.id, 'floor': room.floor, 'guestNum': room.guest_num, 'beds': room.beds,
                               'price': room.price} for room in rooms]}), 200


@app.route('/add-room', methods=['POST'])
def adding_room():
    if request.method == 'POST':
        room_data = {
            'floor': request.form.get('floor'),
            'guest_num': request.form.get('guest_num'),
            'beds': request.form.get('beds'),
            'price': request.form.get('price')
        }
        Room.create_room(room_data)
        rooms = Room.get_all_rooms()
        return jsonify(
            {'rooms': [{'roomId': room.id, 'floor': room.floor, 'guestNum': room.guest_num, 'beds': room.beds,
                        'price': room.price} for room in rooms]}), 200
    else:
        return jsonify({'message': 'Invalid request method'}), 400


@app.route('/booking', methods=['POST'])
def booking_room():
    if request.method == 'POST':
        booked_room_data = request.form.get('id')
        if Room.booking_room(booked_room_data):
            return jsonify({'message': 'Room has been booked successfully'}), 200
        else:
            return jsonify({'message': 'Cannot book this room, maybe it has already been booked'}), 409
    else:
        return jsonify({'message': 'Invalid request method'}), 400


if __name__ == '__main__':
    app.run(debug=True)
