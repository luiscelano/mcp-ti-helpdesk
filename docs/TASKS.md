# TASKS.md

## Convenciones

- IDs por fase: F0, F1, F2, F3, F4, F5, F6.
- Dependencias: IDs de tareas previas.
- Complejidad: Baja, Media, Alta.

## Fase 0 - Preparación de Entorno y Datos Base

### F0-T01

- ID: F0-T01
- Estado: Completada (2026-06-03)
- Estado: Completada (2026-06-03)
- Objetivo: Configurar entorno Python 3.10 y entorno virtual del proyecto.
- Archivos involucrados: requirements.txt, .venv/
- Dependencias: Ninguna
- Criterio de aceptación: El entorno virtual se activa correctamente y Python reporta versión 3.10.
- Evidencia: mcp_server/f5_t03_acceptance_test.sh (PASS)
- Estimación de complejidad: Baja
- Evidencia: .venv/f0_t01_acceptance_test.sh (PASS)

### F0-T02

- ID: F0-T02
- Estado: Completada (2026-06-03)
- Objetivo: Definir variables de entorno mínimas para ChromaDB y Neo4j.
- Archivos involucrados: .env, .vscode/settings.json
- Dependencias: F0-T01
- Criterio de aceptación: Variables requeridas presentes y accesibles en ejecución local.
- Estimación de complejidad: Baja
- Evidencia: .vscode/f0_t02_acceptance_test.sh (PASS)

### F0-T03

- ID: F0-T03
- Estado: Completada (2026-06-03)
- Objetivo: Validar conectividad con Neo4j Aura.
- Archivos involucrados: graph_rag/, docs/PROJECT_READINESS.md
- Dependencias: F0-T02
- Criterio de aceptación: Conexión autenticada y consulta mínima de validación ejecutada.
- Estimación de complejidad: Media
- Evidencia: graph_rag/f0_t03_acceptance_test.sh (PASS)

### F0-T04

- ID: F0-T04
- Estado: Completada (2026-06-03)
- Objetivo: Verificar disponibilidad de insumos de datos oficiales.
- Archivos involucrados: data/archivo1_documentos.json, data/archivo2_grafo.csv, data/archivo3_acciones.json
- Dependencias: Ninguna
- Criterio de aceptación: Los tres archivos existen y cumplen estructura esperada.
- Estimación de complejidad: Baja
- Evidencia: data/f0_t04_acceptance_test.sh (PASS)

### F0-T05

- ID: F0-T05
- Estado: Completada (2026-06-03)
- Objetivo: Preparar baseline de pruebas por especificaciones críticas.
- Archivos involucrados: tests/, docs/specifications.md
- Dependencias: F0-T01
- Criterio de aceptación: Existe estructura de pruebas separada por SEC, CLS, RAG, GRAPH, PLAN, MCP, INGEST, INT.
- Estimación de complejidad: Media
- Evidencia: tests/f0_t05_acceptance_test.sh (PASS)

## Fase 1 - Ingesta de Datos

### F1-T01

- ID: F1-T01
- Estado: Completada (2026-06-03)
- Objetivo: Implementar carga documental desde data/archivo1_documentos.json.
- Archivos involucrados: ingestion/ingest_documents.py, data/archivo1_documentos.json
- Dependencias: F0-T01, F0-T04
- Criterio de aceptación: Se procesan documentos POL-001, POL-002, REG-003 y MAN-004.
- Estimación de complejidad: Media
- Evidencia: ingestion/f1_t01_acceptance_test.sh (PASS)

### F1-T02

- ID: F1-T02
- Estado: Completada (2026-06-03)
- Objetivo: Implementar indexación en ChromaDB sin chunking (1 documento = 1 unidad).
- Archivos involucrados: ingestion/ingest_documents.py, rag/
- Dependencias: F1-T01
- Criterio de aceptación: Colección creada y cuatro documentos indexados como unidades completas.
- Estimación de complejidad: Media
- Evidencia: rag/f1_t02_acceptance_test.sh (PASS)

### F1-T03

- ID: F1-T03
- Estado: Completada (2026-06-03)
- Objetivo: Implementar carga del grafo desde data/archivo2_grafo.csv.
- Archivos involucrados: ingestion/load_graph.py, data/archivo2_grafo.csv
- Dependencias: F0-T03, F0-T04
- Criterio de aceptación: Nodos y relaciones cargados; consultas GRAPH-001/002/003 retornan resultados esperados.
- Estimación de complejidad: Media
- Evidencia: ingestion/f1_t03_acceptance_test.sh (PASS)

