+++
title         = "Agentic Observability with NVIDIA"
hero_title    = "Agentic Observability *with NVIDIA*"
eyebrow       = "Agentic Observability with NVIDIA — FY'27"
description   = "An NVIDIA AI Blueprint, as shipped, on AWS. Observed by Splunk. Secured by Cisco. Governed in Splunk Core."
home_sections = ["workshops"]

[[cta]]
label = "Start: Setup & Prerequisites"
href  = "/workshops/agentic-observability-nvidia/01-setup/"
style = "primary"

[[cta]]
label = "Jump to the labs"
href  = "/workshops/agentic-observability-nvidia/02-overview/"
style = "ghost"
+++

*A field workshop for the platform, security, and observability teams who are putting NVIDIA-built agents into production — and the executives accountable for them.*

## The Problem: The Agents Arrived Before the Instruments Did

Enterprises are standing up agentic AI on NVIDIA AI Blueprints in weeks. A reference storefront, a research assistant, or a customer-service agent comes with its models, its retrievers, and its orchestration already wired — and it runs on the GPUs you already bought. The build problem is solved.

The trust problem is not. The moment that blueprint takes real traffic, four teams ask four questions at once. Operations asks whether the agents are fast, healthy, and affordable. Security asks whether a prompt injection can talk the promotion agent into a discount it should never give. Quality asks whether the search agent is picking the right tool and the right products. Compliance asks for the record of a single checkout, end to end, on demand.

Most teams answer those questions by changing the application: a tracing library here, a guardrail wrapper there, a log shipper bolted on the side. Every change forks the blueprint away from the one NVIDIA maintains, and every fork has to be re-applied on the next release. **The instrumentation becomes the technical debt.**

This workshop closes that gap the other way around. The blueprint stays exactly as shipped. Three additions — Splunk Agent Observability, Cisco AI Defense, and HTTP Event Collector forwarding to Splunk Core — are applied as configuration and keys, never as code. One trace, captured once, answers all four questions.
