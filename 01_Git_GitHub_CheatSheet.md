# Git & GitHub CLI - Cheat Sheet para KIA

## Configuracion Inicial

```bash
# Configurar identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@kia.com"

# Configurar editor por defecto
git config --global core.editor "code --wait"

# Ver configuracion actual
git config --list
```

## Comandos Basicos de Git

### Repositorio

| Comando | Descripcion |
|---------|-------------|
| `git clone <url>` | Clonar un repositorio remoto |
| `git init` | Inicializar un repo local nuevo |
| `git status` | Ver estado actual (archivos modificados, staged, etc.) |
| `git log --oneline -10` | Ver ultimos 10 commits en formato compacto |
| `git log --graph --oneline --all` | Ver historial con ramas visuales |

### Ramas

| Comando | Descripcion |
|---------|-------------|
| `git branch` | Listar ramas locales |
| `git branch -a` | Listar todas las ramas (locales + remotas) |
| `git checkout -b feature/mi-feature` | Crear y cambiar a nueva rama |
| `git switch feature/mi-feature` | Cambiar a una rama existente |
| `git branch -d feature/mi-feature` | Eliminar rama local (ya mergeada) |

### Flujo de Trabajo Diario

```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama de feature
git checkout -b feature/KIA-123-nueva-funcionalidad

# 3. Trabajar y hacer commits
git add archivo_modificado.py
git commit -m "feat(api): añadir endpoint de validacion KIA-123"

# 4. Subir rama al remoto
git push -u origin feature/KIA-123-nueva-funcionalidad

# 5. Abrir PR en GitHub (ver seccion GitHub CLI)

# 6. Despues del merge, limpiar
git checkout main
git pull origin main
git branch -d feature/KIA-123-nueva-funcionalidad
```

### Staging y Commits

| Comando | Descripcion |
|---------|-------------|
| `git add <archivo>` | Añadir archivo al staging |
| `git add -p` | Añadir cambios interactivamente (por hunks) |
| `git commit -m "mensaje"` | Hacer commit con mensaje |
| `git commit --amend` | Modificar ultimo commit (mensaje o archivos) |
| `git stash` | Guardar cambios temporalmente |
| `git stash pop` | Recuperar cambios guardados |

### Sincronizacion

| Comando | Descripcion |
|---------|-------------|
| `git fetch origin` | Traer cambios del remoto sin aplicar |
| `git pull origin main` | Traer y aplicar cambios de main |
| `git push origin <rama>` | Subir commits al remoto |
| `git pull --rebase origin main` | Rebase en vez de merge al traer cambios |

### Resolver Conflictos

```bash
# 1. Al hacer pull/merge y hay conflictos:
git status  # Ver archivos en conflicto

# 2. Editar archivos (buscar marcadores <<<<<<<)
# Resolver manualmente o con el editor

# 3. Marcar como resuelto
git add <archivo_resuelto>

# 4. Continuar merge/rebase
git merge --continue  # o git rebase --continue

# 5. Si quieres abortar
git merge --abort  # o git rebase --abort
```

## GitHub CLI (gh)

### Instalacion

```bash
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh  # Debian/Ubuntu
```

### Autenticacion

```bash
gh auth login  # Login interactivo
gh auth status # Ver estado de autenticacion
```

### Pull Requests

| Comando | Descripcion |
|---------|-------------|
| `gh pr create --fill` | Crear PR con info del commit |
| `gh pr create --title "feat: ..." --body "..."` | Crear PR con titulo y cuerpo |
| `gh pr list` | Listar PRs abiertos |
| `gh pr view 123` | Ver detalle de PR #123 |
| `gh pr checkout 123` | Hacer checkout de PR #123 |
| `gh pr review 123 --approve` | Aprobar PR |
| `gh pr merge 123 --squash` | Merge con squash |
| `gh pr diff 123` | Ver diff de PR |

### Issues

| Comando | Descripcion |
|---------|-------------|
| `gh issue create --title "bug: ..."` | Crear issue |
| `gh issue list` | Listar issues abiertos |
| `gh issue view 456` | Ver detalle de issue |
| `gh issue close 456` | Cerrar issue |

### Repositorio

| Comando | Descripcion |
|---------|-------------|
| `gh repo clone org/repo` | Clonar repo |
| `gh repo view --web` | Abrir repo en el navegador |
| `gh run list` | Ver runs de GitHub Actions |
| `gh run view 789` | Ver detalle de un workflow run |
| `gh run watch 789` | Ver logs en tiempo real |

## Convencion de Commits (Conventional Commits)

```
<tipo>(<scope>): <descripcion corta>

Tipos:
  feat:     Nueva funcionalidad
  fix:      Correccion de bug
  docs:     Cambios en documentacion
  style:    Formato (no afecta logica)
  refactor: Refactorizacion de codigo
  test:     Añadir o modificar tests
  chore:    Tareas de mantenimiento
  ci:       Cambios en CI/CD

Ejemplos:
  feat(auth): añadir autenticacion con OAuth2
  fix(api): corregir timeout en endpoint /users
  docs(readme): actualizar instrucciones de instalacion
  ci(actions): añadir step de security scan al pipeline
```

## Atajos Utiles

```bash
# Alias recomendados
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

---

*Consultoria de Adopcion GitHub - KIA Iberia | Devoteam 2026*
