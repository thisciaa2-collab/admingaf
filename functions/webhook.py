import os
import json
import time
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"  # <-- TOKEN CONFIGURADO

LOG_HISTORY = []
MAX_LOGS = 100

def on_request():
    global LOG_HISTORY
    
    secret = request.headers.get('x-roblox-secret')
    if secret != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    event = data.get('event')
    payload = data.get('data', {})
    
    log_entry = {
        "timestamp": time.time(),
        "event": event,
        "data": payload
    }
    LOG_HISTORY.append(log_entry)
    if len(LOG_HISTORY) > MAX_LOGS:
        LOG_HISTORY.pop(0)
    
    print(f"[WEBHOOK] 📨 {event} | {json.dumps(payload)}")
    
    return jsonify({"status": "ok"}), 200
