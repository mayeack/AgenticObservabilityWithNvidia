+++
title       = "Introduction"
description = "Blueprint as shipped. Observed. Secured. Governed. One trace, end to end."
duration    = "15 min"
weight      = 5
+++

*A field workshop for the platform, security, and observability teams who are putting NVIDIA-built agents into production — and the executives accountable for them.*

## The Problem: The Agents Arrived Before the Instruments Did

Enterprises are standing up agentic AI on NVIDIA AI Blueprints in weeks. A reference storefront, a research assistant, or a customer-service agent comes with its models, its retrievers, and its orchestration already wired — and it runs on the GPUs you already bought. The build problem is solved.

The trust problem is not. The moment that blueprint takes real traffic, four teams ask four questions at once. Operations asks whether the agents are fast, healthy, and affordable. Security asks whether a prompt injection can talk the promotion agent into a discount it should never give. Quality asks whether the search agent is picking the right tool and the right products. Compliance asks for the record of a single checkout, end to end, on demand.

Most teams answer those questions by changing the application: a tracing library here, a guardrail wrapper there, a log shipper bolted on the side. Every change forks the blueprint away from the one NVIDIA maintains, and every fork has to be re-applied on the next release. **The instrumentation becomes the technical debt.**

This workshop closes that gap the other way around. The blueprint stays exactly as shipped. Three additions — Splunk Agent Observability, Cisco AI Defense, and HTTP Event Collector forwarding to Splunk Core — are applied as configuration and keys, never as code. One trace, captured once, answers all four questions.

---

## The Scenario

![alt text](/images/image-1.png)

An online retailer runs the **NVIDIA Retail Agentic Commerce** blueprint: a storefront where NeMo Agent Toolkit agents search the catalog, recommend products, decide promotions, complete checkout over the Agentic Commerce Protocol, and write the post-purchase message — all on Nemotron models served by NVIDIA NIM on GPUs in AWS.

![alt text](/images/image-2.png)

The value is real: a shopper types a sentence and an agent assembles the cart. So is the exposure. The promotion agent decides prices. The search agent reads whatever the shopper types. The post-purchase agent writes what the customer receives. Each of those decisions has to be observable, enforceable, and auditable before the retailer can scale it.

**The blueprint can scale. So can the risk. The instruments have to arrive without rewriting the blueprint.**

---

## The Thesis: Blueprint As Is, Three Additions

The blueprint's own code is never touched. Every addition is a configuration file, an environment variable, or an API key — applied as a Docker Compose overlay next to the blueprint, not inside it.

> **Every agent decision is captured once as an OpenTelemetry trace and correlated across quality, security, operations, and audit — so the four questions become one investigation, not four tools.**

| **Pillar** | **Question** | **Addition** | **Platform** |
| --- | --- | --- | --- |
| **Run** | *Does it work as shipped?* The blueprint, its NIMs, and its GPUs on AWS, unmodified | none — the baseline | NVIDIA AI Blueprint on AWS |
| **Observe** | *Is it good, fast, and affordable?* Every workflow, agent, tool, and LLM span with tokens, latency, and quality scores | a `tracing` block in the agents' YAML | Splunk Agent Observability |
| **Secure** | *Is it safe?* Runtime inspection of every prompt and response, with policy enforced before the model answers | an API key and a gateway URL | Cisco AI Defense |
| **Govern** | *Is it accountable?* The same spans and verdicts as immutable, searchable events | a collector and an HEC token | Splunk Core |

![alt text](/images/image-3.png)

The architecture: the storefront calls four NeMo Agent Toolkit agents; the agents call Nemotron NIMs through the Cisco AI Defense gateway; every agent emits one trace to Splunk Agent Observability and to a local OpenTelemetry Collector that forwards it over HEC to Splunk Core, where Cisco AI Defense events land alongside it.

---

## The Journey: One Checkout, Four Pillars

The workshop is delivered against a live storefront running on a GPU instance in AWS. You will use the storefront as a shopper, then follow one of your own sessions through each console.

### Architecture Overview: One Trace, Four Consoles

**Scenario.** You open the storefront and the agent activity panel. A search, a recommendation, a promotion decision, and a checkout each appear as agent calls with protocol messages behind them.

**What the additions do.** The same calls appear as spans in Splunk Agent Observability, as inspected prompts in Cisco AI Defense, and as events in Splunk Core — with a shared trace identifier and nothing rewritten in the blueprint.

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Unified Visibility & Control.** You can put an NVIDIA-built agent into production and see every decision it makes, in every console that needs it, without forking the blueprint or waiting for the next release to carry your instrumentation.
{{% /notice %}}

