#!/usr/bin/env bash
# =============================================================================
# bootstrap.sh — raw Ubuntu 22.04 GPU box -> Agentic Observability with NVIDIA rig
#
# Idempotent. Run as root on the instance:
#   sudo REPLICA=1 ZONE=example.com TUNNEL_UUID=<uuid> ACCESS_KEY=<key> [NIM_BEARER=<token>] bash bootstrap.sh
#
# Expects the hand-over files (Spec §2.2) in /tmp:
#   /tmp/blueprint.env   -> /opt/Retail-Agentic-Commerce/.env
#   /tmp/workshop.env    -> /opt/AgenticObservabilityWithNvidia/deploy/.env.workshop
#   /tmp/tunnel.json     -> /root/.cloudflared/<TUNNEL_UUID>.json
# The blueprint checkout is pinned to v1.0.0 and NEVER modified.
# =============================================================================
set -euo pipefail

: "${REPLICA:?set REPLICA (1, 2, ...)}"
: "${ZONE:?set ZONE (DNS zone for acpN.<zone>)}"
: "${TUNNEL_UUID:?set TUNNEL_UUID}"
: "${ACCESS_KEY:?set ACCESS_KEY (storefront basic-auth password)}"
NIM_BEARER="${NIM_BEARER:-}"
BLUEPRINT_TAG="${BLUEPRINT_TAG:-v1.0.0}"
BLUEPRINT_DIR=/opt/Retail-Agentic-Commerce
WORKSHOP_DIR=/opt/AgenticObservabilityWithNvidia
NIM_CACHE=/opt/nim-cache
HOST="acp${REPLICA}.${ZONE}"
NIM_HOST="nim${REPLICA}.${ZONE}"

log() { printf '\n==> %s\n' "$*"; }

log "Preflight"
command -v nvidia-smi >/dev/null || { echo "nvidia-smi missing: use the Deep Learning Base OSS Nvidia Driver GPU AMI"; exit 1; }
nvidia-smi -L
docker compose version >/dev/null || { echo "Docker Compose v2 missing"; exit 1; }
for f in /tmp/blueprint.env /tmp/workshop.env /tmp/tunnel.json; do [ -s "$f" ] || { echo "missing hand-over file $f"; exit 1; }; done

log "Packages: cloudflared, caddy"
if ! command -v cloudflared >/dev/null; then
  curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg -o /usr/share/keyrings/cloudflare-main.gpg
  echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared jammy main" > /etc/apt/sources.list.d/cloudflared.list
fi
if ! command -v caddy >/dev/null; then
  apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
  curl -fsSL 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -fsSL 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' > /etc/apt/sources.list.d/caddy-stable.list
fi
apt-get update -q && apt-get install -y -q cloudflared caddy jq git

log "Blueprint checkout (pinned, pristine): $BLUEPRINT_DIR @ $BLUEPRINT_TAG"
if [ ! -d "$BLUEPRINT_DIR/.git" ]; then
  git clone --branch "$BLUEPRINT_TAG" --depth 1 https://github.com/NVIDIA-AI-Blueprints/Retail-Agentic-Commerce.git "$BLUEPRINT_DIR"
fi
git -C "$BLUEPRINT_DIR" status --porcelain | grep -q . && { echo "blueprint checkout is modified — refusing to continue"; exit 1; }

log "Workshop overlay checkout: $WORKSHOP_DIR"
if [ ! -d "$WORKSHOP_DIR/.git" ]; then
  git clone https://github.com/mayeack/AgenticObservabilityWithNvidia.git "$WORKSHOP_DIR"
else
  git -C "$WORKSHOP_DIR" pull --ff-only
fi

log "Env files and secrets"
install -m 600 /tmp/blueprint.env "$BLUEPRINT_DIR/.env"
install -m 600 /tmp/workshop.env  "$WORKSHOP_DIR/deploy/.env.workshop"
grep -q "^WORKSHOP_ENVIRONMENT=acp${REPLICA}$" "$WORKSHOP_DIR/deploy/.env.workshop" || echo "WARNING: WORKSHOP_ENVIRONMENT is not acp${REPLICA}"
mkdir -p "$NIM_CACHE" && chown 1000:1000 "$NIM_CACHE"
mkdir -p /root/.cloudflared && install -m 600 /tmp/tunnel.json "/root/.cloudflared/${TUNNEL_UUID}.json"
rm -f /tmp/blueprint.env /tmp/workshop.env /tmp/tunnel.json

log "NGC login"
set -a; . "$WORKSHOP_DIR/deploy/.env.workshop"; set +a
echo "$NGC_API_KEY" | docker login nvcr.io -u '$oauthtoken' --password-stdin

log "Caddy (access-key gate for the storefront, bearer gate for the NIM)"
sed -e "s|__HOST__|$HOST|g" -e "s|__NIM_HOST__|$NIM_HOST|g" -e "s|__NIM_BEARER__|$NIM_BEARER|g" \
    "$WORKSHOP_DIR/deploy/ec2/Caddyfile" > /etc/caddy/Caddyfile
HASH=$(caddy hash-password --plaintext "$ACCESS_KEY")
sed -i "s|__ACCESS_KEY_HASH__|$HASH|" /etc/caddy/Caddyfile
systemctl enable --now caddy && systemctl reload caddy

log "cloudflared"
mkdir -p /etc/cloudflared
sed -e "s|__TUNNEL_UUID__|$TUNNEL_UUID|g" -e "s|__HOST__|$HOST|g" -e "s|__NIM_HOST__|$NIM_HOST|g" \
    "$WORKSHOP_DIR/deploy/ec2/cloudflared.config.yml.example" > /etc/cloudflared/config.yml

log "systemd units"
sed -e "s|__BLUEPRINT_DIR__|$BLUEPRINT_DIR|g" -e "s|__WORKSHOP_DIR__|$WORKSHOP_DIR|g" \
    "$WORKSHOP_DIR/deploy/ec2/acp-stack.service"  > /etc/systemd/system/acp-stack.service
cp "$WORKSHOP_DIR/deploy/ec2/acp-tunnel.service" /etc/systemd/system/acp-tunnel.service
systemctl daemon-reload
systemctl enable --now acp-tunnel
docker network inspect acp-infra-network >/dev/null 2>&1 || docker network create acp-infra-network
systemctl enable --now acp-stack

log "Waiting for the NIMs (first start downloads the models: 10-20 min)"
for port in 8010 8011; do
  until curl -sf "http://localhost:${port}/v1/health/ready" >/dev/null; do sleep 15; printf '.'; done; echo " :$port ready"
done
curl -sf http://localhost/api/health >/dev/null && echo "storefront healthy"
git -C "$BLUEPRINT_DIR" status --porcelain | grep -q . && echo "WARNING: blueprint modified" || echo "blueprint as shipped (git status clean)"

log "Done. Storefront: https://$HOST  (user acp / the access key). Now validate Spec §8."
