
from flask import Blueprint
from flask_jwt_extended import jwt_required

bp = Blueprint("audit", __name__)

@bp.get("/logs")
@jwt_required()
def logs():
    return {"logs": [
        {"action": "login", "user": "master@sos.com"},
        {"action": "create_incident", "user": "admin@plant.com"}
    ]}
