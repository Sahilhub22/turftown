from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Turf(db.Model):
    __tablename__ = 'turfs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), default='Coimbatore')
    sport_type = db.Column(db.String(50), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    amenities = db.Column(db.String(300))
    rating = db.Column(db.Float, default=4.0)
    total_reviews = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    open_time = db.Column(db.String(10), default='06:00')
    close_time = db.Column(db.String(10), default='23:00')
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    slots = db.relationship('TurfSlot', backref='turf', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='turf', lazy=True)

    def __repr__(self):
        return f'<Turf {self.name}>'


class TurfSlot(db.Model):
    __tablename__ = 'turf_slots'
    id = db.Column(db.Integer, primary_key=True)
    turf_id = db.Column(db.Integer, db.ForeignKey('turfs.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=False)

    booking = db.relationship('Booking', backref='slot', uselist=False)

    def __repr__(self):
        return f'<Slot {self.date} {self.start_time}-{self.end_time}>'


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    turf_id = db.Column(db.Integer, db.ForeignKey('turfs.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('turf_slots.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    payment_method = db.Column(db.String(30), default='Pay at Venue')
    booking_ref = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f'<Booking {self.booking_ref}>'
