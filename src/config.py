import os
from dotenv import load_dotenv

def load_config(app):
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")

    db_url = os.getenv("DATABASE_URL", "sqlite:///sos.db")

    # 🔥 Corrige automaticamente o driver do Postgres para usar psycopg3
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-dev")
    app.config["CORS_ORIGINS"] = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    app.config["SOCKET_CORS"] = os.getenv("SOCKET_CORS", app.config["CORS_ORIGINS"])
