import os
import json
import time
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"

LOG_HISTORY = []
MAX_LOGS = 100

def on_request():
    global LOG_HISTORY
    
    # Verificar método
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed. Use POST"}), 405
    
    # Verificar autenticación
    secret = request.headers.get('x-roblox-secret')
    if secret != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Obtener datos
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    event = data.get('event')
    payload = data.get('data', {})
    
    # Guardar en logs
    log_entry = {
        "timestamp": time.time(),
        "event": event,
        "data": payload
    }
    LOG_HISTORY.append(log_entry)
    if len(LOG_HISTORY) > MAX_LOGS:
        LOG_HISTORY.pop(0)
    
    print(f"[WEBHOOK] 📨 {event} | {json.dumps(payload)}")
    
    return jsonify({"status": "ok", "event": event}), 200

# ----------------------------------------------------------------
#  ENDPOINT PARA VER LOGS
# ----------------------------------------------------------------
# Si quieres logs vía GET, crea otro archivo functions/logs.py
