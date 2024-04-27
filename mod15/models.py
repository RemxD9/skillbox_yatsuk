from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
db = SQLAlchemy(app)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    floor = db.Column(db.Integer)
    guest_num = db.Column(db.Integer)
    beds = db.Column(db.Integer)
    price = db.Column(db.Integer)
    is_booked = db.Column(db.Boolean, default=False)

    @classmethod
    def get_all_rooms(cls):
        return cls.query.filter_by(is_booked=False).all()

    @classmethod
    def create_room(cls, data):
        new_room = cls(floor=data['floor'], guest_num=data['guest_num'], beds=data['beds'], price=data['price'])
        db.session.add(new_room)
        db.session.commit()

    @classmethod
    def booking_room(cls, room_id):
        room = cls.query.get(room_id)
        if room and not room.is_booked:
            room.is_booked = True
            db.session.commit()
            return True
        else:
            return False


def downloading_first_data_in_database(database):
    with app.app_context():
        database.create_all()
        room1 = Room(floor=2, guest_num=1, beds=1, price=2000)
        room2 = Room(floor=1, guest_num=2, beds=1, price=2500)
        room3 = Room(floor=3, guest_num=1, beds=1, price=3500)
        database.session.add(room1)
        database.session.add(room2)
        database.session.add(room3)
        database.session.commit()


if __name__ == '__main__':
    downloading_first_data_in_database(db)
