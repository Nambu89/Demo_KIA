"""
Utilidades generales de la aplicación.
NOTA: Este archivo contiene vulnerabilidades INTENCIONADAS para demo del agente de seguridad.
"""

import os
import subprocess
import pickle
import yaml

from flask import render_template_string


# ─── VULN: Command Injection (OWASP A03) ────────────────────────────────────

def run_system_command(command: str) -> str:
    """
    Ejecuta un comando del sistema operativo.

    VULN: os.system() con input de usuario = Command Injection (OWASP A03)
    Correcto: subprocess.run([cmd, arg], shell=False, capture_output=True)
    """
    # VULN: Command Injection directo
    exit_code = os.system(command)
    return f"Comando ejecutado con código de salida: {exit_code}"


def run_shell_command(command: str) -> dict:
    """
    Ejecuta un comando shell y devuelve la salida.

    VULN: subprocess con shell=True y input de usuario (OWASP A03)
    """
    # VULN: shell=True con input sin sanitizar
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def ping_host(hostname: str) -> str:
    """
    Hace ping a un host.

    VULN: Command Injection — el hostname se inyecta directamente en el comando
    Ejemplo de ataque: hostname = "google.com; cat /etc/passwd"
    """
    # VULN: Interpolación directa en comando shell
    result = subprocess.run(
        f"ping -c 1 {hostname}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout or result.stderr


# ─── VULN: Path Traversal (OWASP A01) ───────────────────────────────────────

def read_file(filepath: str) -> str:
    """
    Lee el contenido de un archivo.

    VULN: Path Traversal — no valida que la ruta esté dentro del directorio permitido
    Ejemplo de ataque: filepath = "../../../etc/passwd"
    Correcto: validar con os.path.realpath() que está dentro de UPLOAD_FOLDER
    """
    # VULN: open() directo con input de usuario sin sanitizar
    with open(filepath, "r") as f:
        return f.read()


def save_uploaded_file(filename: str, content: bytes) -> str:
    """
    Guarda un archivo subido por el usuario.

    VULN: Path Traversal — el filename puede contener ../
    Ejemplo de ataque: filename = "../../etc/cron.d/malicious"
    """
    upload_dir = "/tmp/uploads"
    # VULN: os.path.join no protege contra rutas absolutas ni ../
    full_path = os.path.join(upload_dir, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(content)
    return full_path


# ─── VULN: Template Injection (OWASP A03) ───────────────────────────────────

def render_user_template(template_content: str, **context) -> str:
    """
    Renderiza un template proporcionado por el usuario.

    VULN: Server-Side Template Injection (SSTI) — render_template_string con input de usuario
    Ejemplo de ataque: template_content = "{{ config.items() }}"
    Correcto: usar render_template() con archivos estáticos, nunca con input de usuario
    """
    # VULN: SSTI — el usuario controla el contenido del template
    return render_template_string(template_content, **context)


def generate_report(user_name: str, data: dict) -> str:
    """
    Genera un informe HTML con datos del usuario.

    VULN: XSS — el nombre del usuario se inyecta sin escapar en HTML
    VULN: SSTI — usa render_template_string
    """
    template = f"""
    <html>
    <body>
        <h1>Informe para {user_name}</h1>
        <pre>{{{{ data | tojson }}}}</pre>
    </body>
    </html>
    """
    return render_template_string(template, data=data)


# ─── VULN: Deserialización insegura (OWASP A08) ─────────────────────────────

def load_session_data(serialized_data: bytes) -> dict:
    """
    Carga datos de sesión serializados.

    VULN: pickle.loads() con datos no confiables = Ejecución Remota de Código (RCE)
    Correcto: usar json.loads() o un formato seguro
    """
    # VULN: Deserialización insegura — puede ejecutar código arbitrario
    return pickle.loads(serialized_data)


def load_config_from_yaml(yaml_content: str) -> dict:
    """
    Carga configuración desde YAML.

    VULN: yaml.load() sin Loader seguro permite ejecución de código
    Correcto: usar yaml.safe_load()
    """
    # VULN: yaml.load() sin SafeLoader
    return yaml.load(yaml_content)


# ─── VULN: eval() con input de usuario (OWASP A03) ──────────────────────────

def calculate_expression(expression: str) -> float:
    """
    Evalúa una expresión matemática.

    VULN: eval() con input de usuario = Ejecución de Código Arbitrario
    Ejemplo de ataque: expression = "__import__('os').system('rm -rf /')"
    Correcto: usar ast.literal_eval() o una librería de parsing matemático
    """
    # VULN: eval() directo con input de usuario
    return eval(expression)


def dynamic_filter(items: list, filter_expr: str) -> list:
    """
    Filtra una lista usando una expresión dinámica.

    VULN: eval() con input de usuario
    """
    # VULN: eval() con input controlado por el usuario
    return [item for item in items if eval(filter_expr)]
