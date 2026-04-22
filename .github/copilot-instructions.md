# KIA Iberia - Instrucciones para GitHub Copilot

## Descripcion del proyecto

Este repositorio contiene una API Flask para detección de presencia mediante análisis de imágenes. Es parte del ecosistema de aplicaciones de KIA Iberia.

## Stack tecnologico

- Lenguaje: Python 3.12
- Framework: Flask 3.0
- Base de datos: SQLite (demo) / PostgreSQL (producción)
- Tests: pytest + pytest-cov
- CI/CD: GitHub Actions
- Contenedores: Docker

## Convenciones de codigo

### Naming
- Variables y funciones: snake_case
- Clases: PascalCase
- Constantes: UPPER_SNAKE_CASE
- Archivos: snake_case.py

### Estructura
- Imports agrupados: stdlib, third-party, local (separados por linea en blanco)
- Funciones publicas con docstrings completos
- Type hints obligatorios en Python
- Maximo 50 lineas por funcion
- Maximo 300 lineas por archivo

### Formato
- Indentacion: 4 espacios
- Comillas: dobles para strings
- Trailing commas en listas multilinea
- Linter: Ruff

## Patrones de diseno

- Repository pattern para acceso a datos
- Dependency injection (Flask app factory pattern)
- Dataclasses para modelos de datos
- Error handling con excepciones tipadas, nunca retornar None para errores
- Logging estructurado con contexto (no print statements)

## Testing

- Framework: pytest
- Patron AAA: Arrange, Act, Assert
- Minimo 3 tests por funcion publica: caso basico, edge case, error handling
- Fixtures compartidas en conftest.py
- Mocks solo para dependencias externas (APIs, DB, filesystem)
- Nombres descriptivos en español

## Seguridad

- NUNCA hardcodear secrets, tokens o passwords
- Usar variables de entorno o GitHub Secrets
- Validar TODOS los inputs del usuario
- Sanitizar outputs para prevenir XSS/injection
- Usar parametrized queries para DB (nunca string concatenation)
- Passwords hasheadas con bcrypt o argon2
- Cookies con flags HttpOnly, Secure, SameSite

## Que NO hacer

- No ignorar errores con try/except generico
- No dejar print de debug
- No commitear archivos .env o credenciales
- No crear funciones con mas de 5 parametros
- No usar variables globales mutables
- No usar eval(), exec() ni os.system() con input de usuario
- No usar pickle.loads() con datos no confiables

## Estructura del proyecto

```
src/
  miapi/        # Código fuente principal
    app.py      # Flask app factory
    detector.py # Lógica de detección
    auth.py     # Autenticación
    database.py # Acceso a datos
    config.py   # Configuración
    utils.py    # Utilidades
test/           # Tests unitarios
docs/           # Documentación
.github/
  workflows/    # CI/CD pipelines
  agents/       # Custom agents
```
