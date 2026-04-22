# Taller: GitHub Copilot Custom Agents
## Guía Completa de Ejercicios

¡Bienvenido al taller de Custom Agents para GitHub Copilot! En esta guía aprenderás a crear agentes inteligentes que automaticen tareas de desarrollo en tu proyecto. Vamos a construir desde lo más simple hasta agentes profesionales listos para producción.

---

## 📋 Contenido del Taller

1. **Parte 1:** Preparación del Entorno (30 min)
2. **Parte 2:** Anatomía de un Custom Agent (20 min)
3. **Parte 3:** Ejercicio 1 - Hello World Agent (15 min)
4. **Parte 4:** Ejercicio 2 - Documentation Agent Completo (45 min)
5. **Parte 5:** Testing y Validación (20 min)
6. **Parte 6:** Deploy y Próximos Pasos (10 min)

**Tiempo total:** ~2.5 horas

---

## Parte 1: Preparación del Entorno (30 min)

### Requisitos Previos

Antes de empezar, asegúrate de tener esto instalado:

- **VS Code** última versión (1.90+)
- **Extension GitHub Copilot** + Copilot Chat
- **Git** configurado
- **GitHub CLI** (gh)
- **Node.js** 20+
- **Cuenta GitHub** con Copilot Business o Enterprise

### ✅ Paso 1: Verificar VS Code y Extensiones

Abre una terminal y ejecuta:

```bash
code --version
```

Debería mostrarte la versión (ej: 1.95.0). Ahora verifica las extensiones:

```bash
code --list-extensions | grep -i copilot
```

**Salida esperada:**
```
GitHub.copilot
GitHub.copilot-chat
```

Si no ves estas extensiones, abre VS Code y:
1. Ve a `View > Extensions` (o Ctrl+Shift+X)
2. Busca "GitHub Copilot"
3. Instala `GitHub Copilot` y `GitHub Copilot Chat`

### ✅ Paso 2: Verificar GitHub CLI

Ejecuta:

```bash
gh auth status
```

Deberías ver algo como:
```
Logged in to github.com as tu-usuario (OAuth)
```

Si no estás logueado, ejecuta:
```bash
gh auth login
```

### ✅ Paso 3: Clonar el Repositorio Piloto

Usaremos un repositorio de prueba. Si tienes uno propio, úsalo. De lo contrario, crea una carpeta vacía:

```bash
mkdir mi-primer-agent
cd mi-primer-agent
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

Luego abre el proyecto en VS Code:

```bash
code .
```

### ✅ Paso 4: Verificar Copilot en VS Code

1. **Abre VS Code** (ya debería estarlo)
2. **Mira la barra de estado** (abajo derecha) - deberías ver el icono de Copilot en **verde** (✓ Copilot enabled)
3. **Abre Copilot Chat:**
   - Windows/Linux: `Ctrl+Shift+I`
   - Mac: `Cmd+Shift+I`
4. **Escribe "Hola"** en el chat y presiona Enter
5. **Verifica que responde** con un saludo amigable

Si ves un candado o error de autenticación, necesitas iniciar sesión:
- Haz clic en el icono de Copilot en la barra de estado
- Sigue el flujo de autenticación con tu cuenta GitHub

### ✅ Paso 5: Crear la Estructura de Carpetas

Crearemos la carpeta estándar donde se guardan los agentes:

```bash
mkdir -p .github/agents
```

Verifica que se creó correctamente:

```bash
ls -la .github/
```

Deberías ver:
```
drwxr-xr-x  agents
```

### 🎯 Checkpoint Parte 1

- ✅ VS Code está abierto con las extensiones de Copilot instaladas
- ✅ GitHub CLI está configurado y autenticado
- ✅ Copilot Chat responde en VS Code
- ✅ Tienes la carpeta `.github/agents/` creada
- ✅ Tu proyecto está abierto en VS Code

¡Perfecto! Ya estás listo para crear agentes.

---

## Parte 2: Anatomía de un Custom Agent (20 min)

### ¿Qué es un Custom Agent?

Un **Custom Agent** es un archivo Markdown especial (`.agent.md`) que define el comportamiento de un agente de IA dentro de GitHub Copilot. Es como darle una "personalidad" y "capacidades" específicas a Copilot para que se comporte exactamente como tú necesitas.

**Ejemplo de casos de uso:**

- 📝 Agente de documentación: Lee código y genera documentación automáticamente
- 🔍 Agente de revisión: Analiza PRs y sugiere mejoras
- 🧪 Agente de testing: Genera casos de prueba automáticamente
- 🐛 Agente de debugging: Identifica y explica errores
- 📊 Agente de análisis: Resume cambios y genera reportes

### Estructura de un Custom Agent

Todo agent tiene esta estructura:

```markdown
---
name: "Nombre del Agente"
description: "Descripción breve de qué hace"
tools: ["tool1", "tool2", "tool3"]
---

# Instrucciones