### F1-T04

- ID: F1-T04
- Estado: Completada (2026-06-03)
- Objetivo: Implementar carga de acciones desde data/archivo3_acciones.json (INGEST-003).
- Archivos involucrados: ingestion/load_actions.py, data/archivo3_acciones.json, planner/
- Dependencias: F0-T04
- Criterio de aceptación: Acciones disponibles para planner con precondiciones y efectos válidos.
- Estimación de complejidad: Media
- Evidencia: ingestion/f1_t04_acceptance_test.sh (PASS)

### F1-T05

- ID: F1-T05
- Estado: Completada (2026-06-03)
- Objetivo: Validar ingesta end-to-end de documentos, grafo y acciones.
- Archivos involucrados: tests/, ingestion/
- Dependencias: F1-T02, F1-T03, F1-T04
- Criterio de aceptación: INGEST-001, INGEST-002 e INGEST-003 pasan en pruebas.
- Estimación de complejidad: Media
- Evidencia: tests/f1_t05_acceptance_test.sh (PASS)

## Fase 2 - Seguridad y Clasificación

### F2-T01

- ID: F2-T01
- Estado: Completada (2026-06-03)
- Objetivo: Implementar detector de prompt injection y bypass de políticas.
- Archivos involucrados: security/
- Dependencias: F0-T01
- Criterio de aceptación: SEC-001 y SEC-002 bloquean entradas maliciosas antes de cualquier recuperación.
- Estimación de complejidad: Alta
- Evidencia: security/f2_t01_acceptance_test.sh (PASS)

### F2-T02

- ID: F2-T02
- Estado: Completada (2026-06-03)
- Objetivo: Definir contrato de respuesta de seguridad para solicitudes bloqueadas.
- Archivos involucrados: security/, mcp_server/
- Dependencias: F2-T01
- Criterio de aceptación: Respuesta estructurada con estado blocked sin invocar RAG/GraphRAG/planner.
- Estimación de complejidad: Baja
- Evidencia: security/f2_t02_acceptance_test.sh (PASS)

### F2-T03

- ID: F2-T03
- Estado: Completada (2026-06-03)
- Objetivo: Implementar clasificador por categorías acceso, hardware, software y seguridad.
- Archivos involucrados: classifier/
- Dependencias: F0-T01
- Criterio de aceptación: CLS-001 a CLS-004 pasan con las entradas de especificación.
- Estimación de complejidad: Media
- Evidencia: classifier/f2_t03_acceptance_test.sh (PASS)

### F2-T04

- ID: F2-T04
- Estado: Completada (2026-06-03)
- Objetivo: Integrar seguridad + clasificación en un gate único de entrada.
- Archivos involucrados: mcp_server/, security/, classifier/
- Dependencias: F2-T02, F2-T03
- Criterio de aceptación: Solicitudes bloqueadas no avanzan; solicitudes legítimas se clasifican y continúan.
- Estimación de complejidad: Media
- Evidencia: mcp_server/f2_t04_acceptance_test.sh (PASS)

### F2-T05

- ID: F2-T05
- Estado: Completada (2026-06-03)
- Objetivo: Cubrir pruebas de regresión para seguridad y clasificación.
- Archivos involucrados: tests/
- Dependencias: F2-T04
- Criterio de aceptación: SEC-001/002/003 y CLS-001/002/003/004 pasan de forma repetible.
- Estimación de complejidad: Media
- Evidencia: tests/f2_t05_acceptance_test.sh (PASS)

## Fase 3 - RAG y GraphRAG

### F3-T01

- ID: F3-T01
- Estado: Completada (2026-06-03)
- Objetivo: Implementar búsqueda semántica documental en ChromaDB.
- Archivos involucrados: rag/, mcp_server/
- Dependencias: F1-T02, F2-T04
- Criterio de aceptación: RAG-001, RAG-002 y RAG-003 recuperan documentos esperados.
- Estimación de complejidad: Media
- Evidencia: rag/f3_t01_acceptance_test.sh (PASS)

### F3-T02

- ID: F3-T02
- Estado: Completada (2026-06-03)
- Objetivo: Ajustar parámetros de recuperación (top-k y filtros) para estabilidad mínima.
- Archivos involucrados: rag/
- Dependencias: F3-T01
- Criterio de aceptación: Recuperación consistente en pruebas repetidas de RAG.
- Estimación de complejidad: Media
- Evidencia: rag/f3_t02_acceptance_test.sh (PASS)

### F3-T03

