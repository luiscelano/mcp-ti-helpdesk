# PROJECT_READINESS.md

## Contexto

Este documento evalua la preparacion del proyecto para implementacion y pruebas, con base en:

- [docs/vision.md](docs/vision.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/specifications.md](docs/specifications.md)
- [docs/agent_constraints.md](docs/agent_constraints.md)

Se identifican dependencias, servicios, datos, variables, credenciales, prerrequisitos, riesgos y bloqueadores, clasificando cada elemento como:

- Obligatorio
- Opcional
- Simulable localmente

## 1) Dependencias Externas

| Dependencia                                         | Clasificacion        | Motivo                                                                                                             | Componentes afectados                                                              | Pasos de configuracion                                                                                                                                            |
| --------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python 3.10                                         | Obligatorio          | Lenguaje base definido para todo el sistema.                                                                       | MCP Server, clasificador, seguridad, RAG, GraphRAG, planificador, ingesta, pruebas | 1. Instalar Python 3.10. 2. Verificar version activa. 3. Crear entorno virtual del proyecto.                                                                      |
| MCP Python SDK (oficial)                            | Obligatorio          | Exponer herramientas MCP (resolve_incident, search_documents, search_graph, plan_resolution).                      | Capa de integracion MCP Server <-> Claude Desktop                                  | 1. Instalar dependencia en entorno virtual. 2. Definir servidor MCP con herramientas requeridas. 3. Registrar el servidor en Claude Desktop.                      |
| Claude Desktop                                      | Obligatorio          | Cliente de usuario y consumidor exclusivo de herramientas MCP (RULE-006).                                          | Interfaz de usuario, integracion end-to-end                                        | 1. Instalar Claude Desktop. 2. Configurar conexion al servidor MCP local. 3. Validar invocacion de herramientas.                                                  |
| ChromaDB                                            | Obligatorio          | Base vectorial para RAG tradicional.                                                                               | Modulo RAG, ingesta documental, resolve_incident, pruebas RAG e integracion        | 1. Instalar libreria. 2. Definir ruta/persistencia local. 3. Crear/llenar coleccion de documentos embebidos.                                                      |
| sentence-transformers                               | Obligatorio          | Generar embeddings para indexacion y busqueda semantica en espanol.                                                | Pipeline de ingesta, busqueda RAG                                                  | 1. Instalar libreria. 2. Configurar modelo multilingue recomendado (paraphrase-multilingual-MiniLM-L12-v2). 3. Descargar modelo y validar generacion de vectores. |
| Neo4j Aura                                          | Obligatorio          | Grafo relacional para GraphRAG (servicio externo definido por restricciones del proyecto).                         | Modulo GraphRAG, ingesta del grafo, resolve_incident, pruebas GRAPH-\*             | 1. Crear instancia Neo4j Aura. 2. Configurar URI, usuario y password. 3. Cargar nodos/relaciones iniciales. 4. Probar consultas basicas.                          |
| Driver Neo4j para Python                            | Obligatorio          | Conexion programatica al grafo Neo4j Aura.                                                                         | Modulo GraphRAG y consultas search_graph                                           | 1. Instalar driver. 2. Configurar pool de conexion y timeout. 3. Validar autenticacion con consulta de salud.                                                     |
| PyMuPDF                                             | Opcional             | Util para escenarios futuros con documentos PDF; el flujo vigente de INGEST-001 usa data/archivo1_documentos.json. | Ingestion documental extendida                                                     | 1. Instalar libreria solo si se procesaran PDFs. 2. Implementar lectura de PDF cuando aplique. 3. Validar extraccion con documentos reales.                       |
| python-dotenv                                       | Obligatorio          | Gestion de configuracion por variables de entorno local.                                                           | Inicializacion de servicios y credenciales                                         | 1. Instalar libreria. 2. Definir archivo .env local. 3. Cargar variables al inicio del servidor.                                                                  |
| pytest                                              | Obligatorio          | Validacion de especificaciones SEC, CLS, RAG, GRAPH, PLAN, MCP, INGEST e INT.                                      | Suite de pruebas unitarias e integracion                                           | 1. Instalar pytest. 2. Estructurar tests por especificacion. 3. Ejecutar pruebas localmente.                                                                      |
| Acceso a modelos de Hugging Face (descarga inicial) | Simulable localmente | Necesario solo para primera descarga del modelo de embeddings; luego puede operar con cache local.                 | sentence-transformers, pipeline RAG                                                | 1. Descargar modelo en etapa inicial con internet. 2. Confirmar cache local. 3. Ejecutar en modo offline si aplica.                                               |