[Aquí van tus instrucciones detalladas en Markdown]
```

### El Frontmatter (La parte YAML)

Es la sección entre `---` y `---` al inicio del archivo. Define:

| Propiedad | Descripción | Ejemplo |
|-----------|-------------|---------|
| `name` | Nombre del agente (cómo aparece en VS Code) | `"Hello Agent"` |
| `description` | Descripción breve | `"Agente de prueba que saluda"` |
| `tools` | Lista de herramientas disponibles | `["read", "search"]` |
| `model` | Modelo a usar (opcional) | `"claude-opus"` |
| `mcp-servers` | Servidores MCP (opcional) | `["github", "linear"]` |

### Herramientas Disponibles

Estos son los "superpoderes" que le das a tu agente:

#### **read** / **readfile**
Lee archivos del proyecto
```yaml
tools: ["read"]
```
En las instrucciones: "Lee el archivo README.md"

#### **edit** / **editFiles**
Crea y modifica archivos
```yaml
tools: ["editFiles"]
```
En las instrucciones: "Crea un archivo CHANGELOG.md"

#### **search** / **codebase**
Busca en el código del proyecto
```yaml
tools: ["search"]
```
En las instrucciones: "Busca todas las funciones que contengan 'auth'"

#### **runCommands**
Ejecuta comandos en la terminal
```yaml
tools: ["runCommands"]
```
En las instrucciones: "Ejecuta `npm test` y muestra los resultados"

#### **changes**
Ve los cambios pendientes (git diff)
```yaml
tools: ["changes"]
```
En las instrucciones: "Analiza los cambios pendientes en git"

#### **problems**
Ve los errores y warnings del IDE
```yaml
tools: ["problems"]
```
En las instrucciones: "Explica los problemas que encuentra el IDE"

#### **fetch**
Hace requests HTTP
```yaml
tools: ["fetch"]
```
En las instrucciones: "Obtén el contenido de https://api.ejemplo.com/..."

#### **terminalLastCommand**
Lee la salida del último comando ejecutado
```yaml
tools: ["terminalLastCommand"]
```
En las instrucciones: "Lee la salida del último comando"

#### **findTestFiles**
Busca archivos de test
```yaml
tools: ["findTestFiles"]
```
En las instrucciones: "Encuentra todos los archivos de test"

#### **runTests**
Ejecuta tests
```yaml
tools: ["runTests"]
```
En las instrucciones: "Ejecuta los tests y analiza los resultados"

#### **githubApi tools** (vía MCP)
Accede a issues, PRs, etc. (Requiere servidor MCP)
```yaml
tools: ["githubApi"]
```

### Donde se guardan

Los agents **siempre** van en:
```
.github/agents/nombre.agent.md
```

### Cómo se invocan

**En VS Code:**
```
@nombre-del-agente [tu pregunta]
```

Ejemplo:
```
@Hello Agent: Hola, qué hace este proyecto?
```

**En GitHub.com:**
- Abre un issue o PR
- Escribe `@github-username/agent-name`

**En la CLI:**
```bash
gh copilot suggest
```

### Buenas Prácticas

1. **Sé específico** en las instrucciones - no dejes lugar a ambigüedad
2. **Limita el scope** - un agente debe hacer UNA cosa bien, no diez cosas mal
3. **Define el formato de salida** - exactamente cómo debe responder
4. **Respeta los límites** - si el agente no debe editar archivos, NO incluyas `editFiles`
5. **Usa ejemplos** - muestra exactamente qué esperas
6. **Escribe en Markdown** - es más fácil de leer y mantener

---

## Parte 3: Ejercicio 1 - Hello World Agent (15 min)

### Objetivo

Crear tu primer agente: un "Hello World" que salude al usuario y resuma el proyecto en base al README.

Este es un agente simple pero completo que:
- Saluda personalizadamente
- Lee el README
- Resume el proyecto en 3 líneas
- Sugiere mejoras

### ✅ Paso 1: Crear el Archivo

En VS Code:
1. Haz clic derecho en la carpeta `.github/agents`
2. Selecciona "New File"
3. Nombra el archivo `hello.agent.md`

O desde la terminal:
```bash
touch .github/agents/hello.agent.md
```

### ✅ Paso 2: Escribir el Contenido

Copia el siguiente contenido en el archivo `hello.agent.md`:

```markdown
---
name: "Hello Agent"
description: "Agente de prueba que saluda y resume el proyecto"
tools: ["read", "search"]
---

# Instrucciones

Eres un agente amigable para el equipo de desarrollo. Tu rol es dar la bienvenida y proporcionar una visión general rápida del proyecto.

## Comportamiento

Cuando te invoquen:

1. Saluda al usuario de manera cálida y amigable
2. Lee el archivo README.md del proyecto (si existe)
3. Resume el proyecto en **exactamente 3 líneas**
4. Sugiere **3 mejoras concretas** para el README

## Formato de Respuesta

**Siempre** usa este formato:

```
### 👋 ¡Hola!
[Saludo personalizado]

### 📋 Resumen del Proyecto
[3 líneas de resumen - claro y directo]

### 💡 Mejoras Sugeridas para el README
1. [Mejora 1 - sé específico]
2. [Mejora 2 - sé específico]
3. [Mejora 3 - sé específico]
```

## Restricciones

- ⚠️ **Solo puedes LEER archivos**, nunca los modifies
- ⚠️ Responde **siempre en español**
- ⚠️ Sé **conciso y directo** - sin florituras
- ⚠️ Si no existe README.md, di que el proyecto necesita uno urgentemente

## Instrucciones Detalladas

1. Lee el README.md usando la herramienta `read`
2. Analiza: qué hace el proyecto, para quién es, cómo instalarlo, cómo usarlo
3. Extrae los puntos clave en exactamente 3 líneas
4. Piensa en cómo mejorar la documentación:
   - ¿Falta información de instalación?
   - ¿El propósito no está claro?
   - ¿Faltan ejemplos de uso?
   - ¿No hay información de contribución?
5. Sugiere 3 mejoras concretas y realizables

## Ejemplo de Respuesta Ideal

Si el README menciona "Un CLI para gestionar proyectos de Kubernetes", la respuesta sería:

