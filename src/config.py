
import os
from dotenv import load_dotenv

def load_config(app):
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///sos.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-dev")
    app.config["CORS_ORIGINS"] = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    app.config["SOCKET_CORS"] = os.getenv("SOCKET_CORS", app.config["CORS_ORIGINS"])
