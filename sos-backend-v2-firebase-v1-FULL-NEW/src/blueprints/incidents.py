
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from src.extensions import db, socketio
from src.models import Incident, DeviceToken
from src.schemas import IncidentSchema
from src.utils import paginate
from src.firebase_admin_client import send_push_v1

bp = Blueprint("incidents", __name__)
schema = IncidentSchema()

@bp.get("/")
@jwt_required()
def list_incidents():
    q = Incident.query.order_by(Incident.id.desc())
    severity = request.args.get("severity")
    status = request.args.get("status")
    if severity: q = q.filter(Incident.severity==severity)
    if status: q = q.filter(Incident.status==status)
    return paginate(q, schema)

@bp.post("/")
@jwt_required()
def create_incident():
    data = request.get_json() or {}
    obj = Incident(**data)
    db.session.add(obj)
    db.session.commit()
    payload = schema.dump(obj)
    # realtime web
    socketio.emit("new_incident", payload, namespace="/incidents")
    # push mobile (segmentação simples)
    q = DeviceToken.query.filter_by(active=True)
    if obj.company_id:
        q = q.filter(DeviceToken.company_id==obj.company_id)
    if obj.plant_id:
        q = q.filter(DeviceToken.plant_id==obj.plant_id)
    roles = None
    if obj.severity and obj.severity.lower() in ["critical", "high"]:
        roles = None  # todos no escopo
    else:
        roles = ["brigadista", "leader", "líder"]
    if roles:
        q = q.filter(DeviceToken.role.in_(roles))
    tokens = [t.token for t in q.all()]
    title = f"Incidente: {obj.title}"
    body = f"Severidade: {obj.severity or 'n/d'} | Status: {obj.status or 'open'}"
    extra = {"incident_id": obj.id, "plant_id": obj.plant_id or 0, "company_id": obj.company_id or 0}
    send_push_v1(tokens, title, body, extra)
    return payload, 201
