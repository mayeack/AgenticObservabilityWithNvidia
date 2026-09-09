# ACP Workshop EC2 Instance — Specification

**Version:** 1.0 · **Date:** 2026-09-08
**Scope:** one (1) GPU instance running the NVIDIA Retail Agentic Commerce blueprint (v1.0.0) **as shipped**, plus the
workshop overlay from this repository, publicly reachable at its own `acpN.<zone>` subdomain.
**Source of truth:** `deploy/` in `https://github.com/mayeack/AgenticObservabilityWithNvidia` (this document specifies
*what a correct box is*; `deploy/ec2/bootstrap.sh` is the implementation) and the blueprint's own deployment guide,
`deploy/docker-deployment.md` in `https://github.com/NVIDIA-AI-Blueprints/Retail-Agentic-Commerce` at tag `v1.0.0`.
**Audience:** an operator working from their own machine. Everything needed is in one of the two repos or listed in
§2 as an explicit hand-over item.

> **Count is a run-time parameter.** One box per attendee group. Multiply this spec by the number of groups; every
> value in §6.1 must differ per box.

---

## 1. Definition of done

| # | Acceptance criterion | How it is checked |
|---|---|---|
| 1 | `https://acpN.<zone>/api/health` returns 200 through the tunnel, with the access key | `curl -su "acp:$KEY" https://acpN.<zone>/api/health` |
| 2 | Every path returns 401 without the access key | `curl -sI https://acpN.<zone>/` → 401 |
| 3 | `nvidia-smi` reports **4× NVIDIA L40S**; the Lightning NIM and the Embed NIM are each pinned to their GPU and both `/v1/health/ready` return 200 | ssh to the box, §8 |
| 4 | `git -C /opt/Retail-Agentic-Commerce status --porcelain` is **empty** — the blueprint is as shipped | §8 |
| 5 | A storefront search produces a trace in Splunk AO project `RetailAgenticCommerce`, agent stream `acpN` | Splunk AO console |
| 6 | The same search produces `otel:traces` events in the Splunk index with `deployment.environment=acpN` | Splunk search |
| 7 | With the AI Defense gateway configured, a prompt-injection search is blocked and an event exists in AI Defense | AI Defense console |
| 8 | Two systemd units enabled and active: `acp-stack`, `acp-tunnel`; Caddy active | `systemctl is-active acp-stack acp-tunnel caddy` |
| 9 | Start/stop schedule installed in the workshop's timezone; operator holds the URL **and** access key | the deliverable, §9 |

Criteria 5–7 are the three additions. A box that passes 1–4 only is a working blueprint, not a workshop rig.

---

## 2. Preconditions

### 2.1 Operator machine

| Requirement | Detail |
|---|---|
| Tools | `aws` CLI v2, `cloudflared`, `git`, `ssh`, `jq` |
| Repos | `git clone https://github.com/mayeack/AgenticObservabilityWithNvidia.git` (this repo). The blueprint is cloned **on the box** by `bootstrap.sh` at tag `v1.0.0`; never copy a modified checkout up |
| Cloudflare | `cloudflared tunnel login` as an account that owns `<zone>` |

### 2.2 Credentials and files handed over out of band (never in git)

| Item | Where it goes on the box | Notes |
|---|---|---|
| Blueprint `.env` | `/opt/Retail-Agentic-Commerce/.env` | From the blueprint's `env.example`: `NVIDIA_API_KEY` (build.nvidia.com key, used only to seed Milvus when embeddings are hosted; with local NIMs it is replaced by the gateway key), `MERCHANT_API_KEY`, `PSP_API_KEY`, `WEBHOOK_SECRET` — change the demo defaults |
| Workshop `.env.workshop` | `/opt/AgenticObservabilityWithNvidia/deploy/.env.workshop` | From `deploy/env.workshop.example`: `NGC_API_KEY`, Splunk AO key/project/stream, AI Defense gateway URL + key, HEC URL/token/index, `WORKSHOP_ENVIRONMENT=acpN` |
| Tunnel credentials JSON | `~/.cloudflared/<tunnel-uuid>.json` | per-tunnel file only; the account `cert.pem` never leaves the operator machine |
| SSH key | `~/.ssh/acp_workshop` | matches the EC2 key pair `acp-workshop` |