## 2) Servicios Requeridos

| Servicio                             | Clasificacion | Motivo                                                                           | Componentes afectados                                                   | Pasos de configuracion                                                                                        |
| ------------------------------------ | ------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Servidor MCP local (Python)          | Obligatorio   | Orquesta todo el flujo del sistema y expone herramientas MCP.                    | Todos los modulos internos y cliente Claude Desktop                     | 1. Configurar entorno Python. 2. Registrar herramientas. 3. Iniciar proceso local y verificar disponibilidad. |
| Neo4j Aura                           | Obligatorio   | Fuente de relaciones para GraphRAG.                                              | search_graph, ingesta del grafo, resolve_incident, pruebas GRAPH/INT    | 1. Provisionar instancia. 2. Cargar grafo base. 3. Validar consultas de caminos y relaciones.                 |
| ChromaDB local persistente           | Obligatorio   | Almacenamiento y recuperacion de conocimiento documental.                        | search_documents, ingesta documental, resolve_incident, pruebas RAG/INT | 1. Definir ruta de persistencia. 2. Crear coleccion. 3. Poblar indice vectorial.                              |
| Servicio de logging/monitoreo formal | Opcional      | Mejora trazabilidad en demo y depuracion, pero no es condicion funcional minima. | Operacion y soporte tecnico                                             | 1. Definir formato de logs estructurados. 2. Configurar salida a archivo. 3. Agregar niveles de severidad.    |

## 3) Datos Requeridos

| Dato                                                                    | Clasificacion        | Motivo                                                                                             | Componentes afectados                                                | Pasos de configuracion                                                                                                                                                      |
| ----------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| data/archivo1_documentos.json                                           | Obligatorio          | Fuente oficial de conocimiento documental para RAG segun arquitectura (seccion 7).                 | Ingesta documental, search_documents, resolve_incident               | 1. Validar estructura JSON. 2. Confirmar que el archivo sea accesible en el entorno. 3. Indexar cada documento completo en ChromaDB (sin chunking) con embeddings.          |
| Registros de ingesta requeridos (POL-001, POL-002, REG-003, MAN-004)    | Obligatorio          | Requeridos por INGEST-001 y necesarios para consultas de acceso, impresion, seguridad y prestamos. | Ingesta documental, pruebas RAG e integracion                        | 1. Confirmar presencia de los cuatro registros en data/archivo1_documentos.json. 2. Validar metadatos e identificadores. 3. Verificar recuperacion semantica por categoria. |
| Grafo de conocimiento (entidades y relaciones)                          | Obligatorio          | Requerido por GRAPH-001/002/003 e INGEST-002.                                                      | search_graph, ingesta del grafo, resolve_incident, pruebas GRAPH/INT | 1. Definir esquema de nodos y relaciones. 2. Cargar dataset inicial en Neo4j. 3. Validar caminos esperados.                                                                 |
| data/archivo2_grafo.csv                                                 | Obligatorio          | Entrada explicita para la carga del grafo de conocimiento segun INGEST-002.                        | Ingestion de grafo, GraphRAG                                         | 1. Preparar CSV con nodos y relaciones. 2. Validar formato de columnas. 3. Ejecutar carga en Neo4j Aura.                                                                    |
| data/archivo3_acciones.json (acciones, costos, precondiciones, efectos) | Obligatorio          | Fuente del planificador y de la ingesta de acciones segun PLAN-\* e INGEST-003.                    | load_actions, plan_resolution, resolve_incident, pruebas PLAN/INGEST | 1. Validar formato del archivo. 2. Cargarlo al inicio mediante Action Loader. 3. Ejecutar pruebas de precondiciones, efectos y objetivos del planner.                       |
| Dataset sintetico de incidentes de prueba                               | Simulable localmente | Permite validar clasificador y seguridad sin datos productivos.                                    | Clasificador, seguridad, pruebas SEC/CLS                             | 1. Crear ejemplos por categoria y casos maliciosos. 2. Etiquetar expected outputs. 3. Integrar en pruebas automatizadas.                                                    |

