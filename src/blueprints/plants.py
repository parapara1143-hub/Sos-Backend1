
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from src.extensions import db
from src.models import Plant, Company
from src.schemas import PlantSchema
from src.utils import paginate

bp = Blueprint("plants", __name__)
schema = PlantSchema()

@bp.get("/")
@jwt_required()
def list_plants():
    return paginate(Plant.query.order_by(Plant.id.desc()), schema)

@bp.post("/")
@jwt_required()
def create_plant():
    data = request.get_json() or {}
    if not Company.query.get(data["company_id"]):
        abort(400, description="company not found")
    obj = Plant(name=data["name"], company_id=data["company_id"])
    db.session.add(obj)
    db.session.commit()
    return schema.dump(obj), 201
