# Agent Constraints

## Objetivo

Optimizar la implementación para una entrega académica en una semana.

## Restricciones

- Priorizar simplicidad.
- Priorizar mantenibilidad.
- Evitar sobreingeniería.
- Evitar microservicios.
- Evitar Kubernetes.
- Evitar infraestructura cloud adicional.
- Evitar dependencias innecesarias.
- Ejecutar localmente.
- Neo4j Aura será el único servicio externo.

## Preferencias

- Python 3.10
- MCP SDK oficial
- ChromaDB
- Neo4j Aura
- pytest
- dotenv

## No utilizar

- Redis
- RabbitMQ
- Celery
- Kafka
- Kubernetes
- Terraform
- Docker Swarm

## Planificación

Debido al tamaño reducido del dominio:

- No utilizar motores GOAP.
- No utilizar PDDL.
- No utilizar bibliotecas externas de planificación.
- Implementar backward chaining simple basado en precondiciones y efectos.
