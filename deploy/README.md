# deploy/ — the workshop overlay

Everything the workshop adds to the NVIDIA Retail Agentic Commerce blueprint (v1.0.0) lives here. The blueprint
checkout is never edited; the overlay is applied with one extra `-f` file and one env file.

| Path | Addition | What it is |
| --- | --- | --- |
| `agents/configs/*.yml` | (a) Splunk AO, (c) HEC | the blueprint's four NAT agent YAMLs plus a `galileo` exporter, an `otelcollector` exporter, and a file logger; `agents/upstream/` holds the pristine copies and `agents/workshop.diff` the audit diff |
| `compose/docker-compose.workshop.yml` | (a)(c) | mounts the configs over `/app/configs`, adds the OpenTelemetry Collector, optional `local-gateway` profile |
| `otel/collector.yaml` | (c) | OTLP + agent log files → `splunk_hec` (Splunk Show stack) |
| `env.workshop.example` | (a)(b)(c) | every added variable; copy to `.env.workshop` (gitignored) |
| `gateway/` | (b) fallback | LiteLLM proxy config using its built-in `cisco_ai_defense` guardrail, if the hosted AI Defense Gateway cannot front the NIM |
| `ec2/` | rig | instance spec, runbook, `bootstrap.sh`, Caddyfile, tunnel config, systemd units |
| `splunk/` | Lab 4 | SPL searches and the Dashboard Studio JSON |

## Apply

```bash
export WORKSHOP_DIR=/opt/AgenticObservabilityWithNvidia
cp "$WORKSHOP_DIR/deploy/env.workshop.example" "$WORKSHOP_DIR/deploy/.env.workshop"   # then fill it in
cd /opt/Retail-Agentic-Commerce                                                       # blueprint @ v1.0.0
docker network create acp-infra-network || true
docker compose -f docker-compose.infra.yml -f docker-compose.yml -f docker-compose-nim.yml \
  -f "$WORKSHOP_DIR/deploy/compose/docker-compose.workshop.yml" up -d --build
git status --porcelain            # must be empty: the blueprint is as shipped
```

Cisco AI Defense (b) is not a file in this directory: it is the `NIM_LLM_BASE_URL` / `NVIDIA_API_KEY` pair in
`.env.workshop`, pointed at the AI Defense Gateway connection created in the console.
