+++
title       = "Lab 1 — Measure"
description = "Splunk Agent Observability: evaluate different models, score them with evaluators, and surface the unknown unknowns."
duration    = "40 min"
weight      = 30
+++

![alt text](/workshops/ai-trust-open-weights/image-21.png)

**Pillar:** Measure<br>
**Tool:** Splunk Agent Observability<br>
**Outcome:** Improved Outcomes

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**AI / ML Platform leaders** and **AI Governance / Risk** teams. Primary question: _Is the AI actually any good — and can I measure quality and safety objectively, version over version?_ This is where subjective "it seems fine" becomes a defensible, repeatable score.
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Before you guard or operate anything, define and measure "good." You will see agentic turns scored by **Agent Observability**, read token/cost, and review the **signals** that surface the unknown unknowns.
{{% /notice %}}

## Background

Splunk Agent Observability evaluates the **whole agent trace** and scores each turn against industry standard risks (hallucination, context adherence, PII/PHI leakage, tool-selection quality) plus custom evaluators you define, such as Prescriptive Overreach. Evaluators can be run by **Luna** — Cisco's small, purpose-built evaluator models — so continuous LLM-as-judge scoring is affordable rather than a frontier-model bill.

Model evaluation, evaluator construction, and signal understanding is critical both to build trust in AI systems before deployment, and to monitor model drift over time.

## Labs

### Lab 1.1 Explore Prompting in PseudoCo Assistant

#### 1.1.1 Access PseudoCo Assistant

![alt text](/workshops/ai-trust-open-weights/image.png)

Click **Open PseudoCo Assistant**.

![alt text](/workshops/ai-trust-open-weights/image-11.png)

Ensure that the following fields are set:

- Application Theme: MedAdvice
- Provider: openai
- Model: nvidia/nemotron-3-super
- Static Emission: gpt-4o

#### 1.1.2 Explore PseudoCo Assistant's Behavior

![alt text](/workshops/ai-trust-open-weights/image-12.png)

The left side-panel manipulates the PseudoCo Assistant to produce aberrant behavior, such as toxic responses, synthetic PII, or prescriptive overreach.

![alt text](/workshops/ai-trust-open-weights/image-13.png)

The prompt library contains a set of sample prompts for you to explore.

#### 1.1.3 Prompt Aberrant Behavior

Explore sending various aberrant prompts and triggering non-compliant behavior. At minimum:

- Send a prompt with **Prescriptive Overreach** toggled on
- Send a prompt with **Include Synthetic PII/PHI in Responses** toggled on
- Send a prompt with various PII, such as a phone number, email address, SSN, or address
- Send a prompt with a toxic or aggressive tone
- Send a prompt with a prompt injection attempt

We will explore how this non-compliant behavior is monitored in subsequent sections.

### Lab 1.2 Monitor Behavior in Splunk Agent Observability

#### 1.2.1 Access Cisco Cloud Control

![alt text](/workshops/ai-trust-open-weights/image-14.png)

On the splash page, click **Execute** under **Cisco Cloud Control**.

![alt text](/workshops/ai-trust-open-weights/image-15.png)

Cisco Cloud Control provides you a single, centralized access point to all of the applications in the OneCisco suite of products, with one login.

Click the nine dots in the upper left corner.

![alt text](/workshops/ai-trust-open-weights/image-16.png)

Click **Agent Observability** under **Apps**.

#### 1.2.2 Review Agent Observability Overview

![alt text](/workshops/ai-trust-open-weights/image-17.png)
![alt text](/workshops/ai-trust-open-weights/image-18.png)
![alt text](/workshops/ai-trust-open-weights/image-19.png)

Ensure that the following filters are set:

- Project: PseudoCo Assistant
- Agent stream: MedAdvice

