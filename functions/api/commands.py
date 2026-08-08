from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"

COMMANDS = []

def on_request():
    global COMMANDS
    
    # SOLO ACEPTA GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed. Use GET"}), 405
    
    # Verificar token
    token = request.args.get('token')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Devolver comandos y limpiar
    pending = COMMANDS.copy()
    COMMANDS.clear()
    
    print(f"[WEB] 📊 {len(pending)} comandos entregados")
    return jsonify(pending), 200
