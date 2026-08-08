import os
import json
import time
from flask import request, jsonify

# ================================================================
#  WEBHOOK - Recibe notificaciones de Roblox
# ================================================================

# Obtener el token secreto desde variables de entorno (Cloudflare)
SECRET_TOKEN = os.environ.get('SECRET_TOKEN', 'mi_token_secreto_123456')

# Almacenamiento temporal (en producción usa una base de datos)
LOG_HISTORY = []
MAX_LOGS = 100

def on_request():
    global LOG_HISTORY
    
    # 1. Verificar autenticación
    secret = request.headers.get('x-roblox-secret')
    if secret != SECRET_TOKEN:
        log_message("⚠️ Intento no autorizado", "webhook", request.remote_addr)
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Obtener datos
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    # 3. Procesar evento
    event = data.get('event')
    timestamp = data.get('timestamp', time.time())
    payload = data.get('data', {})
    
    log_message(f"📨 {event}", "webhook", json.dumps(payload))
    
    # 4. Acciones según el evento
    if event == "PlayerBoughtSeed":
        player = payload.get('player')
        seed = payload.get('seed')
        log_message(f"🛒 {player} compró {seed}", "webhook")
    
    elif event == "PlayerHarvested":
        player = payload.get('player')
        apples = payload.get('appleCount')
        log_message(f"🍎 {player} recogió manzana (quedan {apples})", "webhook")
    
    elif event == "PlayerSlept":
        player = payload.get('player')
        log_message(f"🛌 {player} durmió", "webhook")
    
    elif event == "ServerStarted":
        log_message(f"🚀 Servidor iniciado: {payload.get('serverId')}", "webhook")
    
    elif event == "PlayerJoined":
        player = payload.get('player')
        log_message(f"👤 {player} se unió al juego", "webhook")
    
    elif event == "PlayerLeft":
        player = payload.get('player')
        log_message(f"👋 {player} salió del juego", "webhook")

    return jsonify({"status": "ok", "event": event}), 200

# ----------------------------------------------------------------
#  FUNCIÓN DE LOGGING
# ----------------------------------------------------------------
def log_message(message, endpoint, extra=""):
    global LOG_HISTORY
    log_entry = {
        "timestamp": time.time(),
        "endpoint": endpoint,
        "message": message,
        "extra": extra
    }
    LOG_HISTORY.append(log_entry)
    if len(LOG_HISTORY) > MAX_LOGS:
        LOG_HISTORY.pop(0)
    print(f"[{endpoint.upper()}] {message} {extra}")

# ----------------------------------------------------------------
#  ENDPOINT PARA VER LOGS (OPCIONAL)
# ----------------------------------------------------------------
# Si quieres ver los logs desde tu navegador, agrega este endpoint:
# @app.route('/logs', methods=['GET'])
# def get_logs():
#     return jsonify(LOG_HISTORY)
