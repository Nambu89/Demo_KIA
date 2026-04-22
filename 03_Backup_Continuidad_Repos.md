# Estrategia de Backup y Continuidad de Repositorios - KIA Iberia

## Principio: Regla 3-2-1

Mantener al menos **3 copias** de los datos, en **2 ubicaciones diferentes**, con **1 copia offsite**.

## Que se debe respaldar

No basta con clonar el codigo. Un backup completo de GitHub incluye:

| Elemento | Metodo | Frecuencia |
|----------|--------|------------|
| Codigo fuente + historial | `git clone --mirror` | Diario |
| Ramas y tags | Incluido en mirror clone | Diario |
| Issues y comentarios | GitHub API / herramienta de backup | Semanal |
| Pull Requests y reviews | GitHub API / herramienta de backup | Semanal |
| Wikis | `git clone` del wiki repo | Semanal |
| GitHub Actions workflows | Incluido en codigo | Diario |
| Secrets y variables | Documentacion manual (nunca en backup) | Manual |
| Branch protection rules | GitHub API export | Mensual |
| CODEOWNERS | Incluido en codigo | Diario |
| Webhooks config | GitHub API export | Mensual |
| LFS objects | `git lfs fetch --all` | Diario |

## Metodo 1: Mirror Clone Automatizado

El metodo mas basico y efectivo para el codigo:

```bash
#!/bin/bash
# backup_repos.sh - Script de backup de repositorios KIA

BACKUP_DIR="/backups/github/$(date +%Y%m%d)"
ORG="kia-iberia"
REPOS=$(gh repo list $ORG --json name -q '.[].name')

mkdir -p "$BACKUP_DIR"

for repo in $REPOS; do
    echo "Backing up $repo..."
    git clone --mirror "https://github.com/$ORG/$repo.git" \
        "$BACKUP_DIR/$repo.git"

    # Backup LFS si existe
    cd "$BACKUP_DIR/$repo.git"
    git lfs fetch --all 2>/dev/null
    cd -
done

echo "Backup completado: $BACKUP_DIR"
```

### Automatizacion con GitHub Actions

```yaml
name: Repository Backup
on:
  schedule:
    - cron: '0 2 * * *'  # Diario a las 2 AM
  workflow_dispatch:       # Manual

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Mirror clone
        run: |
          git clone --mirror https://github.com/${{ github.repository }}.git backup
      - name: Upload to Azure Blob Storage
        uses: azure/cli@v2
        with:
          inlineScript: |
            az storage blob upload-batch \
              --source backup \
              --destination ${{ secrets.AZURE_CONTAINER }} \
              --account-name ${{ secrets.AZURE_STORAGE_ACCOUNT }}
```

## Metodo 2: Herramientas de Backup Dedicadas

### Opcion A: GitHub Enterprise Backup Utilities (Self-Hosted)

Para GitHub Enterprise Server, GitHub proporciona `backup-utils`:

```bash
# Instalacion
git clone https://github.com/github/backup-utils.git
cd backup-utils

# Configuracion
cp backup.config-example backup.config
# Editar: GHE_HOSTNAME, GHE_DATA_DIR, GHE_NUM_SNAPSHOTS

# Ejecutar backup
bin/ghe-backup

# Restaurar
bin/ghe-restore
```

### Opcion B: Herramientas de terceros

Para GitHub Cloud (no self-hosted):

- **GitProtect.io**: Backup automatizado con cifrado AES, restauracion granular, cumplimiento normativo
- **Rewind Backups**: Backup continuo con restauracion por punto en el tiempo
- **BackHub**: Backup diario automatico a AWS S3

## Metodo 3: Mirroring a Azure DevOps (Recomendado para KIA)

Dado que KIA viene de Azure DevOps/TFS, mantener un mirror alli tiene sentido como estrategia de continuidad:

```yaml
# .github/workflows/mirror-to-azure.yml
name: Mirror to Azure DevOps

on:
  push:
    branches: [main, develop]

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Push mirror to Azure DevOps
        run: |
          git remote add azure https://$(AZURE_PAT)@dev.azure.com/kia-iberia/project/_git/repo
          git push azure --all --force
          git push azure --tags --force
        env:
          AZURE_PAT: ${{ secrets.AZURE_DEVOPS_PAT }}
```

## Plan de Continuidad (Disaster Recovery)

### Escenarios y respuesta

| Escenario | Impacto | RTO | RPO | Respuesta |
|-----------|---------|-----|-----|-----------|
| Eliminacion accidental de rama | Bajo | 5 min | 0 | Restaurar desde mirror local o reflog |
| Eliminacion de repositorio | Alto | 30 min | 24h | Restaurar desde backup diario |
| Caida de GitHub (global) | Critico | - | 0 | Trabajar sobre mirror Azure DevOps |
| Compromiso de seguridad | Critico | 1h | Ultimo backup limpio | Restaurar backup + rotar secrets |

- **RTO** (Recovery Time Objective): Tiempo maximo aceptable de recuperacion
- **RPO** (Recovery Point Objective): Perdida maxima de datos aceptable

### Procedimiento de restauracion

```bash
# 1. Desde mirror clone
git clone --mirror /backups/github/20260320/mi-repo.git
cd mi-repo.git
git remote set-url origin https://github.com/kia-iberia/mi-repo.git
git push origin --all
git push origin --tags

# 2. Desde Azure DevOps mirror
git clone https://dev.azure.com/kia-iberia/project/_git/mi-repo
cd mi-repo
git remote set-url origin https://github.com/kia-iberia/mi-repo.git
git push origin --all
```

## Verificacion de Backups

```yaml
# .github/workflows/verify-backup.yml
name: Verify Backup Integrity

on:
  schedule:
    - cron: '0 6 * * 1'  # Lunes a las 6 AM

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Clone from backup
        run: git clone --mirror $BACKUP_URL test-restore

      - name: Verify integrity
        run: |
          cd test-restore
          git fsck --full
          echo "Backup verificado correctamente"

      - name: Compare with origin
        run: |
          git clone --mirror https://github.com/${{ github.repository }}.git origin-copy
          diff <(cd test-restore && git log --oneline -20) \
               <(cd origin-copy && git log --oneline -20)
```

## Checklist de Implementacion

- [ ] Configurar script de mirror clone diario
- [ ] Configurar mirror a Azure DevOps para repos criticos
- [ ] Definir politica de retencion (30 dias minimo)
- [ ] Cifrar backups en reposo (AES-256)
- [ ] Almacenar backups en ubicacion geografica diferente
- [ ] Probar restauracion mensualmente
- [ ] Documentar procedimiento de DR
- [ ] Configurar alertas si el backup falla
- [ ] Incluir backup de metadata (issues, PRs, wikis)
- [ ] Revisar y actualizar plan cada 6 meses

---

*Consultoria de Adopcion GitHub - KIA Iberia | Devoteam 2026*
