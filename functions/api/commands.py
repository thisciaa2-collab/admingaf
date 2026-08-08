import os
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"

# Misma lista que send_command.py (en producción usa una base de datos)
COMMANDS = []

def on_request():
    global COMMANDS
    
    # Verificar método
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed. Use GET"}), 405
    
    # Verificar autenticación
    token = request.args.get('token')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Devolver comandos y limpiar
    pending = COMMANDS.copy()
    COMMANDS.clear()
    
    print(f"[WEB] 📊 {len(pending)} comandos entregados")
    return jsonify(pending), 200
