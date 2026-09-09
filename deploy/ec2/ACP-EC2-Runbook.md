# ACP Workshop EC2 — Configuration Reference & Rebuild Runbook

**Status:** template — fill in the "as built" values when the first box is provisioned.
**Companion:** `ACP-EC2-Instance-Spec.md` (what a correct box is). This file records what was actually built.

## 1. Scope — what is reproducible

Everything on the box is rebuilt from two public repos plus the hand-over files in Spec §2.2:

| Source | Path on box | Pinned to |
|---|---|---|
| `NVIDIA-AI-Blueprints/Retail-Agentic-Commerce` | `/opt/Retail-Agentic-Commerce` | tag `v1.0.0` (commit `3df75e7`) — **never edited** |
| `mayeack/AgenticObservabilityWithNvidia` | `/opt/AgenticObservabilityWithNvidia` | `main` |

## 2. AWS / instance facts (as built)

| Item | Value |
|---|---|
| Account / profile | _fill in_ |
| Instance ID / type / AZ | _fill in_ / `g6e.12xlarge` / _fill in_ |
| AMI | _fill in (SSM latest at launch time)_ |
| Root volume | 300 GB gp3 |
| Security group | _fill in_ — SSH from operator IP only |
| Key pair | `acp-workshop` |
| Tags | `Name=acp-N`, `acp-workshop=true`, `Replica=N` |
| Tunnel | `acp-N` → `acpN.<zone>` (UUID _fill in_) |

### Ports that must be reachable

See Spec §4. Only 22 is inbound; everything else is via the tunnel or local.

## 3. Users, access, and SSH

- `ubuntu`, key `~/.ssh/acp_workshop`.
- Storefront access key: Caddy basic auth user `acp`, password = the per-box access key (in `/etc/caddy/Caddyfile`).
- NIM bearer token (only if `nimN.<zone>` is published): in `/etc/caddy/Caddyfile`, mirrored in the AI Defense gateway connection.

## 4. Software inventory

| Component | Version | Installed by |
|---|---|---|
| NVIDIA driver / CUDA | from the AMI | AMI |
| Docker Engine + Compose v2 + NVIDIA Container Toolkit | from the AMI | AMI |
| `cloudflared`, `caddy` | apt | `bootstrap.sh` |
| Blueprint images | `nvcr.io/nvidia/blueprint` builds from the checkout (`docker compose build`) | `bootstrap.sh` |
| NIM images | `nemotron-3.5-lightning-30b-a3b:2.0.9-variant`, `nemotron-3-embed-1b:2.2.2` | compose pull |
| Collector | `otel/opentelemetry-collector-contrib:0.157.0` | compose pull |

## 5. Application configuration

### Layout

```
/opt/Retail-Agentic-Commerce/            # blueprint, pristine
  .env                                   # blueprint variables (hand-over)
/opt/AgenticObservabilityWithNvidia/     # this repo
  deploy/.env.workshop                   # workshop variables (hand-over)
  deploy/agents/configs/*.yml            # mounted over /app/configs in the agents
  deploy/otel/collector.yaml
  deploy/compose/docker-compose.workshop.yml
/opt/nim-cache/                          # LOCAL_NIM_CACHE
/etc/caddy/Caddyfile
/etc/cloudflared/config.yml  ~/.cloudflared/<uuid>.json
/etc/systemd/system/acp-stack.service  acp-tunnel.service
```

### `.env.workshop` — non-secret values (verbatim)

