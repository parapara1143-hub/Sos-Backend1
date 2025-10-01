
from datetime import datetime
from src.extensions import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Company(db.Model, TimestampMixin):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    plants = db.relationship("Plant", backref="company", lazy=True)

class Plant(db.Model, TimestampMixin):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    employees = db.relationship("Employee", backref="plant", lazy=True)

class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), nullable=False, default="collaborator")
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"))

class Employee(db.Model, TimestampMixin):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    role = db.Column(db.String(50), default="collaborator")
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=False)

class Incident(db.Model, TimestampMixin):
    __tablename__ = "incidents"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    severity = db.Column(db.String(20), default="low")
    status = db.Column(db.String(20), default="open")
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"))
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class DeviceToken(db.Model, TimestampMixin):
    __tablename__ = "device_tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    platform = db.Column(db.String(20), default="android")  # android/ios
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=True)
    role = db.Column(db.String(40), nullable=True)
    active = db.Column(db.Boolean, default=True)
