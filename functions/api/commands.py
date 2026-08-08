import os
from flask import request, jsonify

# ================================================================
#  COMMANDS - Roblox consulta comandos pendientes
# ================================================================

SECRET_TOKEN = os.environ.get('SECRET_TOKEN', 'mi_token_secreto_123456')

# Mismo almacén que send_command.py (EN MEMORIA, no persistente)
# Para producción, usa Cloudflare KV o una base de datos
COMMANDS = []

def on_request():
    global COMMANDS
    
    # 1. Verificar autenticación
    token = request.args.get('token')
    if token != SECRET_TOKEN:
        log_message("⚠️ Intento no autorizado", "commands", request.remote_addr)
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Devolver comandos y limpiar
    pending = COMMANDS.copy()
    COMMANDS.clear()
    
    log_message(f"📊 {len(pending)} comandos entregados", "commands")
    return jsonify(pending), 200

# ----------------------------------------------------------------
#  FUNCIÓN DE LOGGING
# ----------------------------------------------------------------
def log_message(message, endpoint, extra=""):
    print(f"[{endpoint.upper()}] {message} {extra}")
