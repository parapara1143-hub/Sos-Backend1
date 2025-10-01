
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from src.extensions import db
from src.models import Employee
from src.schemas import EmployeeSchema
from src.utils import paginate

bp = Blueprint("employees", __name__)
schema = EmployeeSchema()

@bp.get("/")
@jwt_required()
def list_employees():
    return paginate(Employee.query.order_by(Employee.id.desc()), schema)

@bp.post("/")
@jwt_required()
def create_employee():
    data = request.get_json() or {}
    obj = Employee(**data)
    db.session.add(obj)
    db.session.commit()
    return schema.dump(obj), 201
