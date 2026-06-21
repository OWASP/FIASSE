# Application Security Engineer Onboarding: How I Use FIASSE in My Day-to-Day Work

As an application security engineer, I understand that my best leverage comes from helping teams *create* [securable software](../framework/S2.1.0.md), not from testing alone. FIASSE is a deliberate departure from traditional AppSec operating patterns that overemphasize downstream triage and ticket routing. I still use those activities when needed, but I prioritize influencing software while it is still being designed and built.

## How My AppSec Operating Model Changes in FIASSE

### 1. Triage Strategy Changes

In traditional programs, triage often centers on large findings queues. In FIASSE, I still triage findings, but my first question is broader: what engineering condition allowed this class of issue to appear?

- I map findings to missing or weak [security requirements](../framework/S4.1.2.md) and [security acceptance criteria](../framework/S4.1.2.md).
- I group repeated findings into design and process patterns rather than treating each item as a disconnected defect.
- I use [merge review](../framework/S5.2.0.md) to keep remediation close to the change that introduced risk.

### 2. Risk Communication Pattern Changes

I communicate risk in engineering terms developers can act on quickly. I avoid [shoveling left](../framework/S6.1.0.md) by using a strict format:

- What is wrong (clear technical issue)
- Which SSEM attribute is at risk (for example [Integrity](../framework/S3.2.3.md#3232-integrity) or [Modifiability](../framework/S3.2.1.md#3212-modifiability))
- What business impact is plausible
- What engineering decision is needed now
- What verification proves we are done

### 3. Escalation Triggers Change

I escalate when the issue is no longer a local code fix and requires broader decisions.

- The same flaw class recurs across teams or services.
- A [trust boundary](../framework/S4.3.0.md) is being violated in a business-critical flow.
- Required [security acceptance criteria](../framework/S4.1.2.md) are missing or cannot be met before merge.
- A dependency risk requires platform, architecture, or governance intervention ([dependency stewardship](../framework/S4.6.0.md)).

### 4. Handoff Loops with Product and Platform Change

FIASSE uses explicit handoff loops so security input stays actionable and preserves developer velocity.

- Product loop: convert threat insights into requirement language and acceptance criteria.
- Platform loop: turn recurring control needs into reusable guardrails, libraries, and defaults.
- Engineering loop: apply and verify decisions in code and [merge review](../framework/S5.2.0.md).
- Security loop closure: confirm outcomes through tests, telemetry, and updated threat models.

## FIASSE Security Input Flow (Velocity-Preserving)

I use a strict flow that prioritizes the earliest point of influence and keeps security from becoming a late gate.

1. **L1 - Product requirements (pre-generation):** inject security into [requirements and acceptance criteria](../framework/S4.1.2.md) before implementation.
2. **L2 - Generation time:** ensure implementation aligns to defined outcomes and core SSEM qualities ([SSEM overview](../framework/S3.0.0.md)).
3. **L3 - Commit/PR time:** perform intelligent remediation during [merge review](../framework/S5.2.0.md), not after release.
4. **L4 - Deployment time:** validate business-logic behavior at [trust boundaries](../framework/S4.3.0.md) and resilient coding expectations ([resilient coding](../framework/S4.4.0.md)).
5. **L5 - Runtime:** use [Observability](../framework/S3.2.1.md#3214-observability) and [Transparency](../framework/S2.5.0.md) signals to detect drift and feed corrections back to earlier layers.

I pay attention to the SSEM attributes because they give me a consistent way to evaluate whether a system can stay defensible over time. I look for [Analyzability](../framework/S3.2.1.md#3211-analyzability), [Modifiability](../framework/S3.2.1.md#3212-modifiability), [Testability](../framework/S3.2.1.md#3213-testability), [Observability](../framework/S3.2.1.md#3214-observability), and the trustworthiness qualities that make security properties durable.

FIASSE influences my approach by making security a native input to software engineering, not a separate phase. I focus on clear expectations, high-signal feedback, and predictable handoffs that improve outcomes without stalling delivery.

## Quick Read Path

If I am new and want the fastest high-level understanding, I read in this order:

1. [Introduction and purpose](../securable_framework.md#1-introduction)
2. [The application security challenge](../framework/S1.1.0.md)
3. [FIASSE and SSEM overview](../framework/S1.2.0.md)
4. [Foundational principles](../framework/S2.0.0.md)
5. [The role of the security team](../framework/S7.1.0.md)
6. [Early integration: planning and requirements](../framework/S5.3.0.md)
7. [Common AppSec anti-patterns](../framework/S6.0.0.md)
8. [Organizational adoption of FIASSE](../framework/S8.0.0.md)

This gives me a clear mental model: help teams define securable outcomes early, reinforce them with engineering language, and keep the partnership centered on building software that can stay defensible as it evolves.