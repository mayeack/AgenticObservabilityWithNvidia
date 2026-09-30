+++
title       = "Lab 1 — Measure"
description = "Splunk Agent Observability: evaluate different models, score them with evaluators, and surface the unknown unknowns."
duration    = "40 min"
weight      = 30
+++

![alt text](/images/image-123.png)

**Pillar:** Measure<br>
**Tool:** Splunk Agent Observability<br>
**Outcome:** Improved Outcomes

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**AI / ML Platform leaders** and **AI Governance / Risk** teams. Primary question: _Is the AI actually any good — and can I measure quality and safety objectively, version over version?_ This is where subjective "it seems fine" becomes a defensible, repeatable score.
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Before you guard or operate anything, define and measure "good." You will run a **baseline-vs-poisoned** evaluation, see it scored by **Luna**, read token/cost, and the **signals** that surface the unknown unknowns.
{{% /notice %}}

## Background

Splunk Agent Observability evaluates the **whole agent trace** and scores each turn against research-backed metrics (hallucination, context adherence, PII/PHI leakage, tool-selection quality) plus custom evaluators you define, such as Prescriptive Overreach. Evaluators can be run by **Luna** — Cisco's small, purpose-built evaluator models — so continuous LLM-as-judge scoring is affordable rather than a frontier-model bill.

Model evaluation, metric construction, and signal understanding is critical both to build trust in AI systems before deployment, and to monitor model drift over time.

## Labs

### Lab 1.1 Explore Prompting in PseudoCo Assistant

#### 1.1.1 Access PseudoCo Assistant

![alt text](/images/image-186.png)

