"""
Utilidades generales de la aplicación.
NOTA: Este archivo contiene vulnerabilidades INTENCIONADAS para demo del agente de seguridad.
"""

import os
import shlex
import subprocess
import pickle
import re
import yaml
import ast
import operator

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

    Corregido: evita command injection eliminando shell=True y validando
    el binario contra una allowlist.
    """
    if not command or not command.strip():
        return {"stdout": "", "stderr": "Comando vacío", "returncode": 1}

    try:
        args = shlex.split(command)
    except ValueError as e:
        return {"stdout": "", "stderr": f"Comando inválido: {e}", "returncode": 1}

    if not args:
        return {"stdout": "", "stderr": "Comando vacío", "returncode": 1}
def _is_valid_hostname(hostname: str) -> bool:
    allowed_commands = {"ls", "pwd", "whoami", "date", "echo"}
    Valida hostnames/IPv4/IPv6 simples para evitar inyección de comandos.
    """
    if not hostname or len(hostname) > 253:
        return False
    pattern = r"^[A-Za-z0-9][A-Za-z0-9\.\-:]{0,251}[A-Za-z0-9]$"
    return re.fullmatch(pattern, hostname) is not None
        return {

def ping_host(hostname: str) -> str:
            "returncode": 1,
    Hace ping a un host de forma segura.
    """
    if not _is_valid_hostname(hostname):
        return "Hostname inválido"


        ["ping", "-c", "1", hostname],
        shell=False,
        shell=False,
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

    El path recibido se resuelve dentro de un directorio permitido para
    evitar Path Traversal.
    """
    base_dir = os.path.realpath("/tmp/uploads")
    full_path = os.path.realpath(os.path.join(base_dir, filepath))

    if os.path.commonpath([base_dir, full_path]) != base_dir:
        raise ValueError("Ruta de archivo no permitida")

    with open(full_path, "r") as f:
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
    Renderiza contenido proporcionado por el usuario de forma segura.

    Seguridad: no interpreta el contenido como plantilla Jinja para evitar SSTI.
    Solo reemplaza placeholders literales de primer nivel: {{ key }} / {{key}}.
    """
    rendered = template_content
    for key, value in context.items():
        placeholder_spaced = "{{ " + str(key) + " }}"
        placeholder_compact = "{{" + str(key) + "}}"
        rendered = rendered.replace(placeholder_spaced, str(value))
        rendered = rendered.replace(placeholder_compact, str(value))
    return rendered


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

_SAFE_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}

_SAFE_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_math_ast(node):
    if isinstance(node, ast.Expression):
        return _evaluate_math_ast(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Solo se permiten números en la expresión")

    if isinstance(node, ast.Num):  # Compatibilidad con versiones antiguas de Python
        return node.n

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_BINARY_OPERATORS:
            raise ValueError("Operador no permitido")
        left = _evaluate_math_ast(node.left)
        right = _evaluate_math_ast(node.right)
        return _SAFE_BINARY_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_UNARY_OPERATORS:
            raise ValueError("Operador unario no permitido")
        operand = _evaluate_math_ast(node.operand)
        return _SAFE_UNARY_OPERATORS[op_type](operand)

    raise ValueError("Expresión no permitida")


def calculate_expression(expression: str) -> float:
    """
    Evalúa una expresión matemática de forma segura (sin ejecutar código arbitrario).

    Solo se permiten números y operadores aritméticos básicos.
    """
    parsed = ast.parse(expression, mode="eval")
    result = _evaluate_math_ast(parsed)
    return float(result)


def dynamic_filter(items: list, filter_expr: str) -> list:
    """
    Filtra una lista usando una expresión dinámica.

    VULN: eval() con input de usuario
    """
    # VULN: eval() con input controlado por el usuario
    return [item for item in items if eval(filter_expr)]
