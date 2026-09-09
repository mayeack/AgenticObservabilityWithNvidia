+++
title       = "Lab 4 — Govern"
description = "Splunk Core: the same spans and verdicts as immutable events — search them, correlate one session, and put the program on a dashboard."
duration    = "45 min"
weight      = 60
+++

![alt text](/images/image-32.png)

**Pillar:** Govern<br>
**Tool:** Splunk Core<br>
**Outcome:** Accountability & Evidence

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**Compliance / Audit** and **Security Operations**. Primary question: _For any session, can we show what the shopper sent, what the agent did, what the gateway decided, and what the model returned — on demand, months later?_
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Find your Lab 1 search and your Lab 3 attack in Splunk Core as events, correlate the trace with the Cisco AI Defense verdict, review the governance dashboard, and see the collector configuration that forwards it all over HTTP Event Collector.
{{% /notice %}}

## Background

Splunk Agent Observability answers the quality question and Cisco AI Defense answers the safety question, each in its own console. Splunk Core is where both records come to rest as immutable, searchable events, and where an auditor or an analyst can correlate them without exporting anything.

The path is the third addition. The agents' YAML carries a second exporter, of type `otelcollector`, pointed at an **OpenTelemetry Collector** container running beside the blueprint. The collector receives every span over OTLP and forwards it with the `splunk_hec` exporter to the **HTTP Event Collector** of the Splunk instance — one span per event, sourcetype `otel:traces`, with the storefront instance name stamped as `deployment.environment`. The agents' log files travel the same way. Cisco AI Defense events arrive through the **Cisco Security Cloud** app as sourcetype `cisco:ai:defense`.

## Labs

### Lab 4.1 Search the Spans

#### 4.1.1 Access Splunk

[How to Access Splunk Core](/workshops/agentic-observability-nvidia/01-setup/#4-how-to-access-splunk-core)

#### 4.1.2 Find Your Storefront's Spans

![alt text](/images/image-33.png)

In **Search & Reporting**, run (replacing the index with the one from your setup email):

```spl
index=acp sourcetype="otel:traces" "deployment.environment"=acp1
| spath
| table _time name "service.name" trace_id span_id "attributes.openinference.span.kind" "attributes.llm.token_count.total"
| sort -_time
```

Each span from Lab 1 is an event: the workflow, the agent, the tool, the LLM call. The `service.name` is the agent (`acp-search-agent`, `acp-recommendation-agent`, …), and the OpenInference span kind tells you which layer of the agent produced it.

#### 4.1.3 Tokens and Latency by Agent

![alt text](/images/image-34.png)

```spl
index=acp sourcetype="otel:traces" "attributes.openinference.span.kind"=LLM
| spath
| eval duration_ms = (end_time - start_time) / 1000000
| stats count sum("attributes.llm.token_count.total") AS tokens p95(duration_ms) AS p95_ms BY "service.name"
```

The same numbers Splunk Agent Observability showed per trace, now as an operating report across every session — and the basis for a cost allocation the retailer can defend.

### Lab 4.2 Search the Cisco AI Defense Events

![alt text](/images/image-35.png)

```spl
index=acp sourcetype="cisco:ai:defense" action=Blocked
| table _time application connection classifications rules severity event_id
| sort -_time
```

Your Lab 3 attack is here with the same classification and event identifier the console showed. The verdict is now part of the retailer's security record, in the same index as the spans it concerns.

### Lab 4.3 Correlate One Session

![alt text](/images/image-36.png)

Copy the `trace_id` of your Lab 1 search from Splunk Agent Observability, then:

```spl
index=acp ("trace_id"="<your trace id>" OR "event_id"="<your ai defense event id>")
| spath
| sort _time
| table _time sourcetype name "service.name" action classifications "attributes.input.value" "attributes.output.value"
```

One search returns the whole story in order: the shopper's input, each agent's action, the model's output, and — for the attacked session — the gateway's block. This is the record the auditor asks for and the analyst investigates from; it exists because every component wrote to the same place with the same identifiers.

### Lab 4.4 Review the Governance Dashboard

![alt text](/images/image-37.png)

Open **Dashboards -> Agentic Observability with NVIDIA**.

Requests by agent, p95 latency, tokens per agent, guardrail verdicts over time, and the last twenty traces with a drill-down into Lab 4.3's correlation search. Every number on the dashboard is one click from the events behind it.

### Lab 4.5 What Was Added

![alt text](/images/image-38.png)

The second exporter in each agent's YAML:

```yaml
      splunk_core:                   # added: OTLP to the local collector
        _type: otelcollector
        endpoint: ${OTEL_COLLECTOR_ENDPOINT:-http://otel-collector:4318/v1/traces}
        project: acp-search-agent
```

And the heart of the collector's configuration — receive OTLP, stamp the identity, forward over HEC:

```yaml
receivers:
  otlp:
    protocols:
      http: { endpoint: 0.0.0.0:4318 }
processors:
  resource/workshop:
    attributes:
      - { key: deployment.environment, value: "${env:WORKSHOP_ENVIRONMENT}", action: upsert }
exporters:
  splunk_hec/traces:
    endpoint: "${env:SPLUNK_HEC_URL}"
    token: "${env:SPLUNK_HEC_TOKEN}"
    index: "${env:SPLUNK_HEC_INDEX}"
    sourcetype: "otel:traces"
service:
  pipelines:
    traces: { receivers: [otlp], processors: [resource/workshop, batch], exporters: [splunk_hec/traces] }
```

The collector is the only new process on the instance. It holds the HEC token; the blueprint never sees it.

## Outcome

Every agent decision and every gateway verdict from the storefront is an immutable event in Splunk Core, correlated on the identifiers the components already shared. The auditor's question and the analyst's question have the same answer, in the same search.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Accountability & Evidence.** You can make every consequential agent decision attributable and explainable on demand, and hand security the same evidence for investigation without exporting anything by hand.
{{% /notice %}}

<!-- exec-outcome:end -->