```ini
WORKSHOP_ENVIRONMENT=acp1
WORKSHOP_DIR=/opt/AgenticObservabilityWithNvidia
WORKSHOP_LOG_DIR=/app/logs
LOCAL_NIM_CACHE=/opt/nim-cache
NIM_LLM_MODEL_NAME=nvidia/nemotron-3.5-lightning
NIM_LLM_BASE_URL=https://<gateway-host>/<tenant>/<connection>/v1
NIM_EMBED_BASE_URL=http://embedqa:8000/v1
NIM_EMBED_MODEL_NAME=nvidia/nemotron-3-embed-1b
NIM_EMBED_DIM=2048
SPLUNK_AO_CONSOLE_URL=https://console.multitenant.galileocloud.io
SPLUNK_AO_OTEL_ENDPOINT=https://api.multitenant.galileocloud.io/otel/traces
SPLUNK_AO_PROJECT=RetailAgenticCommerce
SPLUNK_AO_AGENT_STREAM=acp1
OTEL_COLLECTOR_ENDPOINT=http://otel-collector:4318/v1/traces
SPLUNK_HEC_URL=https://http-inputs-<stack>.splunkcloud.com:443/services/collector/event
SPLUNK_HEC_INDEX=acp
CISCO_AI_DEFENSE_API_BASE=https://us.api.inspect.aidefense.security.cisco.com
```

Secrets (values withheld): `NGC_API_KEY`, `NVIDIA_API_KEY` (= the AI Defense gateway key), `SPLUNK_AO_API_KEY`,
`SPLUNK_HEC_TOKEN`, `CISCO_AI_DEFENSE_API_KEY`, `LITELLM_MASTER_KEY`.

### The one value you must change per replica

`WORKSHOP_ENVIRONMENT` and `SPLUNK_AO_AGENT_STREAM` (identical strings), plus the tunnel/hostname and the AI Defense
gateway connection. See Spec §6.

### OTel collector pipelines

`traces: otlp → memory_limiter, resource/workshop, batch → splunk_hec/traces (otel:traces)`
`logs: filelog/agents → memory_limiter, resource/workshop, batch → splunk_hec/logs (acp:<agent>)`

### systemd units

| Unit | Runs |
|---|---|
| `acp-stack.service` | `docker compose -f … -f … -f … -f docker-compose.workshop.yml up -d` from the blueprint dir; `down` on stop |
| `acp-tunnel.service` | `cloudflared tunnel --config /etc/cloudflared/config.yml run` |
| `caddy.service` | apt-installed Caddy with `/etc/caddy/Caddyfile` |

## 6. Rebuild procedure — raw EC2 → working replica

1. Launch per Spec §7 step 1; create the tunnel and DNS per step 2.
2. `scp` the three hand-over files to `/tmp` on the box.
3. Run `bootstrap.sh` with `REPLICA`, `ZONE`, `TUNNEL_UUID`, `ACCESS_KEY` (and `NIM_BEARER` if `nimN.<zone>` is published).
4. Wait for `nemotron-lightning` and `embedqa` to report ready (first start downloads ~70 GB: 10–20 minutes).
5. The seeder (`milvus-seeder`) runs once from the blueprint's compose; confirm a search returns products.
6. Validate per Spec §8; capture the Lab 1 screenshots (`docker compose ps`, `nvidia-smi`, Phoenix).

## 7. Verification

Spec §1 table, criteria 1–9. Record the date and the person who verified in this section.

## 8. Known issues and gotchas

- Compose resolves the overlay's relative paths against the blueprint directory — which is why the overlay uses
  `${WORKSHOP_DIR}` everywhere. Do not "fix" the paths to be relative.
- `env_file` entries must exist before `docker compose up`; an empty `.env.workshop` starts the agents without
  exporters and they log a warning per exporter rather than failing.
- Both `nvidia-nat` exporters are registered by `nvidia-nat-opentelemetry`; `nat info components -t telemetry_exporter`
  inside an agent container lists `galileo` and `otelcollector` if the image is intact.
- The AI Defense gateway must be able to reach the NIM. With the hosted gateway that means publishing `nimN.<zone>`
  behind the Caddy bearer check; with the local gateway profile nothing is published.

## 9. Backup set — what is not in git

`/opt/Retail-Agentic-Commerce/.env`, `/opt/AgenticObservabilityWithNvidia/deploy/.env.workshop`, `~/.cloudflared/<uuid>.json`,
`/etc/caddy/Caddyfile` (holds the access key and NIM bearer), `~/.ssh/acp_workshop` on the operator machine.
