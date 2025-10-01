
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.extensions import db, migrate, socketio
from src.config import load_config
from src.audit import audit_middleware
from src.blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    load_config(app)
    CORS(app, origins=app.config.get("CORS_ORIGINS").split(","), supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    audit_middleware(app)
    register_blueprints(app)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    socketio.init_app(app, cors_allowed_origins=os.environ.get("SOCKET_CORS","*").split(","))
    socketio.run(app, host="0.0.0.0", port=port)