## 4) Variables de Entorno

| Variable             | Clasificacion | Motivo                                                                            | Componentes afectados        | Pasos de configuracion                                                                                                                          |
| -------------------- | ------------- | --------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| NEO4J_URI            | Obligatorio   | Endpoint de conexion al grafo Neo4j Aura.                                         | GraphRAG, ingesta del grafo  | 1. Obtener URI de Neo4j Aura. 2. Definirla en .env. 3. Validar conectividad.                                                                    |
| NEO4J_USERNAME       | Obligatorio   | Usuario para autenticacion en Neo4j Aura.                                         | GraphRAG, ingesta del grafo  | 1. Crear/usar usuario de base. 2. Guardar en .env. 3. Probar autenticacion.                                                                     |
| NEO4J_PASSWORD       | Obligatorio   | Password de acceso al grafo.                                                      | GraphRAG, ingesta del grafo  | 1. Generar credencial segura. 2. Guardar en .env local (no versionar). 3. Verificar login.                                                      |
| CHROMA_PERSIST_DIR   | Obligatorio   | Ruta de persistencia local de ChromaDB para reutilizar indices entre ejecuciones. | RAG, ingesta documental      | 1. Definir directorio local. 2. Crear permisos de lectura/escritura. 3. Validar persistencia tras reinicio sin reprocesamiento.                 |
| EMBEDDING_MODEL_NAME | Obligatorio   | Modelo de embeddings consistente para indexar y consultar en espanol.             | Pipeline de embeddings y RAG | 1. Configurar en .env el modelo recomendado: paraphrase-multilingual-MiniLM-L12-v2. 2. Validar carga del modelo. 3. Reindexar si cambia modelo. |
| LOG_LEVEL            | Opcional      | Controla verbosidad de logs para depuracion.                                      | Todos                        | 1. Definir valor (INFO/DEBUG). 2. Ajustar por entorno (dev/demo).                                                                               |
| APP_ENV              | Opcional      | Permite separar configuraciones (dev, test, demo).                                | Inicializacion global        | 1. Definir entorno activo. 2. Cargar configuraciones condicionales.                                                                             |

Nota: Los nombres exactos pueden ajustarse al repositorio final, pero estas variables son funcionalmente necesarias para cumplir arquitectura y especificaciones.

## 5) Credenciales Necesarias

| Credencial                                         | Clasificacion | Motivo                                                         | Componentes afectados                             | Pasos de configuracion                                                                       |
| -------------------------------------------------- | ------------- | -------------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Usuario y password de Neo4j Aura                   | Obligatorio   | Sin credenciales no hay consultas GraphRAG ni carga del grafo. | search_graph, ingesta del grafo, resolve_incident | 1. Crear credenciales en Neo4j Aura. 2. Guardar en .env local. 3. Verificar query de prueba. |
| Acceso a Claude Desktop (sesion activa)            | Obligatorio   | Requerido para operar como cliente MCP durante demo.           | Flujo de usuario end-to-end                       | 1. Iniciar sesion en Claude Desktop. 2. Confirmar acceso a herramientas MCP.                 |
| Token de repositorios/modelos privados (si aplica) | Opcional      | Solo necesario si documentos/modelos no son publicos.          | Pipeline de ingesta o descarga de modelos         | 1. Crear token de solo lectura. 2. Guardar como secreto local. 3. Probar acceso controlado.  |

## 6) Prerrequisitos de Desarrollo

| Prerrequisito                                      | Clasificacion        | Motivo                                                                                            | Componentes afectados         | Pasos de configuracion                                                                 |
| -------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------- |
| Sistema operativo compatible (macOS/Linux/Windows) | Obligatorio          | Soporte de Python, dependencias y herramientas locales.                                           | Entorno completo              | 1. Verificar compatibilidad de librerias. 2. Validar rutas y permisos locales.         |
| Git y control de versiones                         | Obligatorio          | Gestion de cambios y colaboracion academica.                                                      | Todo el proyecto              | 1. Configurar repositorio. 2. Definir ramas de trabajo. 3. Confirmar flujo de commits. |
| Entorno virtual Python                             | Obligatorio          | Aisla dependencias y evita conflictos globales.                                                   | MCP server, ingesta y pruebas | 1. Crear venv. 2. Activar entorno. 3. Instalar dependencias del proyecto.              |
| Acceso a internet durante setup inicial            | Simulable localmente | Requerido para instalar paquetes y descargar modelos; luego operacion puede ser mayormente local. | Setup inicial                 | 1. Ejecutar instalacion inicial conectada. 2. Cachear dependencias/modelos.            |
| Editor/IDE (VS Code recomendado)                   | Opcional             | Mejora productividad, pero no es obligatorio para ejecutar.                                       | Desarrollo y depuracion       | 1. Instalar editor. 2. Configurar extensiones Python/testing.                          |

