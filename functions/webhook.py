import json
import time
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"

LOG_HISTORY = []
MAX_LOGS = 100

def on_request():
    global LOG_HISTORY
    
    # SOLO ACEPTA POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed. Use POST"}), 405
    
    # Verificar token
    secret = request.headers.get('x-roblox-secret')
    if secret != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Obtener datos
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    event = data.get('event', 'unknown')
    payload = data.get('data', {})
    
    # Guardar log
    LOG_HISTORY.append({
        "timestamp": time.time(),
        "event": event,
        "data": payload
    })
    if len(LOG_HISTORY) > MAX_LOGS:
        LOG_HISTORY.pop(0)
    
    print(f"[WEBHOOK] 📨 {event} | {json.dumps(payload)}")
    
    return jsonify({"status": "ok", "event": event}), 200