### 2.3 Account access

| Requirement | Value / check |
|---|---|
| AWS account | Confirm with `aws sts get-caller-identity --profile <profile>` before anything costs money |
| Service quota | *Running On-Demand G and VT instances* (`L-DB2E81BA`) ≥ **48 vCPU per box** (`g6e.12xlarge` = 48 vCPU). Increases take hours to days; request first |
| Security group | SSH (22) from the operator IP only. No other inbound rule — the tunnel dials out |
| NGC | An NGC API key with access to `nvcr.io/nim/nvidia/nemotron-3.5-lightning-30b-a3b` and `nvcr.io/nim/nvidia/nemotron-3-embed-1b` |
| Splunk AO | A project `RetailAgenticCommerce`; one agent stream per box (`acpN`); an API key |
| Cisco AI Defense | An application `ACP Retail Agents` with one **Gateway** connection per box and the runtime policy `ACP Retail Protect` attached |
| Splunk | HEC URL, token, and index on the target stack (on a Splunk Show instance: `/etc/environment`) |

---

## 3. Compute specification

| Property | Value | Rationale |
|---|---|---|
| Instance type | `g6e.12xlarge` | 48 vCPU, 384 GiB, **4× L40S 48 GB**, 100 Gbps. The NIM support matrix lists L40S for Nemotron 3.5 Lightning (BF16 TP≥2 or W4A16 on one card) and for Nemotron 3 Embed 1B |
| Region | `us-east-1` | quota and pricing reference |
| AMI | Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 22.04), resolved at launch from SSM `/aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-ubuntu-22.04/latest/ami-id` | driver, Docker, and NVIDIA Container Toolkit preinstalled; no reboot in the bootstrap |
| Root volume | **300 GB gp3**, `DeleteOnTermination=true` | NIM caches (~63 GB for Lightning BF16, less for W4A16), NIM images (~15 GB each), blueprint images, Milvus. Keep `LOCAL_NIM_CACHE=/opt/nim-cache` on EBS so a stop/start does not re-download models; the 1.9 TB NVMe instance store is ephemeral |
| Login | user `ubuntu`, SSH 22 | |
| Tags | `acp-workshop=true`, `Replica=N`, `Name=acp-N` | `Replica` drives the tunnel name, subdomain, agent stream, and `WORKSHOP_ENVIRONMENT` |

**GPU placement.** The blueprint pins the Lightning NIM to GPU 0 and the Embed NIM to GPU 1 (`docker-compose-nim.yml`).
On a 48 GB card NIM must select the W4A16 profile for Lightning; if `nemotron-lightning` fails to become ready, apply the
commented `NIM_TENSOR_PARALLEL_SIZE=2` / `device_ids: ['0','1']` override in `deploy/compose/docker-compose.workshop.yml`
and move `embedqa` to GPU 2. Milvus runs on the CPU.

---

## 4. Network specification

Nothing is exposed on the instance's public IP. The Cloudflare tunnel dials outbound; Caddy on the host gates both hostnames.

| Port | Bind | Purpose | Exposure |
|---|---|---|---|
| 22 | `0.0.0.0` | SSH | inbound, operator IP only (SG) |
| 80 | `0.0.0.0` (docker) | nginx → storefront UI, merchant API, PSP, Apps SDK | via Caddy :8080 (basic auth) → tunnel `acpN.<zone>` |
| 8010 / 8011 | `0.0.0.0` (docker) | Lightning NIM / Embed NIM | 8010 via Caddy :8090 (bearer) → tunnel `nimN.<zone>` **only when the hosted AI Defense Gateway must reach the NIM** |
| 8000, 8001, 2091, 8002–8005 | docker network | merchant, PSP, Apps SDK, NAT agents | internal (nginx publishes what the UI needs) |
| 6006, 4317 | `0.0.0.0` (docker) | Phoenix UI / OTLP | local only; facilitator screenshots over SSH port-forward |
| 4318, 8888, 13133 | docker network | OpenTelemetry Collector OTLP / metrics / health | internal |
| 19530, 9001, 5432 | `0.0.0.0` (docker) | Milvus, MinIO console, Postgres | local only |