## 7) Riesgos Tecnicos

| Riesgo                                                              | Clasificacion        | Impacto                                                              | Mitigacion recomendada                                                                                                         |
| ------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Falsos positivos en capa de seguridad (bloquea consultas legitimas) | Obligatorio          | Puede cortar el flujo y degradar utilidad del sistema.               | Definir reglas y pruebas negativas/positivas basadas en SEC-001/002/003.                                                       |
| Falsos negativos en seguridad (deja pasar prompt injection)         | Obligatorio          | Riesgo de incumplimiento y respuestas inseguras.                     | Endurecer deteccion de patrones de bypass y registrar eventos.                                                                 |
| Baja relevancia del RAG por calidad de datos/embeddings             | Obligatorio          | Respuestas incompletas o incorrectas.                                | Curar corpus, ajustar top-k y evaluar con casos RAG-001/002/003.                                                               |
| Uso de modelo no multilingue para consultas en espanol              | Obligatorio          | Caida de precision semantica en recuperacion documental.             | Fijar EMBEDDING_MODEL_NAME a paraphrase-multilingual-MiniLM-L12-v2 y validar consultas en espanol.                             |
| Grafo incompleto o inconsistente                                    | Obligatorio          | GraphRAG no recupera caminos esperados en GRAPH-\* o INGEST-002.     | Validar cobertura de entidades clave y relaciones obligatorias.                                                                |
| Planificador sin validacion estricta de precondiciones              | Obligatorio          | Puede sugerir acciones invalidas (violacion de PLAN-002 y RULE-005). | Implementar verificacion de estado/facts y pruebas de regresion.                                                               |
| Ingesta documental incompleta o JSON fuente inconsistente           | Obligatorio          | No se cumplen INGEST-001 ni los RAG esperados.                       | Confirmar integridad de data/archivo1_documentos.json y presencia de POL-001, POL-002, REG-003 y MAN-004 antes de indexar.     |
| Ingesta del grafo con CSV mal formado                               | Obligatorio          | No se cumplen INGEST-002 ni las consultas GRAPH-\*.                  | Validar columnas, relaciones y nodos de data/archivo2_grafo.csv antes de cargar en Neo4j.                                      |
| Ingesta de acciones incompleta o JSON invalido                      | Obligatorio          | No se cumple INGEST-003 y el planner no puede construir planes.      | Validar data/archivo3_acciones.json, precondiciones, efectos y objetivo usuario_desbloqueado antes de habilitar planificación. |
| Cambios de modelo de embeddings sin reindexacion                    | Simulable localmente | Deteriora recuperacion por incompatibilidad vectorial.               | Fijar version de modelo y gatillar reindexado al cambiarla.                                                                    |
| Dependencia de un servicio externo unico (Neo4j Aura)               | Obligatorio          | Caida de servicio afecta GraphRAG completo.                          | Agregar manejo de fallos, timeouts y respuesta degradada.                                                                      |
| Sobrecarga de alcance en una semana academica                       | Obligatorio          | Riesgo de no completar integracion end-to-end.                       | Priorizar MVP segun restricciones y posponer mejoras no criticas.                                                              |

## 8) Bloqueadores Potenciales

