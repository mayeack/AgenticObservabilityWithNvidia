+++
title       = "Lab 1 — Run"
description = "NVIDIA AI Blueprint on AWS: use the storefront as shipped and confirm the agents, NIMs, and GPUs are the blueprint's own."
duration    = "45 min"
weight      = 30
+++

![alt text](/images/image-8.png)

**Pillar:** Run<br>
**Tool:** NVIDIA AI Blueprint on AWS<br>
**Outcome:** Accelerated Time to Value

<!-- persona:start -->

{{% notice style="info" title="Who this is for" icon="users" %}}
**AI Platform / MLOps engineers** and **Infrastructure leaders**. Primary question: _Can we run an NVIDIA blueprint on our own GPUs, as shipped, and keep NVIDIA's upgrade path?_ Application owners join to see what the storefront does before anyone instruments it.
{{% /notice %}}

<!-- persona:end -->

{{% notice style="info" title="Objective" icon="target" %}}
Use the storefront as a shopper, watch the four agents work, and confirm that what is running is the NVIDIA Retail Agentic Commerce blueprint exactly as shipped — its Compose files, its NIM microservices, its models — on a GPU instance in AWS.
{{% /notice %}}

## Background

The NVIDIA Retail Agentic Commerce blueprint is deployed from its own three Docker Compose files on a single AWS `g6e.4xlarge` with one NVIDIA L40S. The **Nemotron 3.5 Lightning** NIM serves every agent's reasoning and the **Nemotron 3 Embed** NIM serves retrieval, both resident on that one GPU; Milvus, Postgres, and the application services run on the CPU. Nothing in the checkout is patched; the workshop's additions arrive as a fourth Compose file laid beside it.

The blueprint already emits OpenTelemetry spans: every agent's YAML ships a Phoenix exporter under `general.telemetry.tracing`. That is the hook every later lab uses. In this lab you see the agents from the shopper's side and from the blueprint's own trace viewer, so that in Lab 2 you can recognise the same spans in Splunk.

## Labs

### Lab 1.1 Shop the Storefront

#### 1.1.1 Access the Storefront

[How to Access the Storefront](/workshops/agentic-observability-nvidia/01-setup/#1-how-to-access-the-storefront)

#### 1.1.2 Search for a Product

![alt text](/images/image-9.png)

In the search box, type a natural-language request such as **"trail running shoes for rocky terrain under $150"** and press Enter.

The **search agent** turns the sentence into a semantic query, retrieves candidates from Milvus using Nemotron 3 Embed, and lets Nemotron 3.5 Lightning choose and rank the products. Watch the **Agent Activity** panel: the retrieval and the model call appear as separate steps.

#### 1.1.3 Review Recommendations

![alt text](/images/image-10.png)

Open a product. The **recommendation agent** proposes complementary items. This agent is itself multi-agent: it plans, retrieves, and ranks in separate steps, which is why it will produce the deepest span tree in Lab 2.

#### 1.1.4 Add to Cart and Watch the Promotion Decision

![alt text](/images/image-11.png)

Add the product to the cart. The **promotion agent** receives pre-computed business signals — margin, inventory, cart value — and selects a strategy from a pre-approved set. The model never computes a price: it chooses among options the merchant API has already validated, and the merchant API applies the result deterministically.

This is the decision Cisco AI Defense protects in Lab 3.

#### 1.1.5 Check Out Over the Agentic Commerce Protocol

Proceed to checkout. The merchant API completes the purchase over the Agentic Commerce Protocol and delegates payment to the PSP service. The Agent Activity panel shows the protocol messages — checkout session, payment delegation, order — as they happen.

#### 1.1.6 Read the Post-Purchase Message

The **post-purchase agent** writes the shipping and thank-you message from the order context, in the shopper's language. Note the wording; it is generated text and will be visible as an LLM output span in Lab 2.

### Lab 1.2 Review the Deployment

#### 1.2.1 The Compose Stack

![alt text](/images/image-12.png)

The facilitator's screenshot shows `docker compose ps` on the instance: the blueprint's application services, the two NIM containers, Milvus, Postgres, Phoenix — and one workshop addition, `otel-collector`. The blueprint's Compose files are unmodified; the collector comes from the overlay file.

#### 1.2.2 The GPUs

![alt text](/images/image-13.png)

`nvidia-smi` on the instance: one NVIDIA L40S with two NIM processes resident — the Nemotron 3.5 Lightning NIM on a 4-bit weight profile with its KV cache capped, and the Nemotron 3 Embed NIM beside it. This is the AI factory in miniature — NVIDIA's models, NVIDIA's inference microservices, on an NVIDIA GPU, in AWS, for the price of a mid-size CPU instance.

#### 1.2.3 NIM Health

The NIM microservices expose `/v1/health/ready` and the OpenAI-compatible `/v1/models`. The agents reach them by service name on the Compose network; nothing about the models is exposed to the internet.

### Lab 1.3 Review the Blueprint's Own Traces

#### 1.3.1 Open Phoenix

![alt text](/images/image-14.png)

The facilitator opens the blueprint's bundled Phoenix instance. Each agent has its own project — `search-agent`, `arag-recommendations`, `promotion-agent`, `post-purchase-agent` — populated by the exporter NVIDIA ships in the YAML.

#### 1.3.2 The Span Tree

![alt text](/images/image-15.png)

Open the trace for your search. The workflow span contains the agent span, the `product_search` tool span, and the LLM span with its input and output. Remember the shape: in Lab 2 the identical tree appears in Splunk Agent Observability, because the workshop added a second and third destination for the same spans rather than new instrumentation.

## Outcome

The storefront runs as NVIDIA ships it, on your GPUs, with every agent decision already visible as an OpenTelemetry trace. Everything that follows is a question of where those traces go and what inspects the model calls on the way — not of changing the application.

<!-- exec-outcome:start -->

{{% notice style="info" title="Executive outcome" icon="star" %}}
**Executive outcome — Accelerated Time to Value.** You move from reference architecture to a running agentic application on your own infrastructure in hours, and you keep the upgrade path NVIDIA maintains because nothing in the blueprint was changed.
{{% /notice %}}

<!-- exec-outcome:end -->