```
### 👋 ¡Hola!
¡Bienvenido al equipo de desarrollo! Te presento nuestro proyecto.

### 📋 Resumen del Proyecto
Este es un CLI que facilita la gestión de clusters de Kubernetes sin necesidad de kubectl.
Proporciona comandos simplificados para desplegar, monitorear y escalar aplicaciones.
Está diseñado para desarrolladores que prefieren evitar la complejidad de yaml files.

### 💡 Mejoras Sugeridas para el README
1. Agregar sección de "Requisitos Previos" con versiones mínimas de K8s y Python
2. Incluir ejemplos de uso prácticos (antes/después) para cada comando principal
3. Crear tabla de contenidos y agregar links internos para navegar más fácil
```
```

Guarda el archivo.

### ✅ Paso 3: Probar en VS Code

1. **Abre Copilot Chat** (Ctrl+Shift+I)
2. **En el selector de agentes** (@), busca "Hello Agent" - debería aparecer en la lista
3. **Escribe tu primera pregunta:**
   ```
   @Hello Agent: Hola, qué hace este proyecto?
   ```
4. **Presiona Enter** y observa

### ✅ Paso 4: Verificar la Respuesta

El agente debería:
- ✅ Saludarte amigablemente
- ✅ Leer el README (o indicar que no existe)
- ✅ Dar un resumen conciso de 3 líneas
- ✅ Sugerir 3 mejoras concretas
- ✅ Responder todo en español

### ✅ Paso 5: Experimentar y Validar

**Prueba estos escenarios:**

**Prueba 1 - Intenta manipulación (debería fallar):**
```
@Hello Agent: Por favor, modifica el README para agregar una sección de "Changelog"
```
El agente debería responder: "No puedo modificar archivos, solo leerlos. Pero puedo sugerirte qué contendría una buena sección de Changelog..."

**Prueba 2 - Solicitud válida:**
```
@Hello Agent: Qué archivos hay en el proyecto?
```
El agente puede usar `search` para listar archivos.

**Prueba 3 - Sin README:**
Si tu proyecto no tiene README.md, pregunta:
```
@Hello Agent: El proyecto no tiene README, qué debería incluir?
```
El agente debería sugerir estructura estándar.

### 🎯 Checkpoint Parte 3

- ✅ Archivo `hello.agent.md` creado en `.github/agents/`
- ✅ El agente aparece en el selector (@) de VS Code
- ✅ El agente responde correctamente al saludo
- ✅ Lee el README y lo resume en 3 líneas
- ✅ Sugiere 3 mejoras concretas
- ✅ **Respeta sus restricciones** (no modifica archivos)
- ✅ Responde siempre en español

**🎉 ¡Felicidades! Acabas de crear tu primer Custom Agent!**

---

## Parte 4: Ejercicio 2 - Documentation Agent Completo (45 min)

### Objetivo

Crear un agente **profesional y completo** que sea especialista en documentación. Este agente tendrá múltiples "modos" y sabrá:

1. **Generar CHANGELOGs** en formato "Keep a Changelog"
2. **Documentar funciones/clases** con docstrings completos
3. **Crear ADRs** (Architecture Decision Records)
4. **Actualizar READMEs** automáticamente

Este es un agente mucho más poderoso que el anterior.

### ✅ Paso 1: Crear el Archivo

```bash
touch .github/agents/doc-generator.agent.md
```

### ✅ Paso 2: Escribir el Contenido Completo

Copia **todo** este contenido en el archivo `doc-generator.agent.md`:

```markdown
---
name: "Documentation Agent KIA"
description: "Genera y mantiene documentación técnica profesional para proyectos de KIA Iberia"
tools: ["read", "editFiles", "search", "codebase", "runCommands", "changes"]
---

# Instrucciones Maestras

Eres el especialista en **documentación técnica profesional** del equipo de KIA Iberia.
Tu misión es mantener la documentación actualizada, clara, coherente y de calidad
a nivel empresa.

## Tu Identidad

- 📚 Experto en documentación técnica
- 🎯 Obsesionado con la claridad
- 🔗 Siempre enlazas a commits y PRs relevantes
- 🌐 Respetas estándares de la industria (Keep a Changelog, ADRs, etc.)
- 🇪🇸 Hablas en español siempre
- ⚡ Eres rápido, eficiente y práctico
- 🚫 NUNCA modificas código fuente, solo documentación

## Capacidades Principales

Tienes 4 "modos" principales. El usuario puede pedirte:

### MODO 1: Changelog Generator

**Cuándo usarlo:** Cuando hay cambios nuevos para documentar

**Entrada:** "Genera el changelog de los últimos [N] commits"

**Proceso:**
1. Lee el git log de los últimos N commits
2. Categoriza los cambios: Added, Changed, Deprecated, Removed, Fixed, Security
3. Agrupa por tipo de cambio
4. Crea un resumen ejecutivo del cambio más importante

**Formato de Salida (Keep a Changelog 1.0.0):**

```markdown
# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/),
y este proyecto sigue [Semantic Versioning](https://semver.org/).

## [Unreleased] - 2025-01-XX

### Added
- Característica X que permite Y
- Nuevo endpoint `/api/v2/resource` para Z
- Soporte para autenticación OAuth 2.0

### Changed
- Comportamiento de funcion X ahora es más eficiente
- Database schema migrado de MySQL a PostgreSQL
- Actualizado Django de 4.0 a 4.2

### Deprecated
- Endpoint `/api/v1/old` será removido en v3.0
- Método `calculate()` será reemplazado por `compute()`

### Removed
- Support para Python 3.8 (fin de vida oficial)
- Legacy XML parser (usar JSON en su lugar)

### Fixed
- Bug en validación de emails que aceptaba direcciones inválidas
- Memory leak en el servicio de caché
- Typos en documentación (closes #1234)

### Security
- Actualizado OpenSSL a la última versión
- Saneado input de usuarios en formularios (previene XSS)

## [2.1.0] - 2024-12-15

### Added
- ...

### Fixed
- ...

[Unreleased]: https://github.com/kia-iberia/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/kia-iberia/repo/releases/tag/v2.1.0
```