**Overview**: Displays the selected AI project and agent stream, with filters for time range.
**Usage and performance**: Summarizes total requests, tool and LLM failures, token consumption, and estimated agent cost.
**Signals generated**: Surfaces detected AI trust and safety issues, including harmful responses, unlicensed medical advice, and sensitive PII.
**Controls applied**: Shows which governance controls were triggered and whether activity was observed, denied, steered, or allowed to proceed without a trigger.
**Evaluator trends**: Tracks evaluator results over time, including action completion, context adherence, and tool selection quality.

![alt text](/workshops/ai-trust-open-weights/image-20.png)

Click **View project details** to drill into Agent Observability.

#### 1.2.3 Review Agent Stream

![alt text](/workshops/ai-trust-open-weights/image-10.png)

Click on **MedAdvice**.

![alt text](/workshops/ai-trust-open-weights/image-23.png)

The **Agent Stream**  turns every live AI conversation into a graded, searchable record — the continuous audit trail that proves the application is behaving safely in production.

Logs — The running ledger of real user interactions, capturing what went in and what the AI sent back. This is the system of record that makes behavior observable and reviewable rather than a black box.

Automated scoring (such as Output Toxicity, Prescriptive Overreach, Output PII) — Every response is auto-graded against safety and quality measures, including custom risk checks tuned to this use case. This is the core value: thousands of interactions evaluated without human review, with problematic responses surfaced automatically for attention.

Click on any trace.

![alt text](/workshops/ai-trust-open-weights/image-24.png)

This single-trace view is the microscope of the platform — it opens up one AI conversation end to end, showing exactly how a multi-step agent produced its answer and how that answer scored on quality and safety.

Trace tree (Session → chat turn → agents) — Exposes the full chain of reasoning behind one response, including the specialist agents and underlying model that handled it. This turns a single answer into a traceable, explainable record — essential when you need to prove why the AI said what it said.

Input / Output panel — Shows the exact user request and the verbatim response side by side. This is the ground truth for any review, audit, or dispute — what was actually asked, and what was actually returned.

Evaluators — One trace, examined from every angle: how it scored, how it was configured, human notes, and flagged risks. The value is a complete case file for any interaction worth investigating.

Feel free to explore the other tabs, such as **Latency** and **Trace Graph**.

#### 1.2.4 Review Signals

![alt text](/workshops/ai-trust-open-weights/image-25.png)

Click the back arrow to return to the **Agent Stream**.

![alt text](/workshops/ai-trust-open-weights/image-26.png)

Click on **Signals**. 

![alt text](/workshops/ai-trust-open-weights/image-27.png)

The Signals panel is the AI watching the AI — it scans every logged conversation for risk patterns and surfaces them as named, prioritized issues, so the team learns where the application is failing without reading transcripts one by one. Whereas Evaluators need to be defined by the user, Signals surface the unknown unknown issues.

Click on any signal.

![alt text](/workshops/ai-trust-open-weights/image-28.png)

**Signal summary**: Identifies an Unlicensed Medication Advice signal where the LLM provided prescription guidance to a user without sufficient medical or identity context.
**Scope and impact**: Shows the affected spans, traces, and sessions associated with the signal, along with when the issue was created and last updated.
**Root cause analysis**: Explains the behavior that triggered the signal and links it to the relevant policy or prompt enforcement gap.
**Recommendation**: Provides a suggested remediation, in this case adding a pre-check to verify user identity before medication advice is given.
**Evidence details**: Visualizes when affected spans occurred and provides example interactions that contributed to the signal.
**Trace linkage**: Lets the user drill into the underlying session, trace, and span for direct investigation of the agent behavior.

#### 1.2.5 Review Trends

![alt text](/workshops/ai-trust-open-weights/image-29.png)

Click on **Trends**.

![alt text](/workshops/ai-trust-open-weights/image-30.png)

The Trends view is the over-time picture of AI quality and risk — it tracks whether the application is holding steady, improving, or drifting, turning a snapshot of scores into a story leadership can monitor like any other business metric.

Scroll down to **System Metrics**.

The System Metrics view is the operational and cost dashboard for the AI — alongside quality and safety, it tracks consumption, spend, reliability, and volume, so the application is run like a managed business asset, not an unmonitored experiment.

