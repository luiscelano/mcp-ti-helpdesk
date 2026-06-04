# Vision.md

# Sistema Inteligente para Gestión de Incidentes de TI

## 1. Visión General

El Banco Guatemalteco enfrenta dificultades operativas en su mesa de ayuda de tecnología debido a la gestión manual de incidentes reportados por los empleados. Actualmente, los técnicos deben invertir tiempo en buscar información en múltiples documentos, interpretar políticas internas, determinar procedimientos de resolución y redactar respuestas para los usuarios.

Esta situación genera tiempos de respuesta inconsistentes, dependencia del conocimiento individual de cada técnico y riesgos asociados al acceso incorrecto a información sensible.

Para abordar estos problemas, se propone desarrollar un Sistema Inteligente para Gestión de Incidentes de TI basado en Inteligencia Artificial, capaz de asistir en la clasificación, análisis y resolución de incidentes utilizando técnicas modernas de recuperación de conocimiento y razonamiento asistido por modelos de lenguaje.

---

# 2. Problema a Resolver

La organización presenta tres desafíos principales:

### Recuperación ineficiente de conocimiento

Los técnicos deben consultar manualmente políticas, procedimientos, manuales y documentación técnica para encontrar información relevante sobre cada incidente.

Esto provoca:

- Incremento en los tiempos de respuesta.
- Dependencia de la experiencia individual.
- Respuestas inconsistentes entre técnicos.

### Vulnerabilidad frente a manipulación

Los asistentes basados en modelos de lenguaje pueden ser manipulados mediante instrucciones maliciosas que intenten ignorar políticas internas o revelar procedimientos restringidos.

Esto representa riesgos de seguridad y cumplimiento normativo.

### Falta de estandarización en la resolución

Actualmente no existe un mecanismo uniforme para determinar el orden de las acciones necesarias para resolver un incidente.

Como resultado:

- Los procedimientos varían entre técnicos.
- Se generan errores operativos.
- Los tiempos de resolución son inconsistentes.

---

# 3. Objetivo General

Desarrollar un sistema inteligente que asista en la gestión de incidentes de TI mediante la integración de recuperación de conocimiento, análisis de relaciones, planificación de acciones y mecanismos de seguridad, proporcionando respuestas consistentes y fundamentadas para apoyar la toma de decisiones de la mesa de ayuda.

---

# 4. Objetivos Específicos

- Clasificar automáticamente incidentes reportados por los usuarios.
- Recuperar información relevante desde una base documental.
- Recuperar relaciones y dependencias desde un grafo de conocimiento.
- Generar secuencias de acciones coherentes para la resolución de incidentes.
- Detectar y bloquear solicitudes maliciosas o intentos de manipulación.
- Generar respuestas claras y consistentes para los usuarios finales.
- Integrar todas las capacidades mediante herramientas accesibles desde Claude Desktop.

---

# 5. Alcance del Sistema

El sistema estará diseñado para procesar incidentes relacionados con:

- Problemas de acceso a sistemas.
- Problemas de hardware.
- Problemas de software.
- Incidentes relacionados con seguridad.

La solución deberá:

- Recibir una descripción textual del incidente.
- Analizar el contenido de la solicitud.
- Recuperar conocimiento relevante.
- Consultar relaciones dentro de un grafo de conocimiento.
- Construir un plan de resolución.
- Generar una respuesta estructurada.

---

# 6. Actores del Sistema

## Empleado del Banco

Usuario que reporta un incidente y consulta el sistema a través de Claude Desktop.

Responsabilidades:

- Describir el incidente.
- Revisar la respuesta generada.

## Sistema Inteligente

Responsable de analizar la solicitud y generar una respuesta basada en conocimiento recuperado y reglas de negocio.

## Claude Desktop

Interfaz utilizada por los usuarios para interactuar con el sistema mediante herramientas MCP.

---

# 7. Propuesta de Solución

La solución estará basada en una arquitectura donde Claude Desktop utilizará herramientas expuestas por un servidor MCP desarrollado en Python.

El sistema combinará múltiples técnicas de Inteligencia Artificial:

### Recuperación de Conocimiento (RAG)

Permitirá localizar información relevante dentro de documentos, políticas y manuales almacenados en una base vectorial.

### Recuperación Basada en Grafos (GraphRAG)

Permitirá complementar la información documental mediante relaciones explícitas entre entidades y procesos.

### Planificación de Acciones

Permitirá generar secuencias válidas de resolución respetando dependencias y precondiciones.

### Seguridad de Prompts

Permitirá detectar y bloquear solicitudes maliciosas antes de que sean procesadas.

---

# 8. Resultado Esperado

Dado un incidente reportado por un usuario, el sistema deberá producir:

1. Clasificación del incidente.
2. Información documental relevante.
3. Relaciones relevantes del grafo de conocimiento.
4. Plan de resolución recomendado.
5. Respuesta final para el usuario.
6. Bloqueo de solicitudes maliciosas cuando corresponda.

---

# 9. Criterios de Éxito

La solución será considerada exitosa si:

- Clasifica correctamente los incidentes soportados.
- Recupera información relevante para la consulta.
- Utiliza relaciones del grafo para enriquecer las respuestas.
- Genera planes coherentes de resolución.
- Bloquea intentos de manipulación.
- Funciona correctamente desde Claude Desktop mediante MCP.
- Puede ser demostrada utilizando consultas simples, complejas y maliciosas.

---

# 10. Restricciones del Proyecto

- El sistema será desarrollado en Python 3.10.
- La integración con el usuario se realizará mediante Claude Desktop.
- La comunicación se realizará mediante Model Context Protocol (MCP).
- El almacenamiento vectorial utilizará ChromaDB.
- El grafo de conocimiento utilizará Neo4j Aura.
- El proyecto deberá ejecutarse localmente para fines académicos y de demostración.

---

# 11. Fuera de Alcance

La solución no contempla:

- Gestión de tickets.
- Gestión de usuarios bancarios.
- Ejecución automática de acciones sobre sistemas productivos.
- Modificación de cuentas o accesos reales.
- Integraciones con sistemas corporativos del banco.

El sistema tendrá únicamente fines de asistencia y recomendación para la resolución de incidentes.