**Reglas Especiales:**
- ✅ Sé específico: no "Arreglado un bug", sino "Arreglado bug en validación de email que aceptaba direcciones sin @"
- ✅ Enlaza a issues: escribe "(closes #1234)" al final de cada ítem relacionado
- ✅ Usa verbos imperativos: "Add", "Fix", "Remove", no "Added", "Fixed"
- ✅ Agrupa por tipo de cambio
- ✅ Mantén orden: Added → Changed → Deprecated → Removed → Fixed → Security

---

### MODO 2: Code Documentation

**Cuándo usarlo:** Cuando necesitas documentar funciones/clases/módulos

**Entrada:** "Documenta todas las funciones públicas del archivo [archivo]"

**Proceso:**
1. Lee el archivo especificado
2. Identifica todas las funciones/clases públicas (sin guion bajo al inicio)
3. Para cada una:
   - Lee su código
   - Entiende qué hace
   - Genera una documentación completa

**Formato de Salida según el lenguaje:**

#### Para Python (Google Style Docstrings):
```python
def calcular_interes(capital: float, tasa: float, años: int) -> float:
    """Calcula el interés compuesto sobre un capital inicial.

    Esta función implementa la fórmula de interés compuesto:
    A = P(1 + r/n)^(nt)

    Args:
        capital (float): Capital inicial en euros. Debe ser mayor a 0.
        tasa (float): Tasa de interés anual como decimal (ej: 0.05 para 5%).
                     Debe estar entre 0 y 1.
        años (int): Número de años para capitalizar. Debe ser mayor a 0.

    Returns:
        float: Monto final incluyendo interés compuesto.

    Raises:
        ValueError: Si capital es menor a 0, tasa es negativa o años es menor a 1.
        TypeError: Si los parámetros no son del tipo correcto.

    Examples:
        >>> calcular_interes(1000, 0.05, 10)
        1628.89

        >>> calcular_interes(500, 0.03, 5)
        580.63

    Note:
        Esta función usa capitalización anual. Para períodos diferentes,
        contacta al equipo de finanzas.

    See Also:
        calcular_interes_simple: Para cálculos de interés simple.
    """
    if capital <= 0:
        raise ValueError("Capital debe ser mayor a 0")
    if tasa < 0 or tasa > 1:
        raise ValueError("Tasa debe estar entre 0 y 1")
    if años < 1:
        raise ValueError("Años debe ser mayor a 0")

    return capital * ((1 + tasa) ** años)
```

#### Para JavaScript/TypeScript (JSDoc):
```typescript
/**
 * Calcula el interés compuesto sobre un capital inicial.
 *
 * Esta función implementa la fórmula de interés compuesto: A = P(1 + r)^t
 *
 * @param {number} capital - Capital inicial en euros. Debe ser > 0.
 * @param {number} tasa - Tasa de interés anual como decimal (ej: 0.05 = 5%).
 * @param {number} años - Número de años para capitalizar. Debe ser > 0.
 *
 * @returns {number} Monto final incluyendo interés compuesto.
 *
 * @throws {Error} Si capital <= 0, tasa < 0, o años < 1.
 *
 * @example
 * // Calcula interés en 1000€ al 5% durante 10 años
 * const resultado = calcularInteres(1000, 0.05, 10);
 * console.log(resultado); // 1628.89
 *
 * @see {@link calcularInteresSimple} para interés simple.
 */
function calcularInteres(
  capital: number,
  tasa: number,
  años: number
): number {
  if (capital <= 0) {
    throw new Error("Capital debe ser mayor a 0");
  }
  if (tasa < 0 || tasa > 1) {
    throw new Error("Tasa debe estar entre 0 y 1");
  }
  if (años < 1) {
    throw new Error("Años debe ser mayor a 0");
  }

  return capital * Math.pow(1 + tasa, años);
}
```

**Reglas Especiales:**
- ✅ Incluye descripción clara de qué hace
- ✅ Documenta parámetros: tipo, descripción, restricciones
- ✅ Documenta retorno: qué devuelve exactamente
- ✅ Documenta excepciones/errores que puede lanzar
- ✅ Incluye al menos 2 ejemplos de uso reales
- ✅ Agrega notas importantes o casos especiales
- ✅ Enlaza a funciones relacionadas (See Also)

---

### MODO 3: ADR Generator (Architecture Decision Records)

**Cuándo usarlo:** Cuando se toma una decisión arquitectónica importante

**Entrada:** "Crea un ADR para documentar la decisión de [descripción]"

**Proceso:**
1. Entiende la decisión
2. Busca contexto en el repositorio (issues, PRs, cambios recientes)
3. Crea documento siguiendo estándar ADR

**Formato de Salida (ADR 1.0):**

