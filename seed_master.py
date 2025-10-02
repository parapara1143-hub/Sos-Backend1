import os
from src.extensions import db
from src.models import User  # ajuste se o model do usuário tiver outro nome
from app import create_app
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    email = "master@sos.com"
    password = "123456"   # você pode trocar depois
    role = "master"       # importante para diferenciar de admin normal

    if not User.query.filter_by(email=email).first():
        user = User(
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        print("Usuário master criado com sucesso:", email)
    else:
        print("Usuário master já existe:", email)
