# mcp-ti-helpdesk

Servidor MCP para gestion inteligente de incidentes de TI, integrado con Claude Desktop.

## Ejecutar el servidor MCP

Requisitos minimos:

- Entorno virtual en .venv
- Dependencias instaladas

Comando de ejecucion (transporte stdio):

```bash
./.venv/bin/python -m mcp_server.server
```

## Configuracion en Claude Desktop (macOS)

Archivo de configuracion:

- ~/Library/Application Support/Claude/claude_desktop_config.json

Ejemplo:

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

## Herramientas expuestas por MCP

- resolve_incident
- search_documents
- search_graph
- plan_resolution

Estas herramientas reutilizan los componentes existentes del proyecto y no reimplementan logica de RAG, GraphRAG, Planner ni Security.

## Ejemplo de uso

Prompt de ejemplo en Claude Desktop:

```text
Resuelve este incidente: Mi usuario esta bloqueado y no puedo ingresar al sistema.
```

Comportamiento esperado:

- Claude Desktop invoca resolve_incident.
- El servidor MCP ejecuta seguridad, clasificacion, RAG, GraphRAG y planificacion.
- Devuelve respuesta estructurada con final_response.

## Validacion recomendada

Ejecutar suite final de entrega:

```bash
./tests/f6_t05_acceptance_test.sh
```