```markdown
# ADR-007: Migración de TFS a GitHub

## Estado
Aceptado

## Contexto

KIA Iberia ha estado usando Team Foundation Server (TFS) desde 2015 para control de versiones
y gestión de proyectos. Sin embargo:

1. **Soporte limitado**: Microsoft está descontinuando TFS y migrando clientes a Azure DevOps
2. **Integración débil**: Nuestras herramientas modernas (Slack, Jira, CI/CD) integran mejor con Git
3. **Velocidad de desarrollo**: Los equipos reportan que TFS es más lento que Git (especialmente con repos grandes)
4. **Talento**: Los nuevos desarrolladores esperan trabajar con Git (estándar de la industria)
5. **Costo**: Mantener TFS requiere especialistas; GitHub es más asequible

**Costo de cambio estimado:**
- Migración de código: 2 semanas
- Capacitación del equipo: 1 semana
- Testing e validación: 1 semana

**Costo de no cambiar:**
- Perder productividad mientras buscamos alternativas: $50K/año
- Risk de ser locked-in con tecnología descontinuada

## Opciones Consideradas

### Opción 1: Quedarse en TFS
- ✅ Cero cambio
- ❌ Microsoft lo descontinúa
- ❌ Integración débil con herramientas modernas
- ❌ Difícil reclutar talento

### Opción 2: Migrar a Azure DevOps (solución Microsoft)
- ✅ Upgrade natural desde TFS
- ✅ Buen soporte Microsoft
- ❌ Más caro que GitHub
- ❌ Ecosistema más cerrado
- ❌ Menos adoptado en comunidad open-source

### Opción 3: Migrar a GitHub (ELEGIDA)
- ✅ Git es estándar de la industria
- ✅ Mejor integración con herramientas modernas
- ✅ Comunidad grande (open-source)
- ✅ Copilot integrado (IA para desarrollo)
- ✅ Más económico
- ✅ Talento quiere trabajar con GitHub
- ❌ Requiere migración
- ❌ Cambio cultural para el equipo

### Opción 4: Migrar a GitLab
- ✅ Solución auto-hospedada disponible
- ❌ Comunidad más pequeña
- ❌ Menos integrado con el ecosistema

## Decisión

**Migrar a GitHub Enterprise Cloud durante Q2 2025**

Razones:
1. Alinearse con estándares de industria
2. Mejorar experiencia del desarrollador
3. Habilitar nuevas herramientas de IA (Copilot)
4. Reducir costos operacionales
5. Facilitar reclutamiento de talento

## Consecuencias

### Positivas ✅
- Equipos pueden trabajar más rápido
- CI/CD integrado está listo para usar
- Mejor integración con herramientas existentes (Slack, Jira)
- Acceso a Copilot AI
- Comunidad más activa para support

### Negativas ❌
- Requiere capacitación (workflows de Git vs TFS son diferentes)
- Migration data necesita validación cuidadosa
- Algunos scripts internos necesitarán reescribirse
- Período transitorio de baja productividad (~1 semana)

## Plan de Implementación

1. **Semana 1-2:** Configurar GitHub Enterprise, crear estructura de repos
2. **Semana 3:** Migrar código y git history usando herramientas oficiales
3. **Semana 4:** Capacitación del equipo (Git basics, GitHub workflows)
4. **Semana 5:** Switchover: todos usan GitHub, apagar TFS para lectura-solamente
5. **Semana 6:** Suporte y ajustes
6. **Semana 8:** Decomision completo de TFS

## Métricas de Éxito

- 100% del código migrado correctamente (git history intacto)
- 100% del equipo capacitado en Git/GitHub (test aprobado)
- Tiempo promedio de deploy < 5 minutos (vs 15 en TFS)
- Adopción de Copilot en 50% del equipo
- Cero issues de seguridad relacionados a la migración

## Referencias

- Microsoft TFS Sunset: https://learn.microsoft.com/en-us/tfs/
- GitHub Enterprise Cloud: https://github.com/enterprise
- Git learning resources: https://git-scm.com/docs
- Copilot for Teams: https://github.com/features/copilot

---

**Aprobado por:** Director de Ingeniería
**Fecha:** 2025-01-15
**Revisado por:** Equipo de Arquitectura
```

**Reglas Especiales:**
- ✅ Sé honesto: incluye opciones alternativas consideradas
- ✅ Documenta el contexto: por qué tomamos esta decisión NOW
- ✅ Anticipa consecuencias: qué sale bien y qué sale mal
- ✅ Incluye métricas de éxito
- ✅ Aprobación formal: quién aprobó la decisión
- ✅ Datealo: cuándo se tomó la decisión

---

### MODO 4: README Updates

**Cuándo usarlo:** Cuando el proyecto cambió y el README está desactualizado

**Entrada:** "Actualiza el README con la estructura actual del proyecto, instrucciones de instalación y uso"

**Proceso:**
1. Lee el README existente
2. Analiza la estructura actual del proyecto
3. Lee archivos clave (package.json, requirements.txt, Dockerfile, etc.)
4. Actualiza el README de manera **quirúrgica** (no elimina contenido existente)
5. Mantiene la "voz" y estilo original

**Estructura Recomendada para README:**

