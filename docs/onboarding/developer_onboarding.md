# Developer Onboarding: How I Use FIASSE in My Day-to-Day Work

As a software engineer, I understand that FIASSE asks me to shift how I approach security compared to traditional programs. Instead of treating security as an afterthought or gate, I build it into how I [create securable software](../framework/S2.1.0.md) from the start. My motivating principle is ["resiliently adding computing value"](../framework/S2.2.0.md): software that delivers features reliably while staying defensible as requirements and threats evolve.

## My Development Workflow in FIASSE

I apply FIASSE across the key phases of a feature or fix:

### During Requirements & Design:
Before I write code, I confirm that [requirements and acceptance criteria](../framework/S4.1.2.md) include security expectations, not just happy-path functionality. I ask: What are the security acceptance criteria for this feature? This is where I save the most rework because expectations are clear before I build.

### During Implementation:
I [identify trust boundaries and risky inputs](../framework/S4.3.0.md). Trust boundaries are where the level of trust or control changes between components, networks, or users. For example, when data travels from one trusted server to another across the Internet (the Internet being untrusted). For each boundary, I [canonicalize inputs](../framework/S4.4.1.md) by parsing untrusted data into a typed canonical structure that enforces expected type, format, length, and range before processing. For example:

- An API endpoint receives a quantity parameter. I parse it as a positive integer at the boundary and reject the request if parsing fails, then use the parsed value in calculations (not accepting it as the user specified it).
- A database query receives a user ID. I confirm it belongs to the authenticated user before returning associated data.

I also consider what error handling and [Observability](../framework/S3.2.1.md#3214-observability) would help make this feature easier to troubleshoot and maintain if something goes wrong: structured logs at trust boundaries, clear error states, and recovery paths.

### During Code Review:
I write code so that I can understand it when I come back later to make changes. This is [Analyzability](../framework/S3.2.1.md#3211-analyzability): clear naming, minimal cyclomatic complexity, and no unnecessary duplication. When reviewing code, I look for: Can I quickly trace data flow? Can I find where parsing and boundary checks happen? Are trust boundaries obvious?

I make sure there are no [hidden side effects](../framework/S2.6.0.md). I write code so that I am confident I can make changes later without unintended consequences—this is [Modifiability](../framework/S3.2.1.md#3212-modifiability). For example, I do not change part of the system to silently perform a new operation from within a method that already has a clearly defied single purpose.

### During Testing:
I prove my code with Unit Tests that cover normal inputs, edge cases, and invalid states. I expect [Testability](../framework/S3.2.1.md#3213-testability): I can write tests without modifying the code under test. I also expect AppSec to collaborate with me during [merge review](../framework/S5.2.0.md) so that findings become shared learning, not surprise rework. This collaboration may come in the form of automated scans that I am encouraged to ask questions about. I address all findings, including describing why certain code needs to be the way it is despite being flagged by security or security tooling. I understand this is proof of my understanding to those outside the team.

### Dependency & Supply Chain Decisions:
If I choose to use [open source libraries](../framework/S4.5.0.md), I make sure they fit these values. I check: Is the library maintained? Are security issues addressed? Can I update or replace it if needed? This is [dependency stewardship](../framework/S4.6.0.md): ongoing responsibility for libraries I introduce, not just an initial approval.

## Why FIASSE Reduces Rework

I am not chasing a [static state of secure](../framework/S2.1.0.md). I am building software that is defensible as things change. I build knowing there will be failures, but I architect them so failures are less likely to expose sensitive information and so that when something goes wrong, I can trace what caused it through structured [Observability](../framework/S3.2.1.md#3214-observability).

When AppSec reviews my code during [merge review](../framework/S5.2.0.md), I welcome it early because feedback on a small PR is easier to integrate than late-stage findings. I take pride in the code I submit, whether I hand-wrote it or used an AI assistant to generate it. I want the reviewer to be able to understand it and be confident in it too.

When security assurance finds something I didn't think of, I work with AppSec to address it by applying FIASSE principles, not just patching the symptom. A single finding might point to a broader design issue that, once fixed, prevents entire classes of problems. This context-driven approach reduces the rework that comes from treating each finding in isolation.

FIASSE influences my approach by making security a natural output of software engineering, not a surprise gate or separate phase.

## Quick Read Path

If I am new and want the fastest high-level understanding, I read in this order:

1. **[Foundational principles](../framework/S2.0.0.md)** — Understand the shift from traditional secure-by-gate to defensible-by-design.
2. **[SSEM model and attributes](../framework/S3.0.0.md)** — Learn the ten qualities that make software defensible (Analyzability, Modifiability, Testability, Observability, Authenticity, Accountability, Confidentiality, Availability, Integrity, Resilience).
3. **[Practical developer guidance](../framework/S4.0.0.md)** — See how to apply SSEM in your code and decisions.
4. **[Requirements & acceptance criteria](../framework/S4.1.2.md)** — This is your highest-leverage point; security expectations here save rework.
5. **[Boundary control & input handling](../framework/S4.3.0.md)** and **[Resilient coding](../framework/S4.4.0.md)** — Core patterns for safe trust-boundary crossing.
6. **[Developer role expectations](../framework/S7.3.0.md)** — Understand what FIASSE expects from you.

This path prioritizes the practices that save you the most rework. Requirements first, patterns second, then context.

This gives me a clear mental model: build software that creates value and can stay defensible as the system, risks, and business needs evolve—not by added tests at the end, but by design choices made from the start.
