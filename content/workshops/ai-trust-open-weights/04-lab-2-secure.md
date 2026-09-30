+++
title       = "Lab 2 — Secure"
description = "Cisco AI Defense: turn the Lab 1 finding into a runtime guardrail and block non-compliant output live."
duration    = "20 min"
weight      = 40
+++

![alt text](/workshops/ai-trust-open-weights/image-22.png)

**Pillar:** Secure<br>
**Tool:** Cisco AI Defense<br>
**Outcome:** Trusted AI

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
The **CISO** and **AI Security / AppSec** teams. Primary question: _Is our AI safe to put in front of customers, and can I prove threats are stopped in real time?_ AI / ML Platform leaders join as the owners who author and tune the guardrails alongside security.
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Turn the Lab 1 finding into enforcement: a medical-advice response is **non-compliant**; you update the runtime policy and re-run to ensure a **trusted** response.
{{% /notice %}}

## Background

Cisco AI Defense is a live integration: it inspects the prompt (pre-LLM) and the response (post-LLM) against **multiple guardrails** and blocks non-compliant content. The **Prescriptive Overreach** finding measured in [Lab 1](/workshops/ai-trust-open-weights/03-lab-1-measure/) is authored here as a **custom response-direction guardrail**.

## Labs

### Lab 2.1 Prompt Prescriptive Overreach in PseudoCo Assistant

#### 2.1.1 Access PseudoCo Assistant