Required egress: `nvcr.io`, `api.ngc.nvidia.com`, `integrate.api.nvidia.com` (first Milvus seed only), `api.multitenant.galileocloud.io`
(or `ingest.<realm>.observability.splunkcloud.com`), `*.aidefense.security.cisco.com` and the AI Defense gateway host, the Splunk HEC
host, Cloudflare edge, Docker Hub, `ghcr.io`, GitHub, PyPI.

### 4.1 DNS and tunnel

```
acpN.<zone>  ──CNAME──> <tunnel-uuid-N>.cfargotunnel.com ──> box N, Caddy :8080 ──> nginx :80
nimN.<zone>  ──CNAME──> <tunnel-uuid-N>.cfargotunnel.com ──> box N, Caddy :8090 ──> NIM :8010   (optional)
```

One named tunnel (`acp-N`) per box. Route DNS by tunnel **UUID**, never by name (`cloudflared tunnel route dns <uuid> acpN.<zone>`).
The URL is the session pin: no load balancer, no shared tunnel.

---

## 5. Software stack

| Layer | Component | Source |
|---|---|---|
| Blueprint | `/opt/Retail-Agentic-Commerce` @ `v1.0.0`, started with `docker-compose.infra.yml` + `docker-compose.yml` + `docker-compose-nim.yml` | NVIDIA |
| NIMs | `nvcr.io/nim/nvidia/nemotron-3.5-lightning-30b-a3b:2.0.9-variant`, `nvcr.io/nim/nvidia/nemotron-3-embed-1b:2.2.2` | NVIDIA (pinned by the blueprint) |
| Overlay | `/opt/AgenticObservabilityWithNvidia/deploy/compose/docker-compose.workshop.yml` (agent configs, collector, optional local gateway) | this repo |
| Collector | `otel/opentelemetry-collector-contrib:0.157.0` | this repo, `deploy/otel/collector.yaml` |
| Edge | Caddy (apt), `cloudflared` (apt) | `deploy/ec2/Caddyfile`, `deploy/ec2/cloudflared.config.yml.example` |
| Units | `acp-stack.service`, `acp-tunnel.service` | `deploy/ec2/*.service` |

---

## 6. Configuration

### 6.1 Values that must differ per box

| Value | Where | Example |
|---|---|---|
| `WORKSHOP_ENVIRONMENT` | `deploy/.env.workshop` | `acp1` |
| `SPLUNK_AO_AGENT_STREAM` | `deploy/.env.workshop` | `acp1` (same string) |
| Tunnel name / hostname | cloudflared | `acp-1` / `acp1.<zone>` |
| Access key | Caddyfile basic auth | generated per box |
| AI Defense gateway connection | `NIM_LLM_BASE_URL`, `NVIDIA_API_KEY` | one connection per box so events are attributable |

### 6.2 One identity, not two

`WORKSHOP_ENVIRONMENT` is stamped by the collector as `deployment.environment` on every HEC event and is the Splunk AO
agent stream name. Lab 4's correlation search and the dashboard filter on it. A mismatch between the two makes the
"same trace in both consoles" moment silently fail.

### 6.3 Secrets handling

- Both env files are copied by `scp` from the operator machine and are `chmod 600`; neither is in git (`.gitignore`).
- The Cloudflare account `cert.pem` never goes to a box; only the per-tunnel credentials JSON does.
- The HEC token lives only in the collector's environment; the blueprint containers never receive it.

---

## 7. Provisioning procedure

