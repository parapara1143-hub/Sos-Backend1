#!/bin/bash
set -e
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=${PORT:-8000}
python -m flask db upgrade || true
python app.py
