from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)  # Increased from 120
    password_hash = db.Column(db.String(256))  # Increased from 128
    devices = db.relationship('Device', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    broker = db.Column(db.String(256), nullable=False)
    mqtt_user = db.Column(db.String(64), nullable=False)
    mqtt_password = db.Column(db.String(128), nullable=False)  # Encrypted in real app
    topic = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_points = db.relationship('DataPoint', backref='device', lazy='dynamic')

# class DataPoint(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     temperature = db.Column(db.Float)
#     humidity = db.Column(db.Float)
#     device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature_c = db.Column(db.Float)  # Renamed from temperature
    temperature_f = db.Column(db.Float)  # New field
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))