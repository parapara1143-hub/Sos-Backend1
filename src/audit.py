
from datetime import datetime

def audit_middleware(app):
    @app.after_request
    def after(resp):
        resp.headers['X-Audit-Stamp'] = datetime.utcnow().isoformat()
        return resp
