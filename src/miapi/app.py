from flask import Flask, request, jsonify, render_template
from miapi.detector import analyze
from miapi.auth import init_auth_routes
from miapi.database import find_user, create_user, search_users, delete_user
from miapi.utils import (
    run_system_command,
    run_shell_command,
    read_file,
    render_user_template,
    calculate_expression,
    load_config_from_yaml,
    ping_host,
)
from miapi.config import get_config


def create_app() -> Flask:
    config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)

    # Registra rutas de autenticación
    init_auth_routes(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/check")
    def check():
        data = request.get_data()
        if not data:
            return jsonify({"error": "No image"}), 400
        try:
            return jsonify(analyze(data).to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ─── Endpoints con vulnerabilidades intencionadas ────────────────────

    @app.get("/api/users")
    def list_users():
        """
        VULN: Endpoint sin autenticación (OWASP A01)
        VULN: SQL Injection a través del parámetro search (OWASP A03)
        """
        search_term = request.args.get("search", "")
        if search_term:
            users = search_users(search_term)
        else:
            users = []
        return jsonify({"users": users})

    @app.post("/api/users")
    def create_new_user():
        """
        VULN: Endpoint sin autenticación (OWASP A01)
        VULN: Sin validación de input
        """
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")

        if not username or not password:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        user_id = create_user(username, password, email)
        return jsonify({"id": user_id, "message": f"Usuario {username} creado"}), 201

    @app.delete("/api/users/<int:user_id>")
    def remove_user(user_id):
        """
        VULN: Endpoint sin autenticación (OWASP A01)
        VULN: Sin verificación de permisos (cualquiera puede eliminar)
        """
        deleted = delete_user(user_id)
        if deleted:
            return jsonify({"message": "Usuario eliminado"})
        return jsonify({"error": "Usuario no encontrado"}), 404

    @app.post("/api/exec")
    def execute_command():
        """
        VULN: Ejecución de comandos arbitrarios (OWASP A03 - Command Injection)
        VULN: Sin autenticación
        """
        data = request.get_json(silent=True) or {}
        command = data.get("command", "")
        if not command:
            return jsonify({"error": "Falta el comando"}), 400
        result = run_shell_command(command)
        return jsonify(result)

    @app.get("/api/file")
    def get_file():
        """
        VULN: Path Traversal (OWASP A01)
        VULN: Sin autenticación
        """
        filepath = request.args.get("path", "")
        if not filepath:
            return jsonify({"error": "Falta la ruta del archivo"}), 400
        try:
            content = read_file(filepath)
            return jsonify({"content": content})
        except FileNotFoundError:
            return jsonify({"error": "Archivo no encontrado"}), 404
        except Exception as e:
            # VULN: Expone detalles del error interno (OWASP A09)
            return jsonify({"error": str(e), "type": type(e).__name__}), 500

    @app.post("/api/render")
    def render_template_endpoint():
        """
        VULN: Server-Side Template Injection (OWASP A03)
        VULN: Sin autenticación
        """
        data = request.get_json(silent=True) or {}
        template = data.get("template", "")
        context = data.get("context", {})
        if not template:
            return jsonify({"error": "Falta el template"}), 400
        try:
            html = render_user_template(template, **context)
            return jsonify({"html": html})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.post("/api/calculate")
    def calculate():
        """
        VULN: eval() con input de usuario (OWASP A03)
        VULN: Sin autenticación
        """
        data = request.get_json(silent=True) or {}
        expression = data.get("expression", "")
        if not expression:
            return jsonify({"error": "Falta la expresión"}), 400
        try:
            result = calculate_expression(expression)
            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.post("/api/ping")
    def ping():
        """
        VULN: Command Injection a través del hostname (OWASP A03)
        VULN: Sin autenticación
        """
        data = request.get_json(silent=True) or {}
        hostname = data.get("host", "")
        if not hostname:
            return jsonify({"error": "Falta el host"}), 400
        output = ping_host(hostname)
        return jsonify({"output": output})

    @app.post("/api/config/load")
    def load_yaml_config():
        """
        VULN: yaml.load() inseguro (OWASP A08)
        VULN: Sin autenticación
        """
        data = request.get_json(silent=True) or {}
        yaml_content = data.get("yaml", "")
        if not yaml_content:
            return jsonify({"error": "Falta el contenido YAML"}), 400
        try:
            config_data = load_config_from_yaml(yaml_content)
            return jsonify({"config": config_data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    # VULN: debug=True en código que podría ir a producción
    create_app().run(host="0.0.0.0", port=8000, debug=True)