# Instrucciones de Code Review — Seguridad (KIA Iberia)

Al revisar código en este repositorio, prioriza los siguientes controles de seguridad según OWASP Top 10.

## Severidad CRÍTICA — Bloquear merge

- **Secretos expuestos**: Detectar API keys, tokens, passwords, connection strings o claves privadas hardcodeadas en el código. Patrones: `password\s*=\s*["']`, `api[_-]?key\s*=\s*["']`, `ghp_`, `AKIA`, `sk-`, `-----BEGIN.*PRIVATE KEY-----`.
- **SQL Injection**: Queries construidas con f-strings, concatenación (`+`) o `.format()`. Exigir queries parametrizadas o uso de ORM.
- **Command Injection**: Uso de `os.system()`, `subprocess.run(shell=True)`, o `subprocess.Popen(shell=True)` con input de usuario.
- **Deserialización insegura**: `pickle.loads()`, `yaml.load()` sin `Loader=SafeLoader`, `eval()`, `exec()` con datos no confiables.
- **Archivos .env commiteados**: Cualquier archivo `.env` con credenciales que no debería estar en el repositorio.

## Severidad ALTA — Requiere corrección

- **Autenticación ausente**: Endpoints que manejan datos sensibles sin decoradores de autenticación (`@login_required`, middleware de auth).
- **Passwords en texto plano**: Comparación directa de passwords sin hashing. Exigir bcrypt, argon2 o scrypt.
- **Hashing débil**: Uso de MD5 o SHA1 para passwords o tokens de autenticación.
- **Path Traversal**: `open(user_input)` o `os.path.join()` sin validar que la ruta está dentro del directorio permitido.
- **SSTI (Server-Side Template Injection)**: `render_template_string()` con contenido controlado por el usuario.
- **XSS**: Output sin escapar en templates HTML.
- **Dependencias vulnerables**: Versiones de librerías con CVEs conocidos.

## Severidad MEDIA — Recomendar corrección

- **CORS permisivo**: `Access-Control-Allow-Origin: *` en producción.
- **DEBUG en producción**: `DEBUG = True` o `FLASK_DEBUG=1` en configuración de producción.
- **Cookies inseguras**: Cookies sin flags `HttpOnly`, `Secure`, `SameSite`.
- **Logging de datos sensibles**: Passwords, tokens o datos personales en logs.
- **CSRF deshabilitado**: `WTF_CSRF_ENABLED = False` sin justificación.
- **Tokens en URLs**: Tokens o API keys pasados como query params (visibles en logs y referer).
- **Sin rate limiting**: Endpoints de autenticación sin protección contra fuerza bruta.

## Severidad BAJA — Sugerir mejora

- **Error handling excesivo**: Respuestas de error que exponen stack traces o detalles internos.
- **Sesiones sin expiración**: Tokens o sesiones con TTL excesivo o sin expiración.
- **Permisos excesivos**: Workflows de GitHub Actions con `permissions: write-all`.

## Formato de los comentarios

Para cada hallazgo, incluir:
1. Severidad (CRÍTICA/ALTA/MEDIA/BAJA)
2. Categoría OWASP (A01-A10)
3. Descripción del riesgo
4. Código corregido como sugerencia
