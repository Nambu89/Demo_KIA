# KIA Iberia - Instrucciones para GitHub Copilot

## Descripcion del proyecto

Este repositorio contiene [DESCRIPCION DEL PROYECTO]. Es parte del ecosistema de aplicaciones de KIA Iberia.

## Stack tecnologico

- Lenguaje: [Python 3.12 / TypeScript 5.x / etc.]
- Framework: [FastAPI / Next.js / etc.]
- Base de datos: [PostgreSQL / MongoDB / etc.]
- Tests: [pytest / Jest / Vitest]
- CI/CD: GitHub Actions
- Contenedores: Docker

## Convenciones de codigo

### Naming
- Variables y funciones: snake_case (Python) / camelCase (TypeScript)
- Clases: PascalCase
- Constantes: UPPER_SNAKE_CASE
- Archivos: snake_case.py / kebab-case.ts

### Estructura
- Imports agrupados: stdlib, third-party, local (separados por linea en blanco)
- Funciones publicas con docstrings/JSDoc completos
- Type hints obligatorios en Python, tipos estrictos en TypeScript
- Maximo 50 lineas por funcion
- Maximo 300 lineas por archivo

### Formato
- Indentacion: 4 espacios (Python) / 2 espacios (TypeScript)
- Comillas: dobles para strings
- Trailing commas en listas multilinea
- Sin semicolons (TypeScript)

## Patrones de diseno

- Repository pattern para acceso a datos
- Dependency injection (FastAPI Depends / constructores en TS)
- DTOs con Pydantic models (Python) / Zod schemas (TypeScript)
- Error handling con excepciones tipadas, nunca retornar None para errores
- Logging estructurado con contexto (no print statements)

## Testing

- Framework: [pytest / Jest]
- Patron AAA: Arrange, Act, Assert
- Minimo un test por funcion publica
- Fixtures compartidas en conftest.py / setup files
- Mocks para servicios externos (APIs, DB)
- Nombres descriptivos: test_should_{comportamiento}_when_{condicion}

## Seguridad

- NUNCA hardcodear secrets, tokens o passwords
- Usar variables de entorno o GitHub Secrets
- Validar TODOS los inputs del usuario
- Sanitizar outputs para prevenir XSS/injection
- Usar parametrized queries para DB (nunca string concatenation)

## Que NO hacer

- No usar `any` en TypeScript
- No ignorar errores con try/except generico
- No dejar console.log o print de debug
- No commitear archivos .env o credenciales
- No crear funciones con mas de 5 parametros
- No usar variables globales mutables

## Estructura del proyecto

```
src/
  api/          # Endpoints y rutas
  services/     # Logica de negocio
  models/       # Modelos de datos
  repositories/ # Acceso a datos
  utils/        # Utilidades compartidas
tests/
  unit/         # Tests unitarios
  integration/  # Tests de integracion
  fixtures/     # Datos de prueba
docs/           # Documentacion
.github/
  workflows/    # CI/CD pipelines
  agents/       # Custom agents
```
