# mcp-ti-helpdesk

Servidor MCP para gestion inteligente de incidentes de TI, integrado con Claude Desktop.

## Guia desde cero (maquina nueva)

Esta guia asume que acabas de clonar el repositorio y no tienes dependencias ni base de datos configurada.

## 1) Prerrequisitos

- Python 3.10
- pip
- Git
- Claude Desktop (para consumo MCP)
- Cuenta/instancia de Neo4j Aura (requerida para GraphRAG)

## 2) Clonar repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd mcp-ti-helpdesk
```

## 3) Crear y activar entorno virtual

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4) Configurar variables de entorno

Crear archivo `.env` en la raiz del proyecto:

```env
NEO4J_URI=neo4j+s://<tu-instancia>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<tu_password>
NEO4J_DATABASE=neo4j
```

Notas:

- `NEO4J_DATABASE` es opcional; por defecto se usa `neo4j`.
- ChromaDB usa persistencia local en `.chroma` por defecto.

## 5) Configurar Neo4j y cargar grafo

1. Crea o habilita una instancia de Neo4j Aura.
2. Usa las credenciales en el `.env`.
3. Carga el grafo base desde CSV:

```bash
python ingestion/load_graph.py
```

4. (Opcional) Validar conectividad de Neo4j:

```bash
python graph_rag/validate_neo4j_connection.py
```

## 6) Inicializar datos documentales y acciones

No necesitas un comando manual extra para RAG y planner:

- RAG indexa automaticamente desde `data/archivo1_documentos.json` cuando se invoca `search_documents`.
- Planner carga acciones desde `data/archivo3_acciones.json` cuando se invoca `plan_resolution`.

## 7) Ejecutar servidor MCP local

Comando principal (transporte stdio):

```bash
python -m mcp_server.server
```

Alternativa sin activar venv:

```bash
./.venv/bin/python -m mcp_server.server
```

## 8) Configurar Claude Desktop (macOS)

Archivo:

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Agregar `mcpServers` en el nivel raiz del JSON (al mismo nivel que `preferences`):

```json
{
  "mcpServers": {
    "mcp-ti-helpdesk": {
      "command": "/bin/zsh",
      "args": [
        "-lc",
        "cd '/Users/luiscelano/Documents/umg/2026/Inteligencia Artificial/mcp-ti-helpdesk' && './.venv/bin/python' -m mcp_server.server"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "CHROMA_PERSIST_DIR": ".chroma"
      }
    }
  }
}
```

Si tu archivo ya tiene otras llaves (por ejemplo `preferences`), no las elimines; solo agrega/mergea `mcpServers`.

## 9) Reiniciar y probar en Claude Desktop

1. Cerrar Claude Desktop completamente.
2. Abrir Claude Desktop.
3. Verificar que aparezca el servidor `mcp-ti-helpdesk`.
4. Probar un prompt como:

```text
Resuelve este incidente: Mi usuario esta bloqueado y no puedo ingresar al sistema.
```

## 10) Herramientas MCP expuestas

- `resolve_incident`
- `search_documents`
- `search_graph`
- `plan_resolution`

Estas herramientas reutilizan componentes existentes y no reimplementan RAG, GraphRAG, Planner ni Security.

## 11) Validaciones recomendadas

Validacion rapida de capa MCP:

```bash
python -m unittest tests.MCP.test_mcp_baseline tests.MCP.test_mcp_server_layer
```

Validacion completa de entrega:

```bash
./tests/f6_t05_acceptance_test.sh
```

## Problemas comunes

1. No aparece el servidor en Claude Desktop

- Verifica JSON valido.
- Verifica que `mcpServers` este al nivel raiz.
- Reinicia Claude Desktop.

2. Error de Neo4j al invocar `search_graph` o `resolve_incident`

- Revisa `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` en `.env`.
- Ejecuta `python graph_rag/validate_neo4j_connection.py`.

3. Error de dependencias o Python

- Confirma Python 3.10.
- Reinstala en venv: `pip install -r requirements.txt`.
