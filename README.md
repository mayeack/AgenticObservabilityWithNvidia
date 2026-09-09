# Agentic Observability with NVIDIA

Customer-facing site for the **Agentic Observability with NVIDIA** workshop, published with GitHub Pages at:

**https://mayeack.github.io/AgenticObservabilityWithNvidia/**

A hands-on workshop that runs the [NVIDIA Retail Agentic Commerce](https://github.com/NVIDIA-AI-Blueprints/Retail-Agentic-Commerce)
blueprint **exactly as shipped** on a GPU instance in AWS and adds three things as configuration — never as code:

1. **Splunk Agent Observability** — a `galileo`-type OpenTelemetry exporter in each NeMo Agent Toolkit agent's YAML.
2. **Cisco AI Defense** — an AI Defense Gateway connection in front of the self-hosted Nemotron NIM (two env vars).
3. **HEC forwarding to Splunk Core** — an OpenTelemetry Collector that ships the same spans and the agent logs to Splunk.

Four labs — Run, Observe, Secure, Govern — on one storefront and one trace.

## Stack

Hugo (0.161+ extended) with the [splunk/hugo-theme-splunk-workshop](https://github.com/splunk/hugo-theme-splunk-workshop)
theme, vendored as a git submodule at `themes/hugo-theme-splunk-workshop`. The site is built and published by GitHub
Actions (`.github/workflows/pages.yml`) on every push to `main` (repo Settings → Pages → Source must be "GitHub Actions").

## Layout

- `content/_index.md` — Home (hero + the opening narrative section). **Generated** by `build_index.py`; do not hand-edit the body.
- `content/workshops/agentic-observability-nvidia/` — the workshop pages: `00-introduction.md` (the narrative source of truth),
  `01-setup.md`, `02-overview.md`, `03-lab-1-deploy.md` … `06-lab-4-govern.md`, `07-wrap-up.md`, `08-reference.md`.
  Sidebar order comes from `weight` in each page's front matter.
- `static/images/` — screenshots, referenced as `/images/image-NN.png`. Placeholders ship until the rig is captured.
- `hugo.toml` — site config and theme params (branding, colors, layout toggles).
- `deploy/` — the workshop overlay for the AWS rig: agent configs, Compose overlay, collector, gateway fallback, EC2
  spec/runbook/bootstrap, Splunk searches and dashboard. See [deploy/README.md](deploy/README.md).

## Editing

```bash
git clone --recurse-submodules https://github.com/mayeack/AgenticObservabilityWithNvidia.git
hugo server          # local preview at http://localhost:1313/AgenticObservabilityWithNvidia/
```

Commit to `main` and push — the Pages workflow rebuilds the site (~1–2 min).

## Conventions

- **Customer-facing.** No internal sales positioning or facilitator-only delivery notes on the site. Facilitator
  material (rig build, keys, cost) lives under `deploy/ec2/`.
- **The Introduction page is the narrative source of truth.** Edit `00-introduction.md`, then run
  `python3 build_index.py`; it regenerates Home's body, exports `../collateral/1 - narrative.md`, and re-syncs the five
  Executive-outcome callouts onto the overview/lab pages (between the `<!-- exec-outcome:start/end -->` markers).
- **Callout standards** (theme `notice` shortcode): Executive outcomes `{{% notice style="info" title="Executive outcome" icon="star" %}}`
  (generated — never hand-edit between the markers); lab objectives `title="Objective" icon="target"`; personas
  `title="Who this is for" icon="users"` between the `<!-- persona:start/end -->` markers; operational asides
  `{{% notice note %}}`; cautions `{{% notice warning %}}`.
- **The blueprint is never edited.** Anything the rig needs goes in `deploy/` and is shown on the lab pages as a diff
  against the upstream file, so the "as shipped" claim stays auditable.
- "Lorem ipsum" marks a section that is intentionally not written yet.
