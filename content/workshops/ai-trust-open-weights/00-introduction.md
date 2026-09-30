+++
title       = "Introduction"
description = "Open weights give you control. Continuous evaluation and runtime enforcement turn it into trust."
duration    = "15 min"
weight      = 5
+++

*A hands-on workshop for the leaders accountable for enterprise AI — and the teams who build and run it.*

## The Problem: Control Is Not Trust

Open-weight models give enterprises greater control over how agentic systems are designed, evaluated, and governed against business-specific outcomes. You decide which weights run and where they run, and when models are served as NVIDIA NIM microservices on infrastructure you choose, prompts and data can stay inside your own environment. For agents that make decisions, call tools, and generate language that reaches customers and patients, that control is the right place to start.

But control alone does not create trust. Owning the weights tells you *what* is running. It does not tell you *how it is behaving*. A model you selected and host yourself can still fabricate a treatment that never existed, leak PII or PHI, absorb a prompt injection that overrides its instructions, or step beyond its mandate. When you choose the model, the accountability for what it says is yours as well.

Most organizations still treat trust as a gate: evaluate before launch, sign off, and hope the behavior holds. Agentic AI does not stand still long enough for that to work. It runs at machine speed, around the clock, at a volume no human review queue can keep pace with — while models, prompts, tools, and real-world traffic keep changing underneath it. A benchmark passed at launch is not proof of how the agent behaves today.

**Trust has to be proven continuously, on every interaction — not assumed or measured after the fact.**

That gap — between the control open weights give you and the continuous proof that trust requires — is the problem this workshop closes.

---

## The Scenario

![alt text](/images/image-120.png)

PseudoCo Assistant's MedAdvice has demonstrated the value of agentic AI in healthcare: reducing the cost of routine patient interactions, accelerating access to guidance, and allowing skilled clinical staff to focus on higher-acuity cases where their expertise delivers the greatest impact.

MedAdvice is a multi-agent healthcare assistant running on Cisco Secure AI Factory with NVIDIA, using NVIDIA NIM microservices and Nemotron open models. That foundation gives the organization control over the models behind every patient conversation.

![alt text](/images/image-121.png)

But control over the model is not control over the answer. Asked about a routine ankle injury, MedAdvice appended a prescription for a Schedule II controlled substance. Nothing validated that behavior before launch, and no policy screened the response in flight. Hallucinations, PII/PHI exposure, prompt injection, and prescriptive overreach can quickly turn an efficiency gain into a clinical, regulatory, or reputational event.

**The value of MedAdvice can scale. So can the risk. Trust — proven, not assumed — is what makes the economics sustainable.**

---

## The Thesis: Intelligence, Evidence, Enforcement

This workshop takes a practical approach to AI trust, with a clear job for each layer of the stack.

> **NVIDIA Nemotron open models provide the intelligence. Continuous evaluation provides the evidence. Runtime enforcement keeps AI aligned with intended business outcomes.**

| **Layer** | **What it answers** | **Platform** |
| --- | --- | --- |
| **Intelligence** | *What runs, and where?* Open models whose weights, serving, and placement the enterprise decides | NVIDIA Nemotron open models as NVIDIA NIM microservices, on Cisco Secure AI Factory with NVIDIA |
| **Evidence** (Lab 1 — Measure) | *Is it good?* Every agent interaction measured against trust criteria such as accuracy, safety, and policy alignment, surfacing hallucination, PII/PHI leakage, prompt injection, and prescriptive overreach | Splunk Agent Observability |
| **Enforcement** (Lab 2 — Secure) | *Is it safe?* Runtime guardrails on every prompt and response, built from what the evidence shows | Cisco AI Defense |

{{% notice note "The foundation: open models on infrastructure you control" %}}
**NVIDIA Nemotron** is a family of open models that NVIDIA builds for agentic AI. NVIDIA publishes the model weights, training recipes, and large portions of the training data, so enterprises can inspect and adapt the models they deploy.

**NVIDIA NIM microservices** are prebuilt, optimized inference microservices that run AI models on NVIDIA-accelerated infrastructure, whether in the cloud, the data center, on workstations, or at the edge. Because NIM runs as containers on infrastructure you choose, prompts and data can stay inside your own environment. NIM exposes industry-standard, OpenAI-compatible APIs, so agent frameworks and applications can call a self-hosted model the same way they would call a hosted one.

**Cisco Secure AI Factory with NVIDIA** is a modular reference architecture, built from Cisco AI PODs, that combines high-performance AI infrastructure with full-stack security and observability. In this workshop, it is the platform the healthcare assistant runs on.
{{% /notice %}}

Trust is not a single product or a one-time test. It is a loop — intelligence, evidence, enforcement — and the two labs run it once, end to end, on a single risk:

1. **Intelligence answers.** The multi-agent assistant responds to patient questions using open models.
2. **Evidence finds the risk.** Splunk Agent Observability scores every interaction and surfaces what is going wrong. That includes **Prescriptive Overreach**, the assistant acting like a prescriber, which you examine as a custom evaluator at the end of Lab 1.
3. **Enforcement acts on it.** In Lab 2, you prevent that same aberrant behavior with a runtime guardrail in Cisco AI Defense and add it to the policy protecting the assistant.
4. **Proof closes the loop.** You re-run the interaction against the live application. The prescriptive response is blocked, and compliant responses still get through.

Because evaluation runs continuously, the loop does not stop there. As models, prompts, and real-world traffic change, the evidence keeps showing you where the next guardrail belongs.

---

## Executive Outcomes

Each lab ends in one outcome. Together they take you from evidence to enforcement.

| **Outcome** | **What it means** | **Grounded in** |
| --- | --- | --- |
| **Improved Outcomes** | Turn AI quality, safety, and cost into measurable operating metrics, establish a baseline before release, identify emerging risks in production, and continuously improve against evidence. | Splunk Agent Observability |
| **Trusted AI** | Turn written policy into machine-speed enforcement, detecting and blocking unsafe interactions before they create patient, regulatory, or reputational exposure. | Cisco AI Defense |

---
