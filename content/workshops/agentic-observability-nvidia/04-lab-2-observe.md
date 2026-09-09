+++
title       = "Lab 2 — Observe"
description = "Splunk Agent Observability: follow one search through every agent, tool, and model span, then let Luna score it."
duration    = "45 min"
weight      = 40
+++

![alt text](/images/image-16.png)

**Pillar:** Observe<br>
**Tool:** Splunk Agent Observability<br>
**Outcome:** Improved Outcomes

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**SRE / Observability** and **AI / ML Platform** teams, with **FinOps**. Primary question: _Which agent, which tool, and which model call made this session slow, expensive, or wrong — and can we score every session, not a sample?_
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Find the trace for the search you ran in Lab 1, read its workflow, agent, tool, and LLM spans with tokens and latency, turn on Luna evaluators for the agent stream, and see the eight-line YAML addition that made all of it possible.
{{% /notice %}}

## Background

Splunk Agent Observability is the evaluation and observability platform for agentic applications. It ingests OpenTelemetry traces that follow the OpenInference and GenAI semantic conventions — exactly what NeMo Agent Toolkit agents emit — and organises them into **projects** and **agent streams**. On every span it records the input, the output, the model, token counts, and latency. **Luna**, its family of purpose-built small evaluator models, scores agent behaviour continuously: tool selection, instruction adherence, context adherence, and more, at a cost that makes scoring every production session practical rather than aspirational.

The blueprint reached it without a new library. NeMo Agent Toolkit ships a `galileo`-type telemetry exporter — the OTLP integration Splunk Agent Observability accepts — so the workshop added one block under `general.telemetry.tracing` in each agent's YAML, pointed at the Splunk Agent Observability endpoint with the project, agent stream, and API key from the environment. The Phoenix exporter NVIDIA shipped stays in place; the same spans now go to both.

## Labs

### Lab 2.1 Open Your Agent Stream

#### 2.1.1 Access Splunk Agent Observability

[How to Access Splunk Agent Observability](/workshops/agentic-observability-nvidia/01-setup/#2-how-to-access-splunk-agent-observability)

#### 2.1.2 Open the Project

![alt text](/images/image-17.png)

Open the project **RetailAgenticCommerce**, then the agent stream named after your storefront instance (for example **acp1**).

The agent stream is the live record of everything your storefront's agents did. Every search, recommendation, promotion decision, and post-purchase message from Lab 1 is here as a trace — captured by the exporter, not by any code in the blueprint.

### Lab 2.2 Find Your Search

#### 2.2.1 Filter the Stream

![alt text](/images/image-18.png)

Filter by time to the minutes you spent in Lab 1, or search the input column for the words you typed. Select the trace for your product search.

#### 2.2.2 Read the Span Tree

![alt text](/images/image-19.png)

The trace has the shape you saw in Phoenix: a **workflow** span, the **agent** span beneath it, the **product_search** tool span with the retrieved candidates, and the **LLM** span with the full prompt and completion from Nemotron 3.5 Lightning.

Select the LLM span. Input tokens, output tokens, and latency are recorded on it. This is the unit of cost and speed for the whole application: every token the storefront spends is attributable to a span, an agent, and a session.

#### 2.2.3 Compare Agents

![alt text](/images/image-20.png)

Open a recommendation trace next to your search trace. The recommendation agent plans, retrieves, and ranks in separate steps, so its tree is deeper and its token total higher. This is the comparison FinOps needs: which agent carries the cost, and whether that cost buys a better outcome.

### Lab 2.3 Score Every Session with Luna

#### 2.3.1 Configure Evaluators

![alt text](/images/image-21.png)

Open the agent stream's evaluator settings and enable **Tool Selection Quality**, **Instruction Adherence**, and **Context Adherence**. Each is a Luna evaluator: a small model trained for that judgement, run on every new trace in the stream.

#### 2.3.2 Read the Scores

![alt text](/images/image-22.png)

Return to your search trace. The scores appear on the spans they judge: did the search agent pick the right tool, did the model follow the agent's instructions, did the answer stay inside the retrieved catalog context. A low context-adherence score on a recommendation is the off-catalog drift from the scenario — found in the trace, before a shopper reports it.

### Lab 2.4 What Was Added

![alt text](/images/image-7.png)

This is the block the workshop added to `search.yml`, and identically to the other three agents. Everything above it is NVIDIA's; everything in it is configuration:

```yaml
general:
  telemetry:
    tracing:
      phoenix:                       # shipped by NVIDIA — unchanged
        _type: phoenix
        project: "search-agent"
        endpoint: ${PHOENIX_ENDPOINT:-http://localhost:6006/v1/traces}
      splunk_ao:                     # added: Splunk Agent Observability
        _type: galileo
        endpoint: ${SPLUNK_AO_OTEL_ENDPOINT}
        project: ${SPLUNK_AO_PROJECT}
        logstream: ${SPLUNK_AO_AGENT_STREAM}
        api_key: ${SPLUNK_AO_API_KEY}
```

The values come from the environment, so the same YAML serves every storefront instance; only the agent stream name changes. No SDK was installed into the blueprint's image, and the blueprint's own exporter still runs.

## Outcome

Every agent decision in the storefront is now measured — tokens, latency, and Luna quality scores per span, per agent, per session — and the application that produced them is still byte-for-byte the blueprint NVIDIA ships.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Improved Outcomes.** You turn agent quality, speed, and cost into operating metrics per agent and per model, so a slow search or an off-catalog recommendation is found in the trace, not in a customer complaint.
{{% /notice %}}

<!-- exec-outcome:end -->
