import os
import time
from flask import jsonify

SECRET_TOKEN = "CRIS2026"

# Misma lista de logs que en webhook.py (compartida)
LOG_HISTORY = []

def on_request():
    token = request.args.get('token') if hasattr(request, 'args') else None
    # Si viene con token, verificar (opcional)
    return jsonify(LOG_HISTORY)
