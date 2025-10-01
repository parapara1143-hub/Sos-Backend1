
# SOS Backend v2 + Firebase Cloud Messaging (HTTP v1)

Backend unificado (Auth, Empresas/Plantas/Usuários/Colaboradores, Incidentes, Relatórios, Auditoria, Settings, WebSocket)
com **Push via Firebase Admin (HTTP v1)**.

## Como rodar local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```
Healthcheck: GET /api/health -> {"status":"ok"}

## Deploy (Render/Railway)
- Start Command: `bash start.sh`
- Variáveis:
  - SECRET_KEY / JWT_SECRET_KEY (strings longas aleatórias)
  - DATABASE_URL (Postgres do host)
  - FIREBASE_CREDENTIALS_JSON (conteúdo INTEIRO do JSON de Service Account)
  - CORS_ORIGINS / SOCKET_CORS (domínios do front)
