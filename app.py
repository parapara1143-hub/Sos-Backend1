import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

# Carregar variáveis do .env local (em dev)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar modelos depois do db estar definido
from src.models.user import User


@app.route("/")
def health():
    return jsonify({"status": "Backend rodando 🚀"}), 200


@app.route("/internal/seed-master", methods=["POST"])
def seed_master():
    """Cria o usuário master para login no painel"""
    try:
        # Checar se já existe
        master = User.query.filter_by(email="master@sos.com").first()
        if master:
            return jsonify({"message": "Usuário master já existe"}), 200

        master = User(
            name="Master",
            email="master@sos.com",
            password="123456",  # ⚠️ Trocar por hash em produção!
            role="master"
        )
        db.session.add(master)
        db.session.commit()

        return jsonify({"message": "Usuário master criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
