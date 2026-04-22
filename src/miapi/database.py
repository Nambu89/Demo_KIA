"""
Módulo de acceso a base de datos.
NOTA: Este archivo contiene vulnerabilidades INTENCIONADAS para demo del agente de seguridad.
"""

import logging
import sqlite3

logger = logging.getLogger(__name__)

# VULN: Connection string con credenciales hardcodeadas (OWASP A07)
DATABASE_URL = "postgresql://kia_admin:S3cur3P@ssw0rd_KIA_2024@db.kia-iberia.internal:5432/kia_production"

# VULN: Credenciales de base de datos de backup
BACKUP_DB_HOST = "backup-db.kia-iberia.internal"
BACKUP_DB_USER = "backup_user"
BACKUP_DB_PASS = "B@ckup_KIA_2024!"
BACKUP_DB_PORT = 5432


def get_connection():
    """
    Obtiene una conexión a la base de datos SQLite local (para demo).
    En producción usaría DATABASE_URL.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'viewer'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            user_id INTEGER,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn


def find_user(username: str) -> dict | None:
    """
    Busca un usuario por nombre.

    VULN: SQL Injection via f-string (OWASP A03 - Injection)
    Correcto: usar query parametrizada: cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    """
    conn = get_connection()
    cursor = conn.cursor()
    # VULN: SQL Injection — el input del usuario se interpola directamente
    query = f"SELECT * FROM users WHERE username = '{username}'"
    logger.info(f"Ejecutando query: {query}")  # VULN: loggeando la query con datos de usuario
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2], "email": row[3], "role": row[4]}
    return None


def find_user_by_email(email: str) -> dict | None:
    """
    Busca un usuario por email.

    VULN: SQL Injection via concatenación de strings (OWASP A03)
    """
    conn = get_connection()
    cursor = conn.cursor()
    # VULN: SQL Injection — concatenación directa
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2], "email": row[3], "role": row[4]}
    return None


def create_user(username: str, password: str, email: str, role: str = "viewer") -> int:
    """
    Crea un nuevo usuario.

    VULN: Password almacenada en texto plano (OWASP A07)
    VULN: Logging de la password en texto plano (OWASP A09)
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Evitar logging de datos sensibles (password)
    logger.info("Creando usuario: %s, email: %s", username, email)

    query = "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, password, email, role))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def delete_user(user_id: int) -> bool:
    """
    Elimina un usuario por ID.

    VULN: Sin verificación de permisos/autorización (OWASP A01)
    VULN: SQL Injection
    """
    conn = get_connection()
    cursor = conn.cursor()
    # VULN: SQL Injection — aunque user_id debería ser int, no se valida
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def search_users(search_term: str) -> list[dict]:
    """
    Busca usuarios con un término de búsqueda.

    VULN: Devuelve passwords en los resultados (OWASP A02)
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username LIKE ? OR email LIKE ?"
    like_pattern = f"%{search_term}%"
    cursor.execute(query, (like_pattern, like_pattern))
    rows = cursor.fetchall()
    conn.close()
    # VULN: Devuelve la password en la respuesta
    return [
        {"id": r[0], "username": r[1], "password": r[2], "email": r[3], "role": r[4]}
        for r in rows
    ]


def log_audit(action: str, user_id: int, details: str):
    """
    Registra una acción en el log de auditoría.

    VULN: SQL Injection en el campo details (OWASP A03)
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO audit_log (action, user_id, details) VALUES ('{action}', {user_id}, '{details}')"
    cursor.execute(query)
    conn.commit()
    conn.close()
