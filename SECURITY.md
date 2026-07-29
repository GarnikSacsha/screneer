# Security Policy

## Scope

Quant Desk is a decision-support demo for Binance USD-M market intelligence. It is not an exchange execution system and must never receive exchange trading credentials.

The maintained surface is the current `main` branch. Before reporting a vulnerability, confirm that it applies to the latest revision.

## Threat model

Assets:

- OpenAI, Telegram, database, and cache credentials;
- availability and cost budget of live ingestion and AI endpoints;
- integrity and freshness of market evidence;
- the human-review and no-execution safety boundary.

Untrusted inputs:

- HTTP clients;
- Binance and other upstream provider payloads;
- cached event messages and market metadata;
- model tool arguments and generated output;
- environment and deployment configuration.

Primary threats:

- unauthorized use of expensive ingestion or model endpoints;
- secret disclosure through source, logs, API errors, or scan artifacts;
- browser injection through upstream strings;
- prompt injection or agent tool-scope escape;
- stale data presented as current;
- publicly reachable Redis or PostgreSQL services;
- dependency and CI supply-chain compromise.

## Security invariants

- The application has no exchange order-placement capability.
- Every AI brief requires human review and returns `execution_allowed=false`.
- Agent tools are read-only and limited to the approved symbol and horizon.
- Production and staging disable protected endpoints unless `ADMIN_API_KEY` is configured.
- Provider exceptions are logged server-side and normalized at the API boundary.
- OpenAI requests use `store=false`; secrets are environment-only and never returned.
- Upstream strings must be escaped before HTML insertion.
- Redis, PostgreSQL, and the demo API bind to loopback by default in Docker Compose.

## Deployment requirements

The checked-in configuration is appropriate for localhost evaluation. Before internet exposure:

1. terminate TLS at a trusted reverse proxy;
2. replace the shared admin key with real user authentication and authorization;
3. enforce distributed rate limiting at the gateway or Redis;
4. use managed data stores or strong credentials without public ports;
5. set explicit production origins and hosts;
6. centralize redacted logs and monitor cost and request anomalies;
7. run dependency, SAST, and Codex Security checks in CI.

`ADMIN_API_KEY` is a temporary portfolio safeguard, not a complete identity system. Never embed it in browser JavaScript.

## Reporting

Do not publish suspected vulnerabilities or secrets in a public issue. Use GitHub's private vulnerability reporting or contact the repository owner privately. Include the affected revision, entry point, impact, and minimal reproduction steps without real credentials.

## Codex Security guidance

Treat this file as policy context. A reportable finding must show a realistic path from an untrusted input to a broken invariant or sensitive sink. Do not treat the deliberate localhost-only demo configuration as internet-ready architecture.
