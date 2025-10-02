import os
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import upgrade
from werkzeug.security import generate_password_hash

from src.extensions import db, migrate, socketio
from src.config import load_config
from src.audit import audit_middleware
from src.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)
    load_config(app)

    # Configurações básicas
    CORS(app, origins=app.config.get("CORS_ORIGINS").split(","), supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    audit_middleware(app)
    register_blueprints(app)

    # 🔹 Rodar migrations automaticamente ao iniciar
    with app.app_context():
        try:
            upgrade()
            print("✅ Migrações aplicadas com sucesso.")
        except Exception as e:
            print("⚠️ Erro ao rodar migrations:", e)

    # rota de health check
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    # rota raiz para evitar 404
    @app.get("/")
    def index():
        return {"message": "API SOS rodando 🚀", "status": "ok"}

    # rota para seed do usuário master
    @app.post("/internal/seed-master")
    def seed_master():
        token = request.headers.get("X-Seed-Token")
        if token != os.environ.get("SEED_TOKEN"):
            return {"error": "unauthorized"}, 401

        email = os.environ.get("MASTER_EMAIL", "master@sos.com")
        password = os.environ.get("MASTER_PASSWORD", "123456")

        from src.models.user import User  # ⚠️ ajuste para o caminho real do seu modelo

        # garante que a tabela existe
        db.create_all()

        existing = User.query.filter_by(email=email).first()
        if existing:
            return {"message": "usuario_master_ja_existe"}, 200

        user = User(
            email=email,
            name="Master",
            role="master",
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "usuario_master_criado"}, 201

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    socketio.init_app(app, cors_allowed_origins=os.environ.get("SOCKET_CORS", "*").split(","))
    socketio.run(app, host="0.0.0.0", port=port)
