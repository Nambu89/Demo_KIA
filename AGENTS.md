# Instrucciones del proyecto para agentes

> Este archivo define las reglas y el contexto que todos los agentes deben seguir al trabajar en este repositorio. Los agentes lo leen automáticamente antes de cada tarea.

## Stack tecnológico

- **Lenguaje**: <!-- Ej: C#, TypeScript, Python, Java, Go -->
- **Framework**: <!-- Ej: ASP.NET Core 8, React 18, FastAPI, Spring Boot -->
- **Base de datos**: <!-- Ej: PostgreSQL, SQL Server, MongoDB, MySQL -->
- **ORM / Data access**: <!-- Ej: Entity Framework Core, Prisma, SQLAlchemy, Hibernate -->
- **Tests**: <!-- Ej: xUnit + FluentAssertions + Moq, Jest, pytest, JUnit + Mockito -->
- **CI/CD**: GitHub Actions
- **Contenedores**: <!-- Ej: Docker, Docker Compose, Kubernetes, ninguno -->
- **Cloud**: <!-- Ej: Azure, AWS, GCP, on-premise, ninguno -->

## Estructura del proyecto

```
├── src/                    # Código fuente principal
├── tests/                  # Tests unitarios y de integración
├── docs/                   # Documentación técnica
├── .github/
│   ├── workflows/          # Pipelines de CI/CD
│   └── agents/             # Agentes custom (si hay locales)
├── AGENTS.md               # Este archivo
└── README.md
```

<!-- Adapta el árbol a la estructura real de tu repositorio -->

## Convenciones de código

### General
- Idioma del código: <!-- Ej: inglés, español -->
- Idioma de commits y PRs: <!-- Ej: español con Conventional Commits (feat:, fix:, docs:) -->
- Idioma de documentación: <!-- Ej: español -->

### Naming
- Clases y métodos: PascalCase
- Variables y parámetros: camelCase
- Constantes: UPPER_SNAKE_CASE
- Archivos de test: <!-- Ej: *Test.cs, *.test.ts, test_*.py, *_test.go -->

### Testing
- Patrón AAA obligatorio (Arrange, Act, Assert)
- Nombres de tests descriptivos que expliquen qué verifican
- Mínimo 3 tests por función pública: caso básico, edge case, error handling
- Mocking solo para dependencias externas (APIs, DB, filesystem)
- NO mockear el sistema bajo test (SUT)
- Tests independientes: sin orden de ejecución, sin estado compartido

### Estilo
- Seguir la configuración del linter/formatter del proyecto
- <!-- Ej: Prettier + ESLint, Black + Ruff, dotnet format, gofmt -->

## Variables de entorno

- Las variables de entorno se documentan en `.env.example` (o `appsettings.Development.json` para .NET)
- NUNCA exponer valores reales de secretos en código, documentación, ni commits
- Nuevas variables deben agregarse a `.env.example` con un valor ficticio
- Formato de documentación de variables:

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `DATABASE_URL` | Connection string de la BD | Sí | `postgresql://user:pass@localhost:5432/mydb` |
| `API_KEY` | Clave del servicio externo | Sí | `your-api-key-here` |

## Reglas de seguridad

- No hardcodear connection strings, API keys, passwords, ni URLs de producción
- No commitear archivos `.env`, certificados, ni claves privadas
- Usar `${{ secrets.X }}` en GitHub Actions, nunca valores en texto plano
- Si se detecta un posible secreto en el código, ALERTAR inmediatamente

## Reglas de documentación

- Todo cambio significativo debe reflejarse en el CHANGELOG.md
- Los endpoints de API nuevos deben documentarse con ejemplo de request/response
- Los PRs deben incluir descripción de qué se cambió y por qué
- No generar documentación vacía o placeholder ("TODO: completar")

## Reglas de CI/CD

- Todo PR debe pasar: lint, tests, build antes de merge
- Usar `concurrency` nativo de GitHub Actions para cancelar runs redundantes
- Branch protection en main: mínimo 1 review, status checks requeridos
- Los deploys a producción requieren aprobación manual

## Lo que los agentes NO deben hacer

- No sobreescribir documentación manual sin confirmación
- No generar tests triviales solo para inflar métricas de cobertura
- No modificar archivos de configuración de CI/CD sin confirmación
- No hacer cambios que rompan la compatibilidad sin documentar
- No asumir el stack — verificar los archivos del proyecto primero
- No inventar convenciones propias si el proyecto ya tiene las suyas
