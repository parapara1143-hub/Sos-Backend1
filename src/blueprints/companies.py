
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from src.extensions import db
from src.models import Company
from src.schemas import CompanySchema
from src.utils import paginate

bp = Blueprint("companies", __name__)
schema = CompanySchema()

@bp.get("/")
@jwt_required()
def list_companies():
    return paginate(Company.query.order_by(Company.id.desc()), schema)

@bp.post("/")
@jwt_required()
def create_company():
    data = request.get_json() or {}
    obj = Company(name=data["name"], code=data["code"])
    db.session.add(obj)
    db.session.commit()
    return schema.dump(obj), 201