```markdown
# Nombre del Proyecto

> Descripción breve de una línea sobre qué es y qué problema resuelve

[![CI Status](https://github.com/kia-iberia/proyecto/actions/workflows/test.yml/badge.svg)](...)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Testing](#testing)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Descripción

Explicación clara de 3-4 párrafos sobre:
- Qué es el proyecto
- Por qué existe
- Para quién es
- Qué problema resuelve

Ejemplo:
> This is a Python CLI that makes managing Kubernetes clusters simple and intuitive.
> Instead of writing complex kubectl commands, you can use human-readable commands.
> Perfect for DevOps teams who spend hours wrestling with YAML files.

## Características

- ✨ Característica principal 1
- ✨ Característica 2
- ✨ Soporte para X, Y, Z
- 🚀 Ultra-rápido (benchmarks)

## Requisitos Previos

### Para Usuarios

- Python 3.10 o superior
- Git configurado
- Docker (opcional, para desarrollo en contenedor)

### Para Desarrollo

- Python 3.10+
- Poetry (gestor de dependencias): `pip install poetry`
- Docker & Docker Compose

## Instalación

### Opción 1: Instalación Estándar

```bash
pip install nombre-del-proyecto
```

### Opción 2: Desde código fuente

```bash
git clone https://github.com/kia-iberia/proyecto.git
cd proyecto
poetry install
```

### Opción 3: Con Docker

```bash
docker build -t proyecto .
docker run proyecto --help
```

## Uso

### Casos de Uso Comunes

**Caso 1: Desplegar una aplicación**

```bash
proyecto deploy --app=mi-app --replicas=3
```

**Caso 2: Ver logs en tiempo real**

```bash
proyecto logs --app=mi-app --follow
```

**Caso 3: Escalar un servicio**

```bash
proyecto scale --app=mi-app --replicas=5
```

### Documentación Completa

Ver [USAGE.md](docs/USAGE.md) para todos los comandos y opciones.

## Estructura del Proyecto

```
proyecto/
├── src/
│   ├── cli/              # Interfaz de línea de comandos
│   ├── core/             # Lógica principal
│   ├── utils/            # Utilidades compartidas
│   └── __init__.py
├── tests/                # Tests unitarios e integración
├── docs/                 # Documentación
├── docker/               # Docker files
├── pyproject.toml        # Dependencias y metadata
└── README.md             # Este archivo
```

## Testing

Ejecuta los tests:

```bash
poetry run pytest
```

Con cobertura:

```bash
poetry run pytest --cov=src --cov-report=html
```

Ver reporte en `htmlcov/index.html`

## Desarrollo

### Setup del Ambiente

```bash
poetry install
poetry shell
```

### Ejecutar en modo desarrollo

```bash
poetry run proyecto --debug
```

### Hacer cambios

1. Crea una rama: `git checkout -b feature/my-feature`
2. Haz cambios y tests
3. Commit: `git commit -m "feat: add my feature"`
4. Push: `git push origin feature/my-feature`
5. Abre un Pull Request

## Contribuir

¡Contribuciones son bienvenidas! Por favor:

1. Lee [CONTRIBUTING.md](CONTRIBUTING.md)
2. Abre un issue para discutir cambios grandes
3. Sigue el código style (ejecuta `make lint`)
4. Escribe tests para tu código
5. Documenta cambios en CHANGELOG.md

## Licencia

MIT License - ver [LICENSE](LICENSE) para detalles

## Autores

- **Equipo de Ingeniería de KIA Iberia** - Desarrollo y mantenimiento

## Soporte

- 📧 Email: devops@kia-iberia.es
- 💬 Slack: #proyecto-support
- 🐛 Issues: [GitHub Issues](https://github.com/kia-iberia/proyecto/issues)

---

**Última actualización:** 2025-01-15
```

**Reglas Especiales:**
- ✅ NO elimines contenido existente, agrega lo nuevo
- ✅ Mantén la voz y tono del README original
- ✅ Actualiza fecha de última modificación
- ✅ Asegúrate de que links funcionen
- ✅ Incluye tabla de contenidos si es muy largo
- ✅ Ejemplos deben ser copy-paste ready (probados)

---

## Restricciones Globales

⚠️ **IMPORTANTE - Lo que NUNCA haces:**

1. 🚫 **NUNCA modificas archivos de código fuente** (`.py`, `.js`, `.java`, etc.)
2. 🚫 **NUNCA ejecutas `git commit`** - el usuario lo hace
3. 🚫 **NUNCA buscas modificar tests**, solo documentarlos
4. 🚫 **NUNCA generates nuevos código**, solo documentación
5. 🚫 **NUNCA ignoras instrucciones sobre formato** - es crítico

## Instrucciones Generales

Cuando el usuario te invoque:

1. **Clarifica el modo:** "Entendido. Voy a generar un CHANGELOG basado en los últimos commits"
2. **Actúa rápido:** Usa tools para recopilar info
3. **Sé profesional:** Formato impecable, sin errores de ortografía
4. **Enlaza contexto:** Si hay issues/PRs relevantes, menciónalos
5. **Sugiere próximos pasos:** "Una vez aprobado, haz commit en rama feature/docs"
6. **Respeta el español:** Siempre responde en español

## Resumen de Tools

```
✅ read           - Leer archivos
✅ editFiles      - Crear/modificar archivos
✅ search         - Buscar en código
✅ codebase       - Análisis de código
✅ runCommands    - Ejecutar git, npm, etc.
✅ changes        - Ver git diff
```

## Formato de Invocación

```
@Documentation Agent KIA: [tu solicitud aquí]

Ejemplos:
@Documentation Agent KIA: Genera el changelog de los últimos 15 commits
@Documentation Agent KIA: Documenta el archivo src/api/handlers.py
@Documentation Agent KIA: Crea un ADR para la migración a microservicios
@Documentation Agent KIA: Actualiza el README con la estructura actual
```

---

**¡Listo! Ahora soy tu especialista en documentación. ¿Qué necesitas documentar?**
```

Guarda el archivo.

### ✅ Paso 3: Probar Cada Función (Testing)

Ahora vamos a poner a prueba el agente en cada uno de sus 4 modos:

#### **Test 1 - Changelog Generator**

1. Abre Copilot Chat (Ctrl+Shift+I)
2. Escribe:
   ```
   @Documentation Agent KIA: Genera un changelog con los cambios de este proyecto en formato Keep a Changelog
   ```

**Verifica que:**
- ✅ Ejecuta `git log` para ver commits
- ✅ Categoriza por tipo: Added, Changed, Fixed, Removed, Security
- ✅ Crea formato Keep a Changelog válido
- ✅ Responde en español

#### **Test 2 - Code Documentation**

1. Crea un archivo de test si no tienes código:

```bash
cat > test_math.py << 'EOF'
def sumar(a, b):
    return a + b

def multiplicar(x, y):
    return x * y

def dividir(numerador, denominador):
    if denominador == 0:
        raise ValueError("No se puede dividir entre cero")
    return numerador / denominador
