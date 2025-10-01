
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt
from src.extensions import db
from src.models import DeviceToken
from src.schemas import DeviceTokenSchema
from src.firebase_admin_client import send_push_v1

bp = Blueprint("notifications", __name__)
schema = DeviceTokenSchema()

@bp.post("/register")
@jwt_required(optional=True)
def register_token():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        abort(400, description="token is required")
    claims = get_jwt() or {}
    dt = DeviceToken.query.filter_by(token=token).first()
    if not dt:
        dt = DeviceToken(token=token)
    dt.platform = data.get("platform", "android")
    dt.user_id = data.get("user_id") or claims.get("sub")
    dt.company_id = data.get("company_id") or claims.get("company_id")
    dt.plant_id = data.get("plant_id") or claims.get("plant_id")
    dt.role = data.get("role")
    dt.active = True
    db.session.add(dt)
    db.session.commit()
    return schema.dump(dt), 201

@bp.post("/unregister")
@jwt_required(optional=True)
def unregister_token():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        abort(400, description="token is required")
    dt = DeviceToken.query.filter_by(token=token).first()
    if dt:
        dt.active = False
        db.session.commit()
    return {"message":"unregistered"}, 200

@bp.post("/send")
@jwt_required()
def send():
    data = request.get_json() or {}
    tokens = data.get("tokens", [])
    title = data.get("title", "SOS")
    body = data.get("body", "Alerta")
    extra = data.get("data", {})
    if not tokens:
        q = DeviceToken.query.filter_by(active=True)
        if cid := data.get("company_id"):
            q = q.filter(DeviceToken.company_id==cid)
        if pid := data.get("plant_id"):
            q = q.filter(DeviceToken.plant_id==pid)
        if role := data.get("role"):
            q = q.filter(DeviceToken.role==role)
        tokens = [t.token for t in q.all()]
    res = send_push_v1(tokens, title, body, extra)
    return {"requested": len(tokens), "result": res}
