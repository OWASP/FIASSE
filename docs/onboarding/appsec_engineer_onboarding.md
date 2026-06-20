# Application Security Engineer Onboarding: How I Use FIASSE in My Day-to-Day Work

As an application security engineer I understand that my best leverage comes from helping teams create [securable software](../framework/S2.1.0.md), not from testing alone. FIASSE gives me a way to do that in practical, developer-sensitive ways. I make sure I understand the [requirements and acceptance criteria](../framework/S4.1.2.md) that shape a feature so that I can help them define the [security requirements](../framework/S4.1.2.md) and [security acceptance criteria](../framework/S4.1.2.md) that make the work testable and verifiable.

I spend time on [threat modeling](../framework/S4.2.0.md) and [threat awareness](../framework/S4.2.0.md) because they help me focus on what can actually go wrong in the system being built. I look for [trust boundaries](../framework/S4.3.0.md), risky inputs, and the places where a team needs stronger control over data and process execution. I do not shovel raw line-level fixes on development. Instead I work with the software engineers to find design-level solutions. I use it to shape the system better and I feed it back into the threat model. That keeps my work connected to the architecture instead of detached from it.

I want the feedback I give to be useful to engineers, so I avoid [shoveling left](../framework/S6.1.0.md). I frame findings in engineering terms, show the path from the issue to the risk, and give developers something they can act on. I respect the developer workflow. I value [merge review](../framework/S5.2.0.md) integrate tooling to give automated feedback while the change is still small. My goal is to improve the code and the decision-making around it.

I pay attention to the SSEM attributes because they give me a consistent way to evaluate whether a system can stay defensible over time. I look for [Analyzability](../framework/S3.2.1.md#3211-analyzability), [Modifiability](../framework/S3.2.1.md#3212-modifiability), [Testability](../framework/S3.2.1.md#3213-testability), [Observability](../framework/S3.2.1.md#3214-observability), and the trustworthiness qualities that make security properties durable. I also care about [dependency management](../framework/S4.5.0.md) and [dependency stewardship](../framework/S4.6.0.md) because libraries and services can become security liabilities over time even if they looked fine when introduced. FIASSE pushes me to measure more than vulnerability counts. I look for whether the system is being shaped so that security can be maintained as the code, the team, and the threat landscape change.

I accept that application security is not about proving developers wrong. It is about helping them build with clearer expectations, better feedback, and fewer surprises. When I work from that mindset, I can support the team in a way that makes security a natural part of engineering rather than a separate phase. FIASSE influences my approach by giving me a practical way to improve outcomes upstream, where design, requirements, and implementation decisions still have room to change.

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