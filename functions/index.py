from flask import jsonify

def on_request():
    return jsonify({
        "status": "online 🟢",
        "endpoints": [
            {"method": "POST", "path": "/webhook", "description": "Recibe notificaciones de Roblox"},
            {"method": "POST", "path": "/api/send_command", "description": "Envía comandos desde tu web"},
            {"method": "GET", "path": "/api/commands", "description": "Roblox consulta comandos pendientes"},
            {"method": "GET", "path": "/", "description": "Esta página"}
        ],
        "logs": "Ver logs en tiempo real en Cloudflare Dashboard"
    })
