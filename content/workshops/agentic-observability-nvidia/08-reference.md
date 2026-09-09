+++
title       = "Reference & Troubleshooting"
description = "What was added, where it lives, and how to check it."
weight      = 80
+++

## The three additions at a glance

| Addition | Where | What changed |
| --- | --- | --- |
| Splunk Agent Observability | each agent's YAML, `general.telemetry.tracing` | one `galileo`-type exporter block |
| Cisco AI Defense | environment | `NIM_LLM_BASE_URL` and `NVIDIA_API_KEY` |
| HEC forwarding to Splunk Core | each agent's YAML plus one container | one `otelcollector`-type exporter block; the OpenTelemetry Collector with a `splunk_hec` exporter |

The blueprint checkout is never edited. All additions live in the workshop repository's `deploy/` directory and are applied with one extra Docker Compose file.

## Environment variables

| Variable | Used by | Purpose |
| --- | --- | --- |
| `NIM_LLM_BASE_URL` | agents (blueprint) | model endpoint; points at the Cisco AI Defense gateway |
| `NVIDIA_API_KEY` | agents (blueprint) | bearer credential presented to that endpoint |
| `NIM_EMBED_BASE_URL` | agents (blueprint) | local Nemotron 3 Embed NIM |
| `SPLUNK_AO_OTEL_ENDPOINT` | agents (overlay) | Splunk Agent Observability OTLP traces endpoint |
| `SPLUNK_AO_PROJECT`, `SPLUNK_AO_AGENT_STREAM`, `SPLUNK_AO_API_KEY` | agents (overlay) | project, agent stream, and key |
| `OTEL_COLLECTOR_ENDPOINT` | agents (overlay) | local collector, OTLP over HTTP |
| `SPLUNK_HEC_URL`, `SPLUNK_HEC_TOKEN`, `SPLUNK_HEC_INDEX` | collector | HTTP Event Collector destination |
| `WORKSHOP_ENVIRONMENT` | collector | storefront instance name stamped on every event |

## Ports on the instance

| Port | Service | Exposure |
| --- | --- | --- |
| 80 | nginx (storefront) | through the access-key gate only |
| 8000, 8001, 2091 | merchant API, PSP, Apps SDK | internal |
| 8002–8005 | NeMo Agent Toolkit agents | internal |
| 8010, 8011 | Nemotron 3.5 Lightning NIM, Nemotron 3 Embed NIM | internal |
| 6006 | Phoenix | internal |
| 4317, 4318 | OpenTelemetry Collector | internal |

## Health checks

- Storefront: `GET /api/health` returns 200.
- NIMs: `GET /v1/health/ready` on each NIM returns 200.
- Collector: `otelcol_exporter_sent_spans` on its metrics endpoint rises after a search; no `send_failed` series appears.
- HTTP Event Collector: `GET <hec-url>/health` returns `{"text":"HEC is healthy","code":17}`.

## Troubleshooting

Lorem ipsum
