# Taller: GitHub Copilot Custom Agents - Archivos Generados

Este directorio contiene todos los materiales para el taller de creación de Custom Agents con GitHub Copilot.

## Archivos Creados

### 1. Guía Completa (Documento Principal)
- **Archivo:** `Guia_Ejercicios_Custom_Agents.md` (41 KB)
- **Contenido:** Guía paso-a-paso en español con 6 partes:
  - Parte 1: Preparación del Entorno (30 min)
  - Parte 2: Anatomía de un Custom Agent (20 min)
  - Parte 3: Ejercicio 1 - Hello World Agent (15 min)
  - Parte 4: Ejercicio 2 - Documentation Agent (45 min)
  - Parte 5: Testing y Validación (20 min)
  - Parte 6: Deploy y Próximos Pasos (10 min)

**Duración total:** 2.5 horas
**Idioma:** Español
**Público:** Desarrolladores con experiencia en VS Code y Git

### 2. Archivos de Agentes (Ejercicios)

#### Ejercicio 1: Hello Agent
- **Archivo:** `ejercicios/01_hello/hello.agent.md` (2.3 KB)
- **Descripción:** Agent simple que:
  - Saluda al usuario
  - Lee el README del proyecto
  - Resume el proyecto en 3 líneas
  - Sugiere 3 mejoras para el README
- **Tools:** `read`, `search`
- **Restricciones:** Solo lee, nunca modifica
- **Objetivo:** Aprender la estructura básica de un agent

#### Ejercicio 2: Documentation Agent
- **Archivo:** `ejercicios/02_doc_agent/doc-generator.agent.md` (17 KB)
- **Descripción:** Agent profesional de documentación con 4 modos:
  1. **Changelog Generator:** Genera CHANGELOGs en formato "Keep a Changelog"
  2. **Code Documentation:** Documenta funciones/clases con docstrings completos
  3. **ADR Generator:** Crea Architecture Decision Records
  4. **README Updates:** Actualiza READMEs sin perder contenido existente
- **Tools:** `read`, `editFiles`, `search`, `codebase`, `runCommands`, `changes`
- **Objetivo:** Crear un agent enterprise-ready y profesional

## Estructura de Directorios

```
taller/
├── README.md                                    # Este archivo
├── Guia_Ejercicios_Custom_Agents.md            # Guía completa del taller
└── ejercicios/
    ├── 01_hello/
    │   └── hello.agent.md                      # Primer agent (Hello World)
    └── 02_doc_agent/
        └── doc-generator.agent.md              # Agent de documentación
```

## Cómo Usar Este Material

### Para Facilitadores
1. Lee la `Guia_Ejercicios_Custom_Agents.md` completa
2. Familiarízate con ambos archivos de agentes
3. Realiza los ejercicios antes de el taller para estar preparado
4. Estima ~2.5 horas de duración total

### Para Participantes
1. Abre la guía en VS Code o tu navegador
2. Sigue cada paso secuencialmente
3. Prueba los agentes localmente
4. Experimenta modificando los archivos `.agent.md`

## Requisitos Previos

- VS Code 1.90 o superior
- Extensiones: GitHub Copilot + GitHub Copilot Chat
- Git configurado
- GitHub CLI (gh)
- Node.js 20+
- Cuenta GitHub con Copilot Business o Enterprise

## Características Principales

### Guía de Ejercicios
- ✅ Paso-a-paso detallado en español
- ✅ Comandos listos para copiar-pegar
- ✅ Checkpoints para validar progreso
- ✅ Troubleshooting común
- ✅ Tests de validación (10 tests)
- ✅ Próximas mejoras sugeridas
- ✅ Referencia rápida de tools

### Archivos de Agentes
- ✅ YAML frontmatter completo y válido
- ✅ Instrucciones detalladas en Markdown
- ✅ Ejemplos de respuestas esperadas
- ✅ Restricciones claras
- ✅ Formatos de salida especificados
- ✅ Comentarios y anotaciones

## Tips Importantes

1. **Lee primero la Parte 2:** Comprende qué es un Custom Agent antes de empezar
2. **Prueba localmente:** Todos los ejercicios se hacen en VS Code local
3. **No copies-pegas ciegamente:** Entiende qué hace cada comando
4. **Experimenta:** Modifica los prompts y ve qué pasa
5. **Valida constantemente:** Usa los checkpoints para verificar progreso

## Próximos Pasos (Roadmap)

La guía sugiere un plan para futuras sesiones:
- Semana 2: PR Review Agent
- Semana 3: Test Generation Agent
- Semana 4: Debugging Agent
- Semana 5-7: Agentic Workflows

## Contacto y Soporte

Para dudas sobre el taller o los agentes:
- Email: devops@kia-iberia.es
- Slack: #proyecto-support

## Versión y Cambios

- **Versión:** 1.0
- **Fecha:** Enero 2025
- **Idioma:** Español
- **Autor:** Equipo de Engineering - KIA Iberia
- **Licencia:** MIT

---

**¡Listo para empezar? Abre `Guia_Ejercicios_Custom_Agents.md` y comienza la Parte 1!**
