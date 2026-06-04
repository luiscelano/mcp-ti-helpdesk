# Guia de configuracion del servidor MCP en Claude Desktop

## Objetivo

Conectar este proyecto a Claude Desktop como servidor MCP local en macOS.

## Requisitos previos

- Claude Desktop instalado.
- Entorno virtual del proyecto creado en .venv.
- Dependencias instaladas en el entorno virtual.
- Variables de entorno del proyecto definidas en .env cuando apliquen.

## Paso 1. Identificar el comando de arranque del servidor MCP

Claude Desktop necesita un comando que inicie el servidor MCP por stdio.

En este repositorio el entrypoint unico del servidor MCP es:

- .venv/bin/python -m mcp_server.server

Este entrypoint usa FastMCP y transporte stdio.

## Paso 2. Ubicar el archivo de configuracion de Claude Desktop

En macOS, usa este archivo:

- ~/Library/Application Support/Claude/claude_desktop_config.json

Si no existe, crealo manualmente.

## Paso 3. Registrar el servidor MCP

Ejemplo recomendado para este proyecto usando shell con cd al workspace:

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

Notas:

- Si necesitas variables como NEO4J_URI, NEO4J_USERNAME y NEO4J_PASSWORD, agregalas en env o cargalas desde tu flujo de arranque.

## Paso 4. Reiniciar Claude Desktop

- Cierra Claude Desktop completamente.
- Abre Claude Desktop de nuevo para que recargue la configuracion MCP.

## Paso 5. Verificar conexion

En Claude Desktop:

- Abre una conversacion nueva.
- Verifica que aparezca el servidor mcp-ti-helpdesk.
- Prueba una invocacion de herramienta (por ejemplo resolve_incident con un caso legitimo).

## Paso 6. Validar el proyecto antes de demo

Desde el workspace, ejecuta:

- ./tests/f6_t05_acceptance_test.sh

Esto valida la entrega final ejecutable, demostrable y trazable.

## Problemas frecuentes

1. Claude no muestra el servidor

- Revisa JSON valido en claude_desktop_config.json.
- Verifica ruta absoluta del workspace y de .venv/bin/python.
- Reinicia Claude Desktop despues de cada cambio.

2. El servidor inicia pero falla al invocar herramientas

- Verifica que el comando use .venv/bin/python -m mcp_server.server.
- Revisa que el entorno tenga dependencias instaladas.
- Confirma variables de entorno requeridas para Neo4j/ChromaDB.

3. Error de permisos o comando no encontrado

- Asegura permisos de ejecucion en scripts de arranque.
- Usa rutas absolutas en command y args.

## Recomendacion de operacion

Para evitar desviaciones en presentacion academica:

- Mantener un unico nombre de servidor: mcp-ti-helpdesk.
- No cambiar contratos de herramientas durante demo.
- Ejecutar la suite F6-T05 antes de cada sesion demostrativa.
