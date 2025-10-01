
from flask import Blueprint
from flask_jwt_extended import jwt_required

bp = Blueprint("settings", __name__)

@bp.get("/")
@jwt_required()
def read():
    return {"push_enabled": True, "maps_provider": "osm", "realtime": True}
