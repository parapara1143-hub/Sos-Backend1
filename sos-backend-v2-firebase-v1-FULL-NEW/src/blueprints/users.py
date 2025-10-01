
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from src.extensions import db
from src.models import User
from src.schemas import UserSchema
from src.utils import paginate

bp = Blueprint("users", __name__)
schema = UserSchema()

@bp.get("/")
@jwt_required()
def list_users():
    return paginate(User.query.order_by(User.id.desc()), schema)

@bp.post("/")
@jwt_required()
def create_user():
    data = request.get_json() or {}
    if "email" not in data or "password" not in data:
        abort(400, description="email and password required")
    obj = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role=data.get("role", "collaborator"),
        company_id=data.get("company_id"),
        plant_id=data.get("plant_id"),
    )
    db.session.add(obj)
    db.session.commit()
    return schema.dump(obj), 201
