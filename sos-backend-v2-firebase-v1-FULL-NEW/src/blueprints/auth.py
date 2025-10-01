
from flask import Blueprint, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from src.extensions import db
from src.models import User, Company, Plant

bp = Blueprint("auth", __name__)

@bp.post("/bootstrap")
def bootstrap():
    data = request.get_json() or {}
    email = data.get("email", "master@sos.com")
    password = data.get("password", "master123")
    if User.query.filter_by(email=email).first():
        return {"message": "Already initialized"}, 200
    company = Company(name="Master Corp", code="MASTER")
    db.session.add(company)
    db.session.flush()
    plant = Plant(name="HQ", company_id=company.id)
    db.session.add(plant)
    db.session.flush()
    user = User(email=email, password_hash=generate_password_hash(password), role="master", company_id=company.id, plant_id=plant.id)
    db.session.add(user)
    db.session.commit()
    return {"message": "Bootstrap complete", "email": email, "password": password}

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        abort(400, description="email and password are required")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        abort(401, description="invalid credentials")
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role, "company_id": user.company_id, "plant_id": user.plant_id})
    return {"access_token": token, "role": user.role}
