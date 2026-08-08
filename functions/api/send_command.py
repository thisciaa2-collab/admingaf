import os
import json
import time
from flask import request, jsonify

# ================================================================
#  SEND_COMMAND - Recibe comandos desde tu web
# ================================================================

SECRET_TOKEN = os.environ.get('SECRET_TOKEN', 'mi_token_secreto_123456')

# Almacén compartido de comandos (mismo que commands.py)
COMMANDS = []
COMMAND_LOCK = None  # En Cloudflare, necesitas usar un almacenamiento externo como KV

def on_request():
    # 1. Verificar autenticación
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        log_message("⚠️ Intento no autorizado", "send_command", request.remote_addr)
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Validar datos
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "Falta 'action'"}), 400

    # 3. Guardar comando
    command = {
        "action": data['action'],
        "player": data.get('player', ''),
        "amount": data.get('amount', 0),
        "seedType": data.get('seedType', 'AppleSeed'),
        "timestamp": time.time()
    }
    
    COMMANDS.append(command)
    log_message(f"🎮 {command['action']} para {command['player']}", "send_command")
    
    return jsonify({
        "status": "ok", 
        "message": "Comando encolado",
        "pending": len(COMMANDS)
    }), 200

# ----------------------------------------------------------------
#  FUNCIÓN DE LOGGING
# ----------------------------------------------------------------
def log_message(message, endpoint, extra=""):
    print(f"[{endpoint.upper()}] {message} {extra}")