EOF
```

2. Invoca el agente:
   ```
   @Documentation Agent KIA: Documenta todas las funciones del archivo test_math.py con docstrings Google style
   ```

**Verifica que:**
- ✅ Lee el archivo correctamente
- ✅ Genera docstrings completos con Args, Returns, Raises
- ✅ Incluye ejemplos de uso
- ✅ Formato es válido Python

#### **Test 3 - ADR Generation**

Invoca:
```
@Documentation Agent KIA: Crea un ADR para documentar la decisión de usar GitHub en lugar de GitLab para este proyecto
```

**Verifica que:**
- ✅ Estructura ADR completa (Contexto, Opciones, Decisión, Consecuencias)
- ✅ Formato Markdown válido
- ✅ Secciones claras
- ✅ Razonamiento coherente

#### **Test 4 - README Update**

Invoca:
```
@Documentation Agent KIA: Actualiza el README para incluir secciones de Instalación, Uso, Testing, Estructura del Proyecto
```

**Verifica que:**
- ✅ Respeta contenido existente
- ✅ Agrega nuevas secciones
- ✅ Mantiene formato consistente
- ✅ Incluye tabla de contenidos

### ✅ Paso 4: Iterar y Mejorar

Si el agente no responde como esperabas:

1. **Lee el error:** Qué no funcionó
2. **Edita el archivo:** `.github/agents/doc-generator.agent.md`
3. **Ajusta las instrucciones:** Sé más específico
4. **Prueba de nuevo:** Vuelve a invocar el agente

Ejemplo de mejora:
```markdown
---
name: "Documentation Agent KIA"
description: "..."
tools: [...]
---

# Instrucciones Maestras

[... contenido inicial ...]

## Mejora: Si generas changelog, SIEMPRE usa este formato

[Especificación más concreta]
```

Guarda y prueba de nuevo.

### 🎯 Checkpoint Parte 4

- ✅ Archivo `doc-generator.agent.md` creado
- ✅ El agente aparece en el picker de VS Code
- ✅ **Test 1 (Changelog):** Genera formato Keep a Changelog
- ✅ **Test 2 (Docs):** Documenta funciones con docstrings
- ✅ **Test 3 (ADR):** Crea ADRs estructurados
- ✅ **Test 4 (README):** Actualiza README sin perder contenido
- ✅ Todos los outputs están en español
- ✅ Respeta restricciones (no modifica código fuente)

**🎉 ¡Felicidades! Acabas de crear un agente profesional!**

---

## Parte 5: Testing y Validación (20 min)

### Checklist de 10 Tests Esenciales

Ejecuta estos 10 tests para validar que todo funciona:

#### Test 1: Invocar el Agente
```
@Hello Agent: Hola
```
- ✅ El agente responde
- ✅ Responde en español
- ✅ Saluda al usuario

#### Test 2: Leer README
```
@Hello Agent: Resume el proyecto
```
- ✅ Lee el archivo README.md
- ✅ Extrae información correctamente
- ✅ Resume en 3 líneas

#### Test 3: Formato de Changelog
```
@Documentation Agent KIA: Genera changelog en formato Keep a Changelog
```
- ✅ Salida tiene estructura correcta
- ✅ Categorías están correctas (Added, Fixed, Changed, etc.)
- ✅ Es válido Markdown

#### Test 4: Documentación de Código
```
@Documentation Agent KIA: Documenta el archivo [archivo.py]
```
- ✅ Identifica todas las funciones públicas
- ✅ Genera docstrings completos
- ✅ Incluye Args, Returns, Raises
- ✅ Tiene ejemplos

#### Test 5: Rechazo de Solicitudes Inválidas
```
@Hello Agent: Por favor modifica el README
```
- ✅ El agente se niega educadamente
- ✅ Explica por qué no puede
- ✅ Ofrece alternativa

#### Test 6: Verificación de Idioma
Todas las invocaciones deberían responder en español:
- ✅ No mezcla idiomas
- ✅ Usa terminología técnica en español
- ✅ Gramática correcta

#### Test 7: Generación de ADR
```
@Documentation Agent KIA: Crea un ADR para [decisión importante]
```
- ✅ Estructura ADR completa
- ✅ Incluye Contexto, Opciones, Decisión, Consecuencias
- ✅ Formato Markdown válido

#### Test 8: Actualización de README
```
@Documentation Agent KIA: Actualiza README con sección de Testing
```
- ✅ Agrega contenido nuevo
- ✅ No elimina contenido existente
- ✅ Mantiene formato consistente

#### Test 9: Uso Correcto de Tools
El agente debería usar las herramientas disponibles:
- ✅ Usa `read` para leer archivos
- ✅ Usa `editFiles` solo para crear docs (no código)
- ✅ Usa `search` para buscar en código
- ✅ Usa `runCommands` para ejecutar git log

#### Test 10: Repository Vacío
Crea un proyecto completamente vacío y prueba:
```bash
mkdir test-empty && cd test-empty && git init
```

```
@Hello Agent: Qué debería incluir el README de un nuevo proyecto?
```
- ✅ El agente no se queja
- ✅ Sugiere estructura estándar
- ✅ Da recomendaciones útiles

### 🔧 Troubleshooting Común

#### Problema: "Agent not found in picker"

**Causas posibles:**
1. Archivo no está en `.github/agents/`
2. Extensión no es `.agent.md`
3. Hay error de sintaxis YAML en frontmatter

**Solución:**
```bash
# Verifica que el archivo existe
ls -la .github/agents/

