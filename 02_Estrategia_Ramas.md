# Estrategia de Ramas - Guia para KIA

## Modelo Recomendado: GitFlow Simplificado

Para KIA, recomendamos un GitFlow simplificado que balancea estructura con agilidad.

## Ramas Principales

### `main`
- Codigo en produccion
- Protegida: nadie puede hacer push directo
- Solo recibe merges via Pull Request
- Cada merge a main es potencialmente desplegable

### `develop`
- Rama de integracion
- Aqui se integran todas las features terminadas
- Base para crear ramas de feature
- CI corre en cada push

## Ramas de Trabajo

### `feature/*`
- Nomenclatura: `feature/KIA-{ticket}-{descripcion-corta}`
- Ejemplo: `feature/KIA-123-login-oauth2`
- Se crean desde: `develop`
- Se mergean a: `develop` (via PR)
- Vida maxima recomendada: 1-2 semanas

### `bugfix/*`
- Nomenclatura: `bugfix/KIA-{ticket}-{descripcion}`
- Ejemplo: `bugfix/KIA-456-fix-null-pointer`
- Se crean desde: `develop`
- Se mergean a: `develop` (via PR)

### `hotfix/*`
- Nomenclatura: `hotfix/KIA-{ticket}-{descripcion}`
- Ejemplo: `hotfix/KIA-789-security-patch`
- Se crean desde: `main` (caso urgente)
- Se mergean a: `main` Y `develop` (via PR)
- Solo para correcciones criticas en produccion

### `release/*`
- Nomenclatura: `release/v{version}`
- Ejemplo: `release/v2.1.0`
- Se crean desde: `develop`
- Se mergean a: `main` Y `develop`
- Para preparar una version: ultimos ajustes, bumps de version

## Flujo Visual

```
main     ──●─────────────────────●──────────●──
            \                   /            /
develop  ────●──●──●──●──●──●──●──●──●──●──●──
               \     /  \        /
feature/A       ●──●    \      /
                         \    /
feature/B                 ●──●
```

## Reglas de Proteccion (Branch Protection Rules)

### Para `main`:
- Require pull request reviews: minimo 1 reviewer
- Require status checks to pass: CI pipeline completo
- Require branches to be up to date: si
- Restrict who can push: solo admins (emergency)
- Require conversation resolution: si
- Require signed commits: recomendado

### Para `develop`:
- Require pull request reviews: minimo 1 reviewer
- Require status checks to pass: CI basico (lint + tests)
- Allow force pushes: no
- Allow deletions: no

## CODEOWNERS

Crear archivo `.github/CODEOWNERS`:

```
# Propietarios globales (revision por defecto)
* @kia-iberia/tech-leads

# Backend
/src/api/       @kia-iberia/backend-team
/src/services/  @kia-iberia/backend-team

# Frontend
/src/ui/        @kia-iberia/frontend-team
/src/components/ @kia-iberia/frontend-team

# Infraestructura y CI/CD
/.github/       @kia-iberia/devops-team
/infra/         @kia-iberia/devops-team
/Dockerfile     @kia-iberia/devops-team

# Documentacion
/docs/          @kia-iberia/tech-leads
*.md            @kia-iberia/tech-leads
```

## Estrategia de Merge

### Recomendacion: Squash and Merge

Para PRs de feature:
- **Squash and merge**: combina todos los commits del PR en uno solo
- Ventaja: historial de main limpio y legible
- Cada commit en main = un PR completado

Para hotfixes:
- **Merge commit**: mantener trazabilidad completa

### Configuracion en GitHub:
- Settings > General > Pull Requests
- Habilitar: "Allow squash merging" (default)
- Habilitar: "Allow merge commits" (para hotfixes)
- Deshabilitar: "Allow rebase merging" (evitar confusion)
- Activar: "Automatically delete head branches"

## Naming Convention Completa

| Tipo | Patron | Ejemplo |
|------|--------|---------|
| Feature | `feature/KIA-{id}-{desc}` | `feature/KIA-123-user-auth` |
| Bugfix | `bugfix/KIA-{id}-{desc}` | `bugfix/KIA-456-fix-timeout` |
| Hotfix | `hotfix/KIA-{id}-{desc}` | `hotfix/KIA-789-sec-patch` |
| Release | `release/v{major}.{minor}.{patch}` | `release/v2.1.0` |
| Docs | `docs/KIA-{id}-{desc}` | `docs/KIA-321-api-guide` |

## Checklist de Implementacion

- [ ] Configurar branch protection en `main`
- [ ] Configurar branch protection en `develop`
- [ ] Crear archivo `.github/CODEOWNERS`
- [ ] Configurar merge strategies permitidas
- [ ] Activar auto-delete de ramas mergeadas
- [ ] Documentar naming convention en el README del repo
- [ ] Crear labels estandar para PRs (feature, bugfix, hotfix, docs)
- [ ] Configurar template de PR (ver guia de templates)

---

*Consultoria de Adopcion GitHub - KIA Iberia | Devoteam 2026*
