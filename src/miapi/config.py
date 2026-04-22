"""
Configuración de la aplicación.
NOTA: Este archivo contiene vulnerabilidades INTENCIONADAS para demo del agente de seguridad.
"""

import os

# ─── VULN: API Keys y tokens hardcodeados (OWASP A07) ───────────────────────

# VULN: AWS Access Key hardcodeada
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "eu-west-1"

# VULN: GitHub Personal Access Token hardcodeado
GITHUB_TOKEN = "ghp_R4nd0mT0k3nV4lu3F0rD3m0Purp0s3sOnLy01"

# VULN: Slack Webhook URL hardcodeada
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T0EXAMPLE/B0EXAMPLE/xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# VULN: API key de servicio externo
EXTERNAL_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234"

# VULN: Clave privada RSA embebida en el código
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MhgHcTz6sE2I2yPB
aFDrBz9vFqU4nBa5PxUy5WPbRMeIRNYyKrFkLkOsSvPKzENLQYLEfHJhdiF/GYjZ
FakeKeyForDemoDoNotUseFakeKeyForDemoDoNotUseFakeKeyForDemo
FakeKeyForDemoDoNotUseFakeKeyForDemoDoNotUseFakeKeyForDemo
-----END RSA PRIVATE KEY-----"""


# ─── VULN: Configuración insegura (OWASP A05) ───────────────────────────────

class Config:
    """Configuración base de la aplicación."""

    # VULN: DEBUG = True en producción
    DEBUG = True
    TESTING = False

    # VULN: Secret key débil y hardcodeada
    SECRET_KEY = "desarrollo-kia-2024"

    # VULN: Sesiones sin expiración
    PERMANENT_SESSION_LIFETIME = 999999999

    # VULN: Base de datos con credenciales en la URL
    SQLALCHEMY_DATABASE_URI = "postgresql://kia_admin:S3cur3P@ssw0rd_KIA_2024@db.kia-iberia.internal:5432/kia_prod"

    # VULN: Token pasado como query param en URL (visible en logs del servidor)
    MONITORING_URL = f"https://monitoring.kia-iberia.internal/api/v1/health?token={GITHUB_TOKEN}"

    # VULN: Sin protección CSRF
    WTF_CSRF_ENABLED = False

    # Uploads
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
    UPLOAD_FOLDER = "/tmp/uploads"


class ProductionConfig(Config):
    """
    Configuración de producción.
    VULN: Hereda DEBUG = True de Config (debería ser False)
    VULN: Mismas credenciales que desarrollo
    """
    # Debería sobreescribir DEBUG = False pero no lo hace
    SQLALCHEMY_DATABASE_URI = "postgresql://kia_admin:S3cur3P@ssw0rd_KIA_2024@prod-db.kia-iberia.internal:5432/kia_prod"


class DevelopmentConfig(Config):
    """Configuración de desarrollo."""
    DEBUG = True
    TESTING = True


# VULN: Diccionario de configuración con la selección por defecto insegura
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,  # VULN: default apunta a desarrollo
}


def get_config(env: str | None = None) -> Config:
    """
    Obtiene la configuración según el entorno.

    VULN: Si no se especifica entorno, usa desarrollo (inseguro como default)
    """
    environment = env or os.environ.get("FLASK_ENV", "default")
    return config_map.get(environment, DevelopmentConfig)()


def get_external_api_url(endpoint: str) -> str:
    """
    Construye la URL para un servicio externo.

    VULN: Token en query params — visible en logs de servidor, historial del navegador, referer headers
    """
    base_url = "https://api.external-service.kia-iberia.com/v2"
    return f"{base_url}/{endpoint}?api_key={EXTERNAL_API_KEY}&region={AWS_REGION}"