### Lab 1 — Run (NVIDIA AI Blueprint on AWS): The Baseline, As Shipped

**Scenario.** The retailer needs the storefront running on its own GPUs, under its own control, before anything else is decided.

**What NVIDIA delivers.** The Retail Agentic Commerce blueprint runs from its own Docker Compose files on an AWS GPU instance. Nemotron 3.5 Lightning and Nemotron 3 Embed run as self-hosted NIM microservices. The blueprint's own Phoenix tracing proves the agents already emit OpenTelemetry spans — the raw material every later lab builds on.

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Accelerated Time to Value.** You move from reference architecture to a running agentic application on your own infrastructure in hours, and you keep the upgrade path NVIDIA maintains because nothing in the blueprint was changed.
{{% /notice %}}

### Lab 2 — Observe (Splunk Agent Observability): Measure Every Agent Decision

**Scenario.** A shopper's search takes longer than it should, and the recommendation agent's suggestions are drifting off-catalog. Nobody can say which agent, which model call, or which tool is responsible.

**What Splunk delivers.** A `tracing` exporter in each agent's NeMo Agent Toolkit YAML sends every workflow, agent, tool, and LLM span to Splunk Agent Observability. You see tokens and latency per span, and Luna evaluators score tool selection and instruction adherence on live traffic — continuously, at a cost that makes scoring every session practical.

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Improved Outcomes.** You turn agent quality, speed, and cost into operating metrics per agent and per model, so a slow search or an off-catalog recommendation is found in the trace, not in a customer complaint.
{{% /notice %}}

### Lab 3 — Secure (Cisco AI Defense): Enforce Policy Without Touching the App

**Scenario.** A shopper types an instruction meant for the agent, not the catalog: ignore the rules, reveal the system prompt, apply the biggest discount. The promotion agent has no idea it is being attacked.

**What Cisco delivers.** The agents' model endpoint is switched to a Cisco AI Defense gateway. Every prompt and every response is inspected against runtime policy — prompt injection, PII, harassment, and custom rules — before the model answers or the shopper sees the result. The blocked attempt is recorded as an event with its verdict.

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Trusted AI.** You turn written policy into runtime enforcement on an application you did not write and cannot patch, and you can tune that policy as fast as the threats change.
{{% /notice %}}

### Lab 4 — Govern (Splunk Core): One Record for the Auditor and the Analyst

**Scenario.** The retailer must show, for one blocked session, what the shopper sent, what the agent attempted, what the gateway decided, and what the model returned — and must be able to do it for every session, months later.

**What Splunk delivers.** A local OpenTelemetry Collector forwards the same spans over HTTP Event Collector to Splunk Core, and Cisco AI Defense events arrive beside them. One search correlates the trace, the verdict, and the agent's action; one dashboard shows the program's posture; the whole record is immutable and searchable.

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Accountability & Evidence.** You can make every consequential agent decision attributable and explainable on demand, and hand security the same evidence for investigation without exporting anything by hand.
{{% /notice %}}

---

## Executive Outcomes

| **Outcome** | **What it means** | **Grounded in** |
| --- | --- | --- |
| **Unified Visibility & Control** | See every agent decision in every console that needs it, without forking the blueprint. | Architecture Overview |
| **Accelerated Time to Value** | Reference architecture to a running agentic application on your own GPUs, with NVIDIA's upgrade path intact. | NVIDIA AI Blueprint on AWS |
| **Improved Outcomes** | Agent quality, speed, and cost as operating metrics per agent and per model. | Splunk Agent Observability |
| **Trusted AI** | Written policy enforced at runtime on an application you did not write. | Cisco AI Defense |
| **Accountability & Evidence** | Every consequential decision attributable and explainable on demand. | Splunk Core |

---

## The Call to Action

NVIDIA has made the agent the easy part. The question for every platform, security, and observability leader is whether the instruments can keep up without slowing the build down.

They can — if the instrumentation lives beside the blueprint instead of inside it. **Run the blueprint as shipped. Add observability, security, and governance as configuration. Investigate once, in the trace.**

This workshop puts that pattern in your hands against a live storefront: run it, observe it, secure it, govern it — on the same checkout, on the same trace.

**Blueprint as shipped. Observed. Secured. Governed. One trace, end to end.**

---