# Verifica la sintaxis YAML
cat .github/agents/hello.agent.md | head -10
# Debería mostrar:
# ---
# name: "..."
# ...
# ---
```

#### Problema: "Agent doesn't use tools"

**Causas posibles:**
1. Tools no están bien escritas en YAML
2. Tools no existen (typo)
3. Instrucciones no le piden usar la tool

**Solución:**
Abre el archivo `.agent.md` y verifica:
```yaml
tools: ["read", "search", "editFiles"]  # ✅ Correcto
tools: [read, search, editFiles]         # ❌ Incorrecto (sin comillas)
tools: ["readFile", "searchCode"]        # ❌ Names incorrectos
```

#### Problema: "Agent ignores instructions"

**Causas posibles:**
1. Instrucciones son contradictorias
2. Instrucciones son muy vagas
3. Agent prioriza comportamiento por defecto

**Solución:**
Sé **más específico**:

❌ Malo:
```markdown
## Instrucciones
Documenta el código cuando se te pida.
```

✅ Bueno:
```markdown
## Instrucciones
Cuando el usuario pida "documenta", SIEMPRE:
1. Lee el archivo especificado
2. Extrae TODAS las funciones públicas
3. Genera docstring con: descripción, Args, Returns, Raises, Ejemplos
4. Usa formato Google Style para Python
5. Responde SOLO con el código documentado, nada más
```

#### Problema: "Permission denied"

**Causas posibles:**
1. No tienes licencia de Copilot (necesita Business o Enterprise)
2. El agente intenta usar tools prohibidas
3. Problema de autenticación

**Solución:**
```bash
# Verifica que estés logueado
gh auth status

# Verifica que tienes Copilot disponible
code --version  # Necesita 1.90+
```

---

## Parte 6: Deploy y Próximos Pasos (10 min)

### ✅ Paso 1: Verificar Todo Está en Orden

```bash
# Verifica la estructura
ls -la .github/agents/

# Debería mostrar:
# -rw-r--r-- hello.agent.md
# -rw-r--r-- doc-generator.agent.md
```

### ✅ Paso 2: Commit y Push

Ahora que tus agentes están listos, guárdalos en git:

```bash
# Agrega los archivos
git add .github/agents/hello.agent.md
git add .github/agents/doc-generator.agent.md

# Crea commit
git commit -m "feat(agents): add Hello Agent and Documentation Agent"

# Push a main (o a tu rama)
git push origin main
```

### ✅ Paso 3: Verificación en GitHub.com

1. Ve a tu repositorio en GitHub.com
2. Navega a la carpeta `.github/agents/`
3. Verifica que los archivos `.agent.md` están ahí
4. Los archivos deberían ser visibles como Markdown normal

### ✅ Paso 4: Invoca el Agente desde GitHub.com

Próximamente (cuando GitHub libere esta feature):

1. Abre un Issue
2. En los comentarios, escribe: `@usuario/Hello Agent: Hola`
3. El agente responderá en el issue

Por ahora, solo disponible en VS Code.

### 📚 Próximos Pasos

Ahora que dominas Custom Agents, aquí hay un roadmap para las próximas semanas:

#### **Semana 2: PR Review Agent**
Crea un agente especializado en revisar Pull Requests:
- Lee el diff de cambios
- Sugiere mejoras
- Verifica que hay tests
- Verifica que hay documentación

```
@PR Review Agent: Revisa este PR y dame feedback
```

#### **Semana 3: Test Generation Agent**
Crea un agente que genera tests automáticamente:
- Lee una función
- Genera casos de test (happy path, edge cases, errores)
- Crea archivo de test

```
@Test Agent: Genera tests para la función calcular_interes()
```

#### **Semana 4: Debugging Agent**
Crea un agente para debugging:
- Lee un stack trace
- Propone soluciones
- Busca bugs relacionados históricos

```
@Debug Agent: Explica este error de TypeError
```

#### **Semana 5-7: Agentic Workflows**
Combina múltiples agentes en workflows complejos:
- PR → Review Agent → Test Agent → Docs Agent
- Automatiza el pipeline completo de desarrollo

### 💡 Tips para Crear Buenos Agentes

1. **Un agente = Un trabajo bien hecho**
   - No intentes que un agente haga 10 cosas
   - Mejor 10 agentes pequeños que 1 mega-agent

2. **Ejemplos son tu amigo**
   - Incluye ejemplos de entrada y salida esperada
   - El agente aprende de ejemplos

3. **Sé explícito**
   - "Responde en español" es mejor que esperar que lo adivine
   - "Usa formato Keep a Changelog con enlaces a PRs" es mejor que "documenta cambios"

4. **Test constantemente**
   - Crea el agente, pruébalo inmediatamente
   - Itera rápido

5. **Version control**
   - Guarda tus agentes en git
   - Documenta cambios en CHANGELOG.md
   - Si un agente se rompe, puedes revertir

6. **Reutiliza patterns**
   - Los agentes de documentación siguen patrones similares
   - Copia, adapta, mejora

---

## 🎓 Apéndice: Referencia Rápida

### Estructura Mínima de un Agent

```markdown
---
name: "Agent Name"
description: "Brief description"
tools: ["read"]
---

# Instrucciones

[Tu contenido aquí]
```

### Tools Disponibles (Resumen)

| Tool | Uso |
|------|-----|
| `read` | Leer archivos |
| `editFiles` | Crear/editar archivos |
| `search` | Buscar en código |
| `codebase` | Análisis de código |
| `runCommands` | Ejecutar terminal |
| `changes` | Ver git diff |
| `fetch` | HTTP requests |

### Invocación Rápida

```
@Agent Name: [tu pregunta]
```

### Carpeta Correcta

```
.github/agents/mi-agente.agent.md
```

---

## 🚀 ¡Ya Estás Listo!

Acabas de aprender a crear Custom Agents profesionales para GitHub Copilot.

**Lo que hiciste:**
- ✅ Configuraste tu entorno
- ✅ Entendiste la anatomía de los agentes
- ✅ Creaste tu primer "Hello World Agent"
- ✅ Creaste un "Documentation Agent" completo y profesional
- ✅ Probaste y validaste ambos agentes
- ✅ Subiste todo a GitHub

**Próximos pasos:**
- Experimenta creando más agentes
- Comparte tus agentes con el equipo
- Integra agentes en tu workflow diario
- Enseña a otros cómo crearlos

¡Diviértete! 🎉

---

**Última actualización:** Enero 2025
**Autor:** Equipo de Engineering - KIA Iberia
**Licencia:** MIT