```bash
# 0. on the operator machine — confirm the account, quota, and key pair BEFORE anything costs money
aws sts get-caller-identity --profile "$PROFILE"
aws service-quotas get-service-quota --service-code ec2 --quota-code L-DB2E81BA --profile "$PROFILE"   # >= 48 vCPU

# 1. launch (300 GB gp3, the DL Base GPU AMI, SSH-only SG, tags Replica=N)
AMI=$(aws ssm get-parameter --name /aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-ubuntu-22.04/latest/ami-id \
      --query Parameter.Value --output text --profile "$PROFILE")
aws ec2 run-instances --image-id "$AMI" --instance-type g6e.12xlarge --key-name acp-workshop \
  --security-group-ids "$SG" --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=300,VolumeType=gp3,DeleteOnTermination=true}' \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=acp-$N},{Key=acp-workshop,Value=true},{Key=Replica,Value=$N}]" \
  --profile "$PROFILE"

# 2. create the tunnel and route DNS by UUID
cloudflared tunnel create acp-$N
cloudflared tunnel route dns <tunnel-uuid> acp$N.<zone>

# 3. hand-over files to the box, then bootstrap
scp -i ~/.ssh/acp_workshop .env ubuntu@<ip>:/tmp/blueprint.env
scp -i ~/.ssh/acp_workshop .env.workshop ubuntu@<ip>:/tmp/workshop.env
scp -i ~/.ssh/acp_workshop ~/.cloudflared/<tunnel-uuid>.json ubuntu@<ip>:/tmp/tunnel.json
ssh -i ~/.ssh/acp_workshop ubuntu@<ip> \
  'curl -fsSL https://raw.githubusercontent.com/mayeack/AgenticObservabilityWithNvidia/main/deploy/ec2/bootstrap.sh | \
   sudo REPLICA='$N' ZONE=<zone> TUNNEL_UUID=<tunnel-uuid> ACCESS_KEY=<key> bash'
```

`bootstrap.sh` is idempotent: rerunning it re-pulls nothing that is already present and restarts the units.

---

## 8. Validation

```bash
nvidia-smi                                                       # 4x L40S; NIM processes on GPU 0 and 1
curl -sf localhost:8010/v1/health/ready && curl -sf localhost:8011/v1/health/ready
curl -sf localhost/api/health
git -C /opt/Retail-Agentic-Commerce status --porcelain           # must print nothing
docker exec otel-collector wget -qO- localhost:8888/metrics | grep -E 'otelcol_exporter_sent_spans|send_failed'
curl -s "${SPLUNK_HEC_URL%/event}/health"                        # {"text":"HEC is healthy","code":17}
curl -su "acp:$ACCESS_KEY" https://acp$N.<zone>/api/health       # 200 through the tunnel
```

Then run one storefront search and confirm criteria 5–7 in §1.

---

## 9. Deliverable

The operator hands over, per box: the URL as a markdown link, its access key, `WORKSHOP_ENVIRONMENT`, and the Splunk AO
agent stream name — the four values the setup page and the facilitator email need.

---

## 10. Cost (us-east-1, on-demand, list price — verify before provisioning)

| Per box | 8 h/workshop day | 8 h/weekday (~176 h/mo) | always-on |
|---|---|---|---|
| `g6e.12xlarge` compute ($10.49/hr) | ~$84 | ~$1,846 | ~$7,650 |
| EBS 300 GB gp3 (billed even while stopped) | — | ~$24 | ~$24 |
| Cloudflare tunnel / CNAMEs | $0 | $0 | $0 |

A box left running is ~$250/day. Install the start/stop schedule the day the box is built; only `terminate` stops
compute billing, and teardown is incomplete until the CNAME and `cloudflared tunnel delete acp-N` are done too.

---

## 11. Lifecycle and teardown

- **Stop/start** keeps the EBS volume (NIM cache included) — restart takes ~5 minutes for the NIMs to become ready.
- **Terminate** → delete the tunnel → delete the CNAME → revoke the AI Defense gateway connection key and the Splunk AO
  agent stream if the replica number is retired.

---

## 12. Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `nemotron-lightning` restarts, log says no compatible profile | one L40S is not enough for the auto-selected profile | apply the TP2 override in the overlay (§3) |
| Storefront works but no traces in Splunk AO | `SPLUNK_AO_API_KEY` empty, or wrong endpoint host (`console.` instead of `api.`) | fix `.env.workshop`, `docker compose restart` the four agents |
| Traces in Splunk AO but nothing in Splunk | collector cannot reach HEC, or index not allowed for the token | `docker logs otel-collector`; check `send_failed` metric; validate token/index |
| Every search fails after enabling the gateway | gateway rejects the bearer credential or cannot reach `nimN.<zone>` | test the gateway with `curl` and the gateway key; check Caddy bearer token; fall back to `--profile local-gateway` |
| Storefront answers but AI Defense shows no events | agents still point at the NIM directly | confirm `NIM_LLM_BASE_URL` in the agents' environment (`docker exec search-agent env`) |
| `git status` in the blueprint is not empty | someone edited the checkout | `git checkout -- . && git clean -fd`; put the change in the overlay instead |