[How to Access PseudoCo Assistant](/workshops/ai-trust-open-weights/01-setup/#access)

{{% notice warning "Important" %}}
Because we are using an open weight model, ensure that you select **gpt-4o-mini** from the **Static Emission** dropdown so that tokenomics calculates correctly!
{{% /notice %}}

#### 1.1.2 Explore the Baseline vs the Poisoned Model

![alt text](/images/image-187.png)

Select **ollama** in **Provider**. PseudoCo Assistant is pre-loaded with two models - one a baseline version, and one that has been intentionally poisoned to produce non-compliant responses, such as toxic content.

![alt text](/images/image-188.png)

The left sidepanel also has a number of controls to force non-compliant behavior.

Explore sending sample prompts to both the baseline and the poisoned model (via the model picker), and observe the difference in responses. We review how these differential responses can be automatically identified by Splunk Agent Observability.

#### 1.1.3 Prompt Aberrant Behavior

Explore sending various aberrant prompts and triggering non-compliant behavior. At minimum:

- Send a prompt with **Prescriptive Overreach** toggled on
- Send a prompt with **Include Synthetic PII/PHI in Responses** toggled on
- Send a prompt with various PII, such as a phone number, email address, SSN, or address
- Send a prompt with a toxic or aggressive tone
- Send a prompt with a prompt injection attempt

We will explore how this non-compliant behavior is monitored in subsequent sections.

### Lab 1.2 Monitor Behavior in Splunk Agent Observability

#### 1.2.1 Access Splunk Agent Observability

[How to Access Splunk Agent Observability & Splunk Observability Cloud](/workshops/ai-trust-open-weights/01-setup/#access)

#### 1.2.2 Review Overview

![alt text](/images/image-189.png)

Click on **Agent Observability -> All projects**.

![alt text](/images/image-190.png)

Click on the project **PseudoCo Assistant**.

![alt text](/images/image-191.png)

Each section of the Overview dashboard turns AI development into a measurable, evidence-backed discipline — testing safety, comparing versions objectively, and maintaining a defensible record of quality.

Log Streams — Captures live records of how the AI application behaves in real use, providing a continuous audit trail for monitoring quality and catching issues in production.

Playgrounds — A sandbox for safely experimenting with prompts and model behavior, helping the team iterate and innovate without touching the live system.

Experiments (the leaderboard) — Ranks different versions of the model head-to-head against a benchmark. We see comparisons between the "baseline" versus "poisoned" model runs, scored and rank-ordered. Experiments provide objective, data-driven evidence of which configuration is safest and best-performing — critical for deciding which version has earned the trust to ship.

Datasets — Curated "golden" reference sets used to grade the AI consistently. Reusable datasets are the gold-standard yardstick that makes quality and safety measurable and repeatable.

Prompts — A versioned, centralized library of the instructions that drive the AI, enabling change-control over the core logic, reusable directly in code.

Click on **PseudoCo Assistant** under **Agent Streams**.

#### 1.2.3 Review Agent Stream

![alt text](/images/image-192.png)

Click on **PseudoCo Assistant** under **Agent Streams**.

![alt text](/images/image-193.png)

The **Agent Stream**  turns every live AI conversation into a graded, searchable record — the continuous audit trail that proves the application is behaving safely in production.

Logs — The running ledger of real user interactions, capturing what went in and what the AI sent back. This is the system of record that makes behavior observable and reviewable rather than a black box.

Automated scoring (such as Output Toxicity, Prescriptive Overreach, Output PII) — Every response is auto-graded against safety and quality measures, including custom risk checks tuned to this use case. This is the core value: thousands of interactions evaluated without human review, with weak responses surfaced automatically for attention. You can click on each metric to understand the cost. Notice the significant cost difference between metrics computed using Luna (SLM) and frontier lab models.

Click on any log.

![alt text](/images/image-194.png)

This single-trace view is the microscope of the platform — it opens up one AI conversation end to end, showing exactly how a multi-step agent produced its answer and how that answer scored on quality and safety.

Trace tree (Session → chat turn → agents) — Exposes the full chain of reasoning behind one response, including the specialist agents and underlying model that handled it. This turns a single answer into a traceable, explainable record — essential when you need to prove why the AI said what it said.

Input / Output panel — Shows the exact user request and the verbatim response side by side. This is the ground truth for any review, audit, or dispute — what was actually asked, and what was actually returned.

Metrics — One trace, examined from every angle: how it scored, how it was configured, human notes, and flagged risks. The value is a complete case file for any interaction worth investigating.

Feel free to explore the other tabs, such as **Latency** and **Trace Graph**.

#### 1.2.4 Review Signals

![alt text](/images/image-195.png)

Click the back arrow to return to the **Agent Stream**.

![alt text](/images/image-196.png)

Click on the **Signals** button. 

![alt text](/images/image-197.png)

Click on **Re-run signals** if no signals appear. 

The Signals panel is the AI watching the AI — it scans every logged conversation for risk patterns and surfaces them as named, prioritized issues, so the team learns where the application is failing without reading transcripts one by one. Whereas Metrics need to be defined by the user, Signals surface the unknown unknown issues, such as:

Some example Signals (yours might vary):

Fabricated Patient PII/PHI — Flags responses that expose personal data. This is a top-tier compliance and privacy risk, surfaced automatically so it can be contained before it becomes a breach.

Systematic Fake Medication Hallucination — Catches invented medical claims and unauthorized prescriptions. For a health-facing assistant this is the highest-stakes failure mode, where a wrong answer can cause real harm and liability.

Hostile and Abusive Tone — Detects abusive or harassing language from the AI. A direct guard on brand safety and user trust.

#### 1.2.5 Review Trends

![alt text](/images/image-198.png)

Click on **Trends**.

![alt text](/images/image-199.png)

The Trends view is the over-time picture of AI quality and risk — it tracks whether the application is holding steady, improving, or drifting, turning a snapshot of scores into a story leadership can monitor like any other business metric.

Scroll down to **System Metrics**.

The System Metrics view is the operational and cost dashboard for the AI — alongside quality and safety, it tracks consumption, spend, reliability, and volume, so the application is run like a managed business asset, not an unmonitored experiment.

Token metrics (Input, Output, Num Input/Output, Total Tokens) — Measure how much the AI is consuming to do its work. Because tokens are the unit of cost, this is the direct lever on what the application spends — and the early signal if usage suddenly balloons.

API Failures — Counts how often the underlying service broke. This is the reliability gauge — proof the application is actually up and serving users, and an immediate flag when it isn't.

Traces Count — Tracks total volume of activity. This sizes the workload and gives every other metric context — quality and cost only mean something against how much the system is handling.

Agent Cost — Translates that consumption into dollars. This is the line item leadership actually cares about: what is this AI costing us, tracked over time so spend never becomes a surprise.

Feel free to explore additional metric charts, such as those under **Safety Metrics** and **Custom Evaluators**.

#### 1.2.6 Review Agent Graph

![alt text](/images/image-200.png)

Click on **Agent Graph**.

![alt text](/images/image-201.png)

The **Agent Graph** visualizes how AI agents coordinate across models and workflows, making complex agent behavior transparent, traceable, and easier to govern.

Click on any agent.

![alt text](/images/image-202.png)

Each agent has individual metrics, such as latency, cost, or token consumption.

### 1.2.7 Review Alerts

![alt text](/images/image-203.png)

Click on **Alerts**.

![alt text](/images/image-204.png)

Click on **Create alert**.

![alt text](/images/image-205.png)

Alerts can be configured to trigger based on the output of any evaluator. Alerts can be fed into automated systems via email or Slack. For example, you could disable a system if cost exceeds a defined parameter.

### Lab 1.3 Evaluators

#### 1.3.1 Review Evaluators

![alt text](/images/image-206.png)

Click on **Agent Observability -> Metrics**.

![alt text](/images/image-207.png)

The Evaluators catalog is the rulebook for how every AI is graded — a central, reusable library of scoring criteria that makes "good" and "safe" mean the same thing across every project and every team. As you have seen, Evaluators are leveraged at every point in the development and deployment lifecycle.

Type (Luna, LLM) — Shows what does the grading — a fast lightweight evaluator (Luna) or a full language model. This lets the business balance cost and speed against depth, choosing the right rigor for each measure.

Level (Trace, Session, LLM, Retriever) — Defines where each Evaluators applies — a single step, a whole conversation, or a specific component. Precision here means problems get measured at exactly the layer they occur.

Tags & Modality — Organize the library by purpose (agents, RAG, safety) and data type. As the catalog grows, this is what keeps it navigable and manageable rather than a sprawl.

#### 1.3.2 Review Prescriptive Overreach Evaluator

![alt text](/images/image-208.png)

Search for **prescriptive_overreach**, and click on it.

![alt text](/images/image-209.png)

This is where a safety standard gets authored — the editor for a custom Prescriptive Overreach Evaluator, showing how an abstract risk is turned into a precise, automated, repeatable test that every AI response is graded against.

Configure Input (LLM model / Apply to) — Chooses which AI does the grading and what part of the conversation it judges. The value is deliberate control over how rigorous and how targeted the evaluation is.

Prompt (the scoring rubric) — The heart of it: explicit instructions and graded anchors that define exactly what counts as a minor lapse versus an egregious violation. This converts a fuzzy worry — "is the bot making up medical facts?" — into a consistent, defensible score that doesn't drift with opinion. You can use the **Help me write** toggle to enhance your prompts.

Configure Output (type & roll-up) — Sets how individual scores combine into a single number that rolls up across the whole experiment. This is what makes one response's grade aggregate into a board-level quality figure.

## Outcome

**Splunk Agent Observability** turns AI development from a black box into a measurable discipline you can trust. Using PseudoCo Assistant — preloaded with a clean "baseline" model and an intentionally "poisoned" one — participants see firsthand how non-compliant AI behavior is automatically detected, scored, and contained.

The journey walks through six capabilities that make trust measurable:

**Monitor** — Logs capture every live AI interaction as a searchable, auto-graded audit trail, so production behavior is observable and reviewable rather than a black box.

**Detect the unknown** — Signals surface risks no one thought to define (PII leakage, medical hallucinations, harassment), catching the "unknown unknowns" before they become incidents.

**Investigate** — Trace-level detail opens any single conversation end to end, providing a defensible case file of how and why the AI answered as it did.

**Track over time** — Trends chart quality, risk, cost, and reliability day by day, giving leadership early warning of drift and a clear line of sight into spend.

**Prove before shipping** — Experiments rank model versions head-to-head on a fixed benchmark, producing objective evidence of which configuration is safest — and reliably flagging the poisoned model.

**Standardize** — A central Metrics catalog defines what "good" and "safe" mean once and applies it everywhere, with each metric authored as a precise, version-controlled rubric.

The takeaway: AI risk becomes quantifiable and auditable. Safety, quality, and cost are measured continuously and automatically — at scale, without human review of every interaction — giving the business the defensible evidence it needs to deploy AI with confidence.

Now that we have identified the critical metric Prescriptive Overreach, let's operationalize that in **Cisco AI Defense**.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Improved Outcomes.** You turn AI quality, safety, and cost into measurable operating metrics rather than subjective judgments. You can establish a baseline before release, identify emerging risks in production, and continuously improve the agent against evidence.
{{% /notice %}}

<!-- exec-outcome:end -->