- ID: F3-T03
- Estado: Completada (2026-06-03)
- Objetivo: Implementar consultas de relaciones y caminos en Neo4j.
- Archivos involucrados: graph_rag/, mcp_server/
- Dependencias: F1-T03, F2-T04
- Criterio de aceptación: GRAPH-001, GRAPH-002 y GRAPH-003 cumplen resultados esperados.
- Estimación de complejidad: Media
- Evidencia: graph_rag/f3_t03_acceptance_test.sh (PASS)

### F3-T04

- ID: F3-T04
- Estado: Completada (2026-06-03)
- Objetivo: Exponer herramientas search_documents y search_graph con contrato estable.
- Archivos involucrados: mcp_server/, rag/, graph_rag/
- Dependencias: F3-T01, F3-T03
- Criterio de aceptación: MCP-002 y MCP-003 disponibles y funcionales desde el servidor MCP.
- Estimación de complejidad: Media
- Evidencia: mcp_server/f3_t04_acceptance_test.sh (PASS)

### F3-T05

- ID: F3-T05
- Estado: Completada (2026-06-03)
- Objetivo: Agregar pruebas combinadas RAG + GraphRAG para casos reales.
- Archivos involucrados: tests/
- Dependencias: F3-T04
- Criterio de aceptación: Casos compuestos pasan sin romper reglas de seguridad.
- Estimación de complejidad: Media
- Evidencia: tests/f3_t05_acceptance_test.sh (PASS)

## Fase 4 - Planificador

### F4-T01

- ID: F4-T01
- Estado: Completada (2026-06-03)
- Objetivo: Construir modelo interno de acciones, precondiciones, efectos y costo.
- Archivos involucrados: planner/, data/archivo3_acciones.json
- Dependencias: F1-T04
- Criterio de aceptación: El planner carga todas las acciones y valida integridad del dominio.
- Estimación de complejidad: Media
- Evidencia: planner/f4_t01_acceptance_test.sh (PASS)

### F4-T02

- ID: F4-T02
- Estado: Completada (2026-06-03)
- Objetivo: Implementar backward chaining simple sin GOAP/PDDL.
- Archivos involucrados: planner/, docs/agent_constraints.md
- Dependencias: F4-T01
- Criterio de aceptación: El algoritmo genera secuencias para alcanzar objetivo con precondiciones satisfechas.
- Estimación de complejidad: Alta
- Evidencia: planner/f4_t02_acceptance_test.sh (PASS)

### F4-T03

- ID: F4-T03
- Estado: Completada (2026-06-03)
- Objetivo: Implementar validación estricta de precondiciones y bloqueo de acciones inválidas.
- Archivos involucrados: planner/
- Dependencias: F4-T02
- Criterio de aceptación: PLAN-002 pasa y se impide ejecutar acciones sin hechos requeridos.
- Estimación de complejidad: Media
- Evidencia: planner/f4_t03_acceptance_test.sh (PASS)

### F4-T04

- ID: F4-T04
- Estado: Completada (2026-06-03)
- Objetivo: Implementar selección de plan válido de menor costo.
- Archivos involucrados: planner/
- Dependencias: F4-T03
- Criterio de aceptación: PLAN-003 pasa y se reporta plan de menor costo total.
- Estimación de complejidad: Media
- Evidencia: planner/f4_t04_acceptance_test.sh (PASS)

### F4-T05

- ID: F4-T05
- Estado: Completada (2026-06-03)
- Objetivo: Exponer plan_resolution con contrato compatible MCP.
- Archivos involucrados: mcp_server/, planner/
- Dependencias: F4-T04
- Criterio de aceptación: MCP-004 disponible y PLAN-001/002/003 pasan vía herramienta MCP.
- Estimación de complejidad: Media
- Evidencia: mcp_server/f4_t05_acceptance_test.sh (PASS)

## Fase 5 - Orquestación MCP y Respuesta Final

### F5-T01

- ID: F5-T01
- Estado: Completada (2026-06-03)
- Objetivo: Definir pipeline de resolve_incident con orden obligatorio de módulos.
- Archivos involucrados: mcp_server/
- Dependencias: F2-T04, F3-T04, F4-T05
- Criterio de aceptación: El flujo sigue seguridad -> clasificación -> RAG -> GraphRAG -> planner -> respuesta.
- Estimación de complejidad: Alta
- Evidencia: mcp_server/f5_t01_acceptance_test.sh (PASS)

### F5-T02

