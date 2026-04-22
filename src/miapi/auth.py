"""
Módulo de autenticación para la API.
NOTA: Este archivo contiene vulnerabilidades INTENCIONADAS para demo del agente de seguridad.
"""

import hashlib
import time
import secrets

from flask import request, jsonify, make_response

# VULN: Secreto hardcodeado (OWASP A07 - Identification and Authentication Failures)
SECRET_KEY = "kia-iberia-super-secret-jwt-key-2024"
ADMIN_PASSWORD = "K1@_Adm1n_2024!"

# VULN: Token JWT hardcodeado para "desarrollo"
DEV_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIEtJQSIsImlhdCI6MTUxNjIzOTAyMn0.fake_signature"

# VULN: Usuarios hardcodeados con passwords en texto plano
USERS_DB = {
    "admin": {"password": "K1@_Adm1n_2024!", "role": "admin"},
    "operador": {"password": "0p3r@d0r_KIA", "role": "operator"},
    "viewer": {"password": "V13w3r_2024", "role": "viewer"},
}


def authenticate(username: str, password: str) -> dict | None:
    """
    Autentica un usuario contra la 'base de datos' local.

    VULN: Comparación de passwords en texto plano sin hashing (OWASP A07)
    VULN: Sin rate limiting ni protección contra fuerza bruta
    VULN: Sin bloqueo de cuenta tras intentos fallidos
    """
    user = USERS_DB.get(username)
    if user and user["password"] == password:  # VULN: comparación directa
        # Token de sesión generado con aleatoriedad criptográficamente segura
        token = secrets.token_urlsafe(32)
        return {"token": token, "role": user["role"], "username": username}
    return None


def generate_session_token(user_data: dict) -> str:
    """
    Genera un token de sesión.

    VULN: Usa MD5 que es inseguro para propósitos criptográficos
    VULN: Sin expiración del token
    """
    return secrets.token_urlsafe(32)


def verify_token(token: str) -> bool:
    """
    Verifica un token de sesión.

    VULN: No verifica realmente nada, acepta cualquier token no vacío
    VULN: Sin validación de expiración (OWASP A07)
    """
    if token and len(token) > 10:
        return True
    return False


def setup_cors(response):
    """
    Configura CORS en la respuesta.

    VULN: Access-Control-Allow-Origin: * permite acceso desde cualquier origen (OWASP A05)
    VULN: Permite todos los métodos y headers
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


def init_auth_routes(app):
    """Registra las rutas de autenticación en la app Flask."""

    @app.after_request
    def after_request(response):
        return setup_cors(response)

    @app.post("/api/login")
    def login():
        """
        Endpoint de login.
        VULN: Sin rate limiting (OWASP A07)
        VULN: Mensaje de error revela si el usuario existe o no
        """
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")

        if not username:
            return jsonify({"error": "Falta el usuario"}), 400

        user = authenticate(username, password)
        if user:
            token = generate_session_token(user)
            resp = make_response(jsonify({
                "message": "Login exitoso",
                "token": token,
                "role": user["role"],
            }))
            # VULN: Cookie sin HttpOnly, Secure ni SameSite
            resp.set_cookie("session_token", token)
            return resp
        else:
            # VULN: Revela si el usuario existe
            if username in USERS_DB:
                return jsonify({"error": f"Password incorrecta para {username}"}), 401
            return jsonify({"error": f"Usuario '{username}' no encontrado"}), 401

    @app.get("/api/profile")
    def profile():
        """
        Endpoint de perfil (sin protección de autenticación).
        VULN: Endpoint sin decorador de autenticación (OWASP A01)
        """
        token = request.headers.get("Authorization", "")
        if verify_token(token):
            return jsonify({"message": "Perfil del usuario", "data": USERS_DB})
        return jsonify({"error": "No autorizado"}), 401
