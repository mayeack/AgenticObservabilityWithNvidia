# From Open Weights to Trusted Outcomes

Customer-facing site for the **From Open Weights to Trusted Outcomes: Building Enterprise AI You Can Control with
Cisco and NVIDIA** workshop, published with GitHub Pages at:

**https://mayeack.github.io/AgenticObservabilityWithNvidia/**

A hands-on workshop on a multi-agent healthcare assistant running on Cisco Secure AI Factory with NVIDIA, using
NVIDIA NIM microservices and Nemotron open models. Two labs turn open-weight control into proven trust:

1. **Lab 1 — Measure (Splunk Agent Observability)** — measure every agent interaction against trust criteria and
   surface hallucination, PII/PHI leakage, prompt injection, and prescriptive overreach.
2. **Lab 2 — Secure (Cisco AI Defense)** — turn the Lab 1 finding into a runtime guardrail and prove it against the
   live application.

Open models provide the intelligence, continuous evaluation provides the evidence, and runtime enforcement keeps AI
aligned with intended business outcomes.

## Stack

Hugo (0.161+ extended) with the [splunk/hugo-theme-splunk-workshop](https://github.com/splunk/hugo-theme-splunk-workshop)
theme, vendored as a git submodule at `themes/hugo-theme-splunk-workshop`. The site is built and published by GitHub
Actions (`.github/workflows/pages.yml`) on every push to `main` (repo Settings → Pages → Source must be "GitHub Actions").

## Layout

- `content/_index.md` — Home (hero + the opening narrative section). **Generated** by `build_index.py`; do not hand-edit the body.
- `content/workshops/ai-trust-open-weights/` — the workshop pages: `00-introduction.md` (the narrative source of truth),
  `01-setup.md`, `03-lab-1-measure.md`, `04-lab-2-secure.md`, `07-wrap-up.md`.
  Sidebar order comes from `weight` in each page's front matter.
- `static/images/` — screenshots, referenced as `/images/image-NN.png`. Screenshots pasted into the workshop folder are referenced as `/workshops/ai-trust-open-weights/image-N.png`.
- `hugo.toml` — site config and theme params (branding, colors, layout toggles).

## Editing

```bash
git clone --recurse-submodules https://github.com/mayeack/AgenticObservabilityWithNvidia.git
hugo server          # local preview at http://localhost:1313/AgenticObservabilityWithNvidia/
```

Commit to `main` and push — the Pages workflow rebuilds the site (~1–2 min).

## Conventions

- **Customer-facing.** No internal sales positioning or facilitator-only delivery notes on the site.
- **The Introduction page is the narrative source of truth.** Edit `00-introduction.md`, then run
  `python3 build_index.py`; it regenerates Home's body, exports `../collateral/1 - narrative.md`, and re-syncs the two
  Executive-outcome callouts onto the lab pages (between the `<!-- exec-outcome:start/end -->` markers).
- **Callout standards** (theme `notice` shortcode): Executive outcomes `{{% notice style="info" title="Executive outcome" icon="star" %}}`
  (generated — never hand-edit between the markers); lab objectives `title="Objective" icon="target"`; personas
  `title="Who this is for" icon="users"` between the `<!-- persona:start/end -->` markers; operational asides
  `{{% notice note %}}`; cautions `{{% notice warning %}}`.
- "Lorem ipsum" marks a section that is intentionally not written yet.
