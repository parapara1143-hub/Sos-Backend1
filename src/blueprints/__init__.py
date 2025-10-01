
from .auth import bp as auth_bp
from .companies import bp as companies_bp
from .plants import bp as plants_bp
from .users import bp as users_bp
from .employees import bp as employees_bp
from .incidents import bp as incidents_bp
from .reports import bp as reports_bp
from .settings import bp as settings_bp
from .audit_api import bp as audit_bp
from .notifications import bp as notifications_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(companies_bp, url_prefix="/api/companies")
    app.register_blueprint(plants_bp, url_prefix="/api/plants")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(employees_bp, url_prefix="/api/employees")
    app.register_blueprint(incidents_bp, url_prefix="/api/incidents")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(audit_bp, url_prefix="/api/audit")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