| Bloqueador                                                                                                 | Clasificacion        | Senal de bloqueo                                                     | Accion preventiva/contingencia                                                                |
| ---------------------------------------------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| No contar con credenciales validas de Neo4j Aura                                                           | Obligatorio          | search_graph o la ingesta del grafo falla en conexion/autenticacion. | Solicitar credenciales al inicio del proyecto y validar conectividad dia 1.                   |
| Corpus documental incompleto (faltan POL-001, POL-002, REG-003 o MAN-004 en data/archivo1_documentos.json) | Obligatorio          | No se cumple INGEST-001 ni RAG-001/002/003.                          | Confirmar integridad de data/archivo1_documentos.json antes de implementar el pipeline final. |
| Falta de data/archivo2_grafo.csv o formato invalido                                                        | Obligatorio          | INGEST-002 no puede ejecutarse correctamente.                        | Definir esquema CSV y validar integridad temprana.                                            |
| Falta de data/archivo3_acciones.json o formato invalido                                                    | Obligatorio          | INGEST-003 y plan_resolution no pueden ejecutarse correctamente.     | Definir esquema JSON y validar integridad temprana.                                           |
| Integracion MCP no registrada correctamente en Claude Desktop                                              | Obligatorio          | Herramientas no visibles o no invocables.                            | Validar registro de servidor y prueba de herramienta minima desde Claude.                     |
| Restricciones de tiempo para pruebas completas                                                             | Obligatorio          | Cobertura insuficiente de especificaciones.                          | Priorizar matriz minima SEC, CLS, RAG, GRAPH, PLAN, MCP, INGEST e INT en pytest.              |
| Inestabilidad de red durante setup                                                                         | Simulable localmente | Fallan instalaciones/descargas iniciales.                            | Preparar cache local de paquetes/modelos y plan de ejecucion offline parcial.                 |

## 9) Estructura del Proyecto

La estructura prevista y ya reflejada en la arquitectura actual es:

```text
project/
├── ingestion/
│   ├── ingest_documents.py
│   ├── load_graph.py
│   └── load_actions.py
├── docs/
│   ├── vision.md
│   ├── architecture.md
│   └── specifications.md
├── mcp_server/
├── classifier/
├── security/
├── rag/
├── graph_rag/
├── planner/
├── data/
│   ├── archivo1_documentos.json
│   ├── archivo2_grafo.csv
│   └── archivo3_acciones.json
├── tests/
├── requirements.txt
└── README.md
```

## Checklist de Preparacion del Entorno

Marcar cada punto antes de iniciar implementacion formal:

- [ ] Python 3.10 instalado y entorno virtual activo.
- [ ] Dependencias base instaladas (MCP SDK, ChromaDB, sentence-transformers, neo4j driver, dotenv y pytest; PyMuPDF solo si se usaran PDFs).
- [ ] Claude Desktop instalado y con acceso al servidor MCP local.
- [x] Instancia Neo4j Aura creada y conectividad validada.
- [ ] Variables de entorno definidas en archivo local (.env).
- [ ] Credenciales sensibles fuera de control de versiones.
- [ ] Archivo documental consolidado (data/archivo1_documentos.json) con POL-001, POL-002, REG-003 y MAN-004.
- [ ] Estrategia de indexacion aplicada sin chunking (un embedding por documento del JSON).
- [ ] EMBEDDING_MODEL_NAME configurado con modelo multilingue recomendado (paraphrase-multilingual-MiniLM-L12-v2).
- [ ] data/archivo2_grafo.csv preparado y validado.
- [ ] Grafo de conocimiento cargado con relaciones de GRAPH-001/002/003.
- [ ] data/archivo3_acciones.json validado (precondiciones, efectos, costos).
- [ ] Pipeline de indexacion documental ejecutado y ChromaDB persistido.
- [ ] Proceso de ingesta del grafo ejecutado en Neo4j Aura.
- [ ] Proceso de carga de acciones ejecutado y planner inicializado con datos validos.
- [ ] Pruebas minimas por especificacion ejecutadas (SEC, CLS, RAG, GRAPH, PLAN, MCP, INGEST e INT).
- [ ] Flujo end-to-end verificado con caso INT-001.
- [ ] Casos maliciosos validados para confirmar bloqueo temprano (sin llegar a RAG/GraphRAG).
- [ ] Plan de contingencia definido para indisponibilidad de Neo4j Aura.

## Resumen Ejecutivo

La preparacion del proyecto depende principalmente de cuatro ejes obligatorios:

1. Integracion MCP funcional con Claude Desktop.
2. Base documental lista para RAG y grafo listo para GraphRAG.
3. Ingesta de datos validada con los archivos y formatos definidos en la arquitectura.
4. Seguridad y planificador validados contra especificaciones.

Con los elementos obligatorios completados y los simulables preparados localmente, el proyecto puede entrar a implementacion y demostracion con riesgo controlado dentro de la ventana academica.