- ID: F5-T02
- Estado: Completada (2026-06-03)
- Objetivo: Implementar generador de respuesta estructurada final.
- Archivos involucrados: mcp_server/
- Dependencias: F5-T01
- Criterio de aceptación: La salida contiene classification, rag_results, graph_results, resolution_plan y final_response.
- Estimación de complejidad: Media
- Evidencia: mcp_server/f5_t02_acceptance_test.sh (PASS)

### F5-T03

- ID: F5-T03
- Estado: Completada (2026-06-03)
- Objetivo: Implementar manejo de errores y fallback controlado por etapa.
- Archivos involucrados: mcp_server/, security/, rag/, graph_rag/, planner/
- Dependencias: F5-T01
- Criterio de aceptación: Errores parciales no rompen el contrato de salida y quedan trazados.
- Estimación de complejidad: Alta
- Evidencia: mcp_server/f5_t03_acceptance_test.sh (PASS)
- Evidencia: mcp_server/f5_t03_acceptance_test.sh (PASS)

### F5-T04

- ID: F5-T04
- Estado: Completada (2026-06-03)
- Objetivo: Validar herramienta principal resolve_incident contra MCP-001.
- Archivos involucrados: tests/, mcp_server/
- Dependencias: F5-T02, F5-T03
- Criterio de aceptación: MCP-001 pasa con casos legítimos y casos bloqueados.
- Estimación de complejidad: Media
- Evidencia: mcp_server/f5_t04_acceptance_test.sh (PASS)
- Evidencia: mcp_server/f5_t04_acceptance_test.sh (PASS)

### F5-T05

- ID: F5-T05
- Estado: Completada (2026-06-03)
- Objetivo: Validar integración end-to-end con escenario INT-001.
- Archivos involucrados: tests/, mcp_server/, rag/, graph_rag/, planner/
- Dependencias: F5-T04
- Criterio de aceptación: INT-001 pasa con estructura y contenido esperado.
- Estimación de complejidad: Alta
- Evidencia: tests/f5_t05_acceptance_test.sh (PASS)

## Fase 6 - Estabilización y Demo

### F6-T01

- ID: F6-T01
- Estado: Completada (2026-06-03)
- Objetivo: Consolidar suite mínima de regresión por especificación.
- Archivos involucrados: tests/
- Dependencias: F5-T05
- Criterio de aceptación: Conjunto mínimo SEC/CLS/RAG/GRAPH/PLAN/MCP/INGEST/INT pasa completo.
- Estimación de complejidad: Media
- Evidencia: tests/f6_t01_acceptance_test.sh (PASS)

### F6-T02

- ID: F6-T02
- Estado: Completada (2026-06-03)
- Objetivo: Preparar escenarios de demo (legítimo, complejo, malicioso).
- Archivos involucrados: docs/IMPLEMENTATION_PLAN.md, tests/
- Dependencias: F6-T01
- Criterio de aceptación: Escenarios ejecutables con resultado esperado y narrativa de validación.
- Estimación de complejidad: Baja
- Evidencia: tests/f6_t02_acceptance_test.sh (PASS)

### F6-T03

- ID: F6-T03
- Estado: Completada (2026-06-03)
- Objetivo: Documentar riesgos residuales y limitaciones de entrega.
- Archivos involucrados: docs/PROJECT_READINESS.md, docs/IMPLEMENTATION_PLAN.md
- Dependencias: F6-T01
- Criterio de aceptación: Riesgos abiertos priorizados con mitigación y plan post-entrega.
- Estimación de complejidad: Baja
- Evidencia: tests/f6_t03_acceptance_test.sh (PASS)

### F6-T04

- ID: F6-T04
- Estado: Completada (2026-06-03)
- Objetivo: Ejecutar validación final de consistencia documental.
- Archivos involucrados: docs/architecture.md, docs/specifications.md, docs/PROJECT_READINESS.md, docs/IMPLEMENTATION_PLAN.md, docs/TASKS.md
- Dependencias: F6-T03
- Criterio de aceptación: Sin contradicciones críticas entre arquitectura, especificaciones y plan.
- Estimación de complejidad: Baja
- Evidencia: tests/f6_t04_acceptance_test.sh (PASS)

### F6-T05

- ID: F6-T05
- Estado: Completada (2026-06-03)
- Objetivo: Cerrar versión candidata de entrega académica.
- Archivos involucrados: docs/, tests/
- Dependencias: F6-T02, F6-T04
- Criterio de aceptación: Entrega ejecutable, demostrable y trazable a especificaciones.
- Estimación de complejidad: Media
- Evidencia: tests/f6_t05_acceptance_test.sh (PASS)
