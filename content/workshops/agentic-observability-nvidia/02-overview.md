+++
title       = "Architecture Overview"
description = "One trace, four consoles: the blueprint as shipped, plus three additions applied as configuration."
duration    = "15 min"
weight      = 20
+++

![alt text](/images/image-5.png)

**Pillar:** Architecture Overview<br>
**Tool:** NVIDIA AI Blueprint + Splunk + Cisco<br>
**Outcome:** Unified Visibility & Control

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**AI Platform leaders** and the **CIO / CTO** who own the decision to run NVIDIA-built agents in production. Primary question: _Can we instrument, secure, and govern an agent we did not write — without forking it?_ Security, SRE, and compliance leaders use this page as the map for their own lab.
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Establish the thesis: the blueprint runs exactly as NVIDIA ships it, three additions are applied beside it as configuration, and one OpenTelemetry trace carries every agent decision into every console.
{{% /notice %}}

## Background

The NVIDIA Retail Agentic Commerce blueprint is a complete agentic storefront: a Next.js shopper UI, a merchant API that speaks the Agentic Commerce Protocol and the Universal Commerce Protocol, a payment service, and four NeMo Agent Toolkit agents — **search**, **recommendation**, **promotion**, and **post-purchase** — that reason on Nemotron 3.5 Lightning and retrieve with Nemotron 3 Embed over Milvus. Both models run as NVIDIA NIM microservices on the GPUs of a single AWS instance.

NeMo Agent Toolkit is the reason the additions are configuration and not code. Every agent is defined by a YAML file: which model it calls, which tools it has, and — under `general.telemetry.tracing` — where its OpenTelemetry spans go. The blueprint already ships one exporter there, for Arize Phoenix. The workshop adds two more.

The three additions:

- **Observe** — a `galileo`-type exporter in each agent's YAML sends spans directly to **Splunk Agent Observability**; a second, `otelcollector`-type exporter sends the same spans to a local OpenTelemetry Collector.
- **Secure** — the agents' `NIM_LLM_BASE_URL` points at a **Cisco AI Defense** gateway instead of the NIM directly; the gateway inspects every prompt and response against runtime policy, then forwards to the NIM.
- **Govern** — the OpenTelemetry Collector forwards spans and container logs over HTTP Event Collector to **Splunk Core**, where the Cisco AI Defense events also land.

The four YAML files and the Compose overlay that carry these additions live outside the blueprint checkout. `git diff` inside the blueprint is empty.

## Labs

### 1. Open the Storefront and the Agent Activity Panel

![alt text](/images/image-6.png)

Open the storefront and expand the **Agent Activity** panel. Search for a product. Each agent call appears as it happens — the search agent's retrieval, the recommendation agent's picks, the promotion agent's decision — with the protocol messages behind it.

This panel is the blueprint's own view of its agents. Everything you see here is what the additions will carry into Splunk and Cisco AI Defense: the same calls, the same order, the same identifiers.

### 2. Review the Architecture

![alt text](/images/image-3.png)

Trace one search through the diagram: shopper UI → merchant API → search agent → Cisco AI Defense gateway → Nemotron NIM, with the span fan-out from the agent to Splunk Agent Observability and, through the collector, to Splunk Core.

Three things to notice. The blueprint components are unchanged. The gateway sits on the network path, not in the code. The collector is the only new process, and it does nothing but forward.

### 3. Review What Was Added — and What Was Not

![alt text](/images/image-7.png)

This is the entire diff between the blueprint's search-agent YAML and the workshop's copy: two exporter blocks under `tracing`. The promotion, recommendation, and post-purchase agents carry the same two blocks. No Python was changed, no image was rebuilt, no prompt was edited.

The additions are auditable because they are small. That is the pattern this workshop teaches: instrument beside the blueprint, not inside it, so NVIDIA's next release drops in without re-applying anything.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Unified Visibility & Control.** You can put an NVIDIA-built agent into production and see every decision it makes, in every console that needs it, without forking the blueprint or waiting for the next release to carry your instrumentation.
{{% /notice %}}

<!-- exec-outcome:end -->