Token metrics (Input, Output, Num Input/Output, Total Tokens) — Measure how much the AI is consuming to do its work. Because tokens are the unit of cost, this is the direct lever on what the application spends — and the early signal if usage suddenly balloons.

API Failures — Counts how often the underlying service broke. This is the reliability gauge — proof the application is actually up and serving users, and an immediate flag when it isn't.

Traces Count — Tracks total volume of activity. This sizes the workload and gives every other metric context — quality and cost only mean something against how much the system is handling.

Agent Cost — Translates that consumption into dollars. This is the line item leadership actually cares about: what is this AI costing us, tracked over time so spend never becomes a surprise.

Feel free to explore additional metric charts, such as those under **Safety Metrics** and **Custom Evaluators**.

### Lab 1.3 Evaluators

#### 1.3.1 Review Evaluators

![alt text](/workshops/ai-trust-open-weights/image-31.png)

Click on **Agent Observability -> Evaluators**.

![alt text](/workshops/ai-trust-open-weights/image-32.png)

The Evaluators catalog is the rulebook for how every AI is graded — a central, reusable library of scoring criteria that makes "good" and "safe" mean the same thing across every project and every team. As you have seen, Evaluators are leveraged at every point in the development and deployment lifecycle.

#### 1.3.2 Review Prescriptive Overreach Evaluator

NOTE: This custom evaluator needs to be added to the dCloud instance

![alt text](/images/image-208.png)

Search for **prescriptive_overreach**, and click on it.

![alt text](/images/image-209.png)

This is where a safety standard gets authored — the editor for a custom Prescriptive Overreach Evaluator, showing how an abstract risk is turned into a precise, automated, repeatable test that every AI response is graded against.

Configure Input (LLM model / Apply to) — Chooses which AI does the grading and what part of the conversation it judges. The value is deliberate control over how rigorous and how targeted the evaluation is.

Prompt (the scoring rubric) — The heart of it: explicit instructions and graded anchors that define exactly what counts as a minor lapse versus an egregious violation. This converts a fuzzy worry — "is the bot making up medical facts?" — into a consistent, defensible score that doesn't drift with opinion. You can use the **Help me write** toggle to enhance your prompts.

Configure Output (type & roll-up) — Sets how individual scores combine into a single number that rolls up across the whole experiment. This is what makes one response's grade aggregate into a board-level quality figure.

## Outcome

**Splunk Agent Observability** turns AI development from a black box into a measurable discipline you can trust. Using PseudoCo Assistant participants see firsthand how non-compliant AI behavior is automatically detected, scored, and contained.

The journey walks through five capabilities that make trust measurable:

**Monitor** — Logs capture every live AI interaction as a searchable, auto-graded audit trail, so production behavior is observable and reviewable rather than a black box.

**Detect the unknown** — Signals surface risks no one thought to define (PII leakage, medical hallucinations, harassment), catching the "unknown unknowns" before they become incidents.

**Investigate** — Trace-level detail opens any single conversation end to end, providing a defensible case file of how and why the AI answered as it did.

**Track over time** — Trends chart quality, risk, cost, and reliability day by day, giving leadership early warning of drift and a clear line of sight into spend.

**Standardize** — A central evaluator catalog defines what "good" and "safe" mean once and applies it everywhere, with each evaluator authored as a precise, version-controlled rubric.

The takeaway: AI risk becomes quantifiable and auditable. Safety, quality, and cost are measured continuously and automatically — at scale, without human review of every interaction — giving the business the defensible evidence it needs to deploy AI with confidence.

Now that we have identified the critical evaluator Prescriptive Overreach, let's operationalize that in **Cisco AI Defense**.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Improved Outcomes.** You turn AI quality, safety, and cost into measurable operating metrics rather than subjective judgments. You can establish a baseline before release, identify emerging risks in production, and continuously improve the agent against evidence.
{{% /notice %}}

<!-- exec-outcome:end -->
