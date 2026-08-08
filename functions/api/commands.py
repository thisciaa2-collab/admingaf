import os
from flask import request, jsonify

SECRET_TOKEN = "CRIS2026"  # <-- TOKEN CONFIGURADO

COMMANDS = []  # Misma lista que send_command.py

def on_request():
    global COMMANDS
    
    token = request.args.get('token')
    if token != SECRET_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    pending = COMMANDS.copy()
    COMMANDS.clear()
    
    print(f"[WEB] 📊 {len(pending)} comandos entregados")
    return jsonify(pending), 200
