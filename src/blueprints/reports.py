
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

bp = Blueprint("reports", __name__)

@bp.get("/kpi")
@jwt_required()
def kpi():
    return {
        "total_incidents": 128,
        "open_incidents": 15,
        "critical": 3,
        "avg_response_time_min": 7.4
    }

@bp.get("/timeseries")
@jwt_required()
def timeseries():
    days = int(request.args.get("days", 14))
    today = datetime.utcnow()
    data = [{"date": (today - timedelta(days=i)).strftime("%Y-%m-%d"), "incidents": (i*3 % 11)} for i in range(days)][::-1]
    return {"data": data}
