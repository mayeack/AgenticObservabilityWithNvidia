# Agent configs — the only YAML the workshop changes

- `upstream/` — byte-for-byte copies of `src/agents/configs/*.yml` from
  [NVIDIA-AI-Blueprints/Retail-Agentic-Commerce @ v1.0.0](https://github.com/NVIDIA-AI-Blueprints/Retail-Agentic-Commerce/tree/v1.0.0/src/agents/configs)
  (commit `3df75e7`). Never edit.
- `configs/` — the same four files plus the workshop additions under `general.telemetry`:
  a `file` logger (addition c), a `galileo`-type exporter (addition a, Splunk Agent Observability) and an
  `otelcollector`-type exporter (addition c, local collector → Splunk HEC).
- `workshop.diff` — `diff -ru upstream configs`; regenerate after any change and show it on the lab pages.

The Compose overlay bind-mounts `configs/` over `/app/configs` in the four `nat-agents` containers, so the
blueprint's image and checkout stay untouched. Exporter types `galileo` and `otelcollector` are registered by
`nvidia-nat-opentelemetry`, which the image already has through the `nvidia-nat[phoenix]` extra (NAT 1.7.0).
