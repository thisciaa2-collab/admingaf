import time
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"

COMMANDS = []  # Misma lista que commands.py

def on_request():
    # SOLO ACEPTA POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed. Use POST"}), 405
    
    # Verificar token
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    # Validar datos
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "Falta 'action'"}), 400

    # Guardar comando
    command = {
        "action": data['action'],
        "player": data.get('player', ''),
        "amount": data.get('amount', 0),
        "seedType": data.get('seedType', 'AppleSeed'),
        "timestamp": time.time()
    }
    
    COMMANDS.append(command)
    print(f"[WEB] 🎮 Comando: {command['action']} para {command['player']}")
    
    return jsonify({
        "status": "ok",
        "message": "Comando encolado",
        "pending": len(COMMANDS)
    }), 200