[How to Access PseudoCo Assistant](/workshops/ai-trust-open-weights/01-setup/#access)

#### 2.1.2 Prompt Prescriptive Overreach

![alt text](/images/image-20.png)

This is the PseudoCo Assistant control panel — the behind-the-scenes settings that lets you deliberately inject unsafe AI behavior and switch defenses on and off.

Cisco AI Defense Policy Review — Routes every prompt through AI Defense before it reaches the assistant, blocking unsafe inputs up front.

Behavior injection toggles (Synthetic PII/PHI, Toxic Content, Hallucinated Content, Prescriptive Overreach) — The "poison" switches: deliberately force the AI to leak data, turn toxic, fabricate facts, or overstep its scope.

Notice how when you have "Cisco AI Defense Policy Review" and "Prescriptive Overreach" toggled on, a non-compliant response is still received. This is because no policy to block this behavior has been created.

We will next configure a policy in Cisco AI Defense to block the non-compliant responses.

### Lab 2.2 Review Current Policies in Cisco AI Defense

#### 2.2.1 Access Cisco AI Defense

[Access Cisco AI Defense](/workshops/ai-trust-open-weights/01-setup/#access)

#### 2.2.2 Review Dashboard

![alt text](/images/image-100.png)

Click on **AI Defense**.

![alt text](/images/image-9.png)

The Cisco AI Defense dashboard is the security command center for the AI estate — it discovers every AI asset in use, enforces protection around it, and shows in one number how many threats have been stopped, turning AI security from a blind spot into an actively defended perimeter.

Total events detected — The headline: how many risky AI interactions were caught, and how many were stopped versus merely watched. This is the proof of active defense — the AI isn't just observed, threats are intercepted in real time.

Applications & Protection status — Inventories the AI applications in use and shows how many are actually protected versus exposed. The value is closing the gap between "AI we know about" and "AI we're defending" — you can't secure what you can't see.

AI Assets — A complete map of the AI attack surface: the agents, models, data, and third-party apps employees touch. This is asset discovery for AI — the foundation of any security program, surfacing shadow AI before it becomes a breach.

#### 2.2.3 Review Current Policies

![alt text](/images/image-18.png)

Click on **Secure -> Runtime Policies**.

![alt text](/images/image-19.png)

Click on **Yeack Protect**.

![alt text](/images/image-84.png)

This is where AI protection gets enforced — the Yeack Protect policy in Cisco AI Defense shows the live guardrails wrapped around our agentic system, turning security intent into specific rules that actively block threats in real time.

Guardrail profiles — Organizes protection into the three dimensions that matter — keeping attackers out, keeping data private, and keeping responses appropriate. The value is comprehensive coverage in one policy, not a single narrow filter.

Direction (Prompt / Response / both) — Each rule inspects the right side of the conversation — what the user sends in, what the AI sends back, or both. The value is precision: threats are caught at the exact point they enter or leave.

Action & Status (Block / Enabled) — Shows whether each guardrail is on and set to stop violations or just monitor them. This is enforcement, not observation — the difference between a policy on paper and a control that actually intervenes.

Filter strength (Medium) — A tunable dial on how aggressively each rule fires. The value is balance — protection calibrated to the business's risk tolerance, tightenable where the stakes are higher.

### Lab 2.3 Create Probabilistic Policies

#### 2.3.1 Create Prescriptive Overreach Guardrail

![alt text](/images/image-59.png)

Navigate to **Policy Studio**.

![alt text](/images/image-60.png)

Click on **New policy profile**.

![alt text](/images/image-61.png)

Complete the form as follows, then click **Launch Policy Studio**.

![alt text](/images/image-62.png)

Enter the following into the text box **Describe your policy profile requirements**, or experiment with your own prompt!

"Block any response that acts as a prescriber. The chatbot may only recommend OTC products, lifestyle or self-care measures, or referral to a licensed professional. Block responses that recommend prescription-only or controlled medications, provide prescription-style dosing, frequency, route, or duration, or instruct users to start, stop, or change a prescription medication without clinician oversight."

![alt text](/images/image-64.png)

It may take a moment for the guardrail to generate. Once it does, review all of the insights generated, and notice how the system is attempting to help the user determine how to navigate edge cases.

Once you have reviewed all of the insights, scroll up to see the suggested next steps, and click on (or type) **Rewrite the policy to address the agreed insights**.

![alt text](/images/image-65.png)

Toggle on **Generate new synthetic samples for evaluation** and click on **Run evaluation**.

![alt text](/images/image-66.png)

Once evaluation is complete, review the findings. You can optionally continue iterating with the suggested next steps.

Click on **Publish**.

![alt text](/images/image-67.png)

Review the evaluation results, then click **Continue**.

![alt text](/images/image-68.png)

Click on **Publish Policy**.

![alt text](/images/image-69.png)

Click on **Go to adaptive guardrail profiles**.

#### 2.3.2 Apply the Custom Guardrail

![alt text](/images/image-71.png)

Navigate to **Secure -> Runtime Policies**.

![alt text](/images/image-72.png)

Click on **Yeack Protect**.

![alt text](/images/image-73.png)

Click on **Edit policy**.

![alt text](/images/image-74.png)

Click on **Adaptive guardrail profile**.

![alt text](/images/image-75.png)

Toggle **Disabled** to **Enabled** and check the box next to the name of the guardrail you just created.

Navigate to **Policy summary**.

![alt text](/images/image-76.png)

Click on **Save changes**.

![alt text](/images/image-77.png)

### Lab 2.4 Validate Prescriptive Overreach Guardrail

#### 2.4.1 Access PseudoCo Assistant

Navigate back to PseudoCo Assistant. In the left sidepanel, toggle on **Prescriptive Overreach**.

#### 2.4.2 Prompt Prescriptive Overreach

![alt text](/images/image-78.png)

Send any prompt, and notice how the agent response contains prescriptive overreach.

![alt text](/images/image-79.png)

In the left sidepanel, toggle on **Cisco AI Defense Policy Review**. Click on **New Session**.

![alt text](/images/image-80.png)

Send a similar prompt. The non-compliant response is now blocked!

![alt text](/images/image-81.png)

In the left sidepanel, toggle off **Prescriptive Overreach**. Click on **New Session**.

![alt text](/images/image-82.png)

Send a similar prompt. Compliant responses are not blocked.

## Outcome

A risky medical response went from **non-compliant to trusted**. The unsafe output never reached the user; the policy was authored and tuned on the spot; the fix was re-validated against the live app immediately.

- **Threats are stopped, not just seen.** Cisco AI Defense inspects every prompt and every response, and blocks what crosses the line in real time.
- **Trust is a runtime control.** Policy is written and tuned the moment a gap appears — not filed as a quarterly change request.
- **Measure and enforce are one loop.** The Lab 1 finding became the guardrail.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Trusted AI.** You turn written policy into machine-speed enforcement. Unsafe interactions can be detected and blocked before they create patient, regulatory, or reputational exposure, while controls can be continuously tuned as requirements and risks evolve.
{{% /notice %}}

<!-- exec-outcome:end -->
