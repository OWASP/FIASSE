---
name: securable-code
description: Apply the FIASSE Securable Software Engineering Model (SSEM) while writing, generating, modifying, or reviewing code. Use for any application code change, even when security is not mentioned - new features, API endpoints or handlers, input parsing, validation, error handling, logging, authentication or session logic, data access, state management, concurrency, and dependency additions or upgrades. Routes to the framework section the code at hand needs.
---

# Securable Code

Securable code is built to remain defensible as threats and requirements change. There is no static state of secure. Each change must leave the code able to be analyzed, modified, tested, and observed, with control enforced at every trust boundary. While coding, keep asking: "What can go wrong?"

## Every change

These qualities live in the code itself and are what reviews and measurement read:

- Small, single-purpose units with low complexity, no duplication, and loose coupling.
- Tests that exercise invalid, out-of-range, and exceptional inputs without modifying the code under test.
- Names and interfaces that do exactly what they say, with no hidden side effects.
- Structured logs at trust boundaries and for security-relevant events, capturing who, what, where, when, and outcome. External error messages stay generic; detail goes to internal logs.
- Every value the system must be able to trust is derived server-side, never accepted from a client.

## When to consult the framework

Read the matching section in `framework/` before writing, or while reviewing, code in these situations. Sections are short; read every one that matches.

| Situation | Read |
|-----------|------|
| Accepting external input: request bodies, query parameters, headers, files, messages, CLI arguments, deserialization | [S4.4.1](framework/S4.4.1.md) canonical input handling, [S4.3.0](framework/S4.3.0.md) boundary control |
| A client could influence an integrity-critical value: price, role, permission, object state, token algorithm | [S4.4.1](framework/S4.4.1.md) (Isolated Integrity Principle) |
| Error handling, failure paths, resource acquisition, concurrency, null handling, output encoding, or risky constructs (string-built queries, `eval()`, untrusted deserialization) | [S4.4.0](framework/S4.4.0.md) resilient coding |
| Logging, audit trails, metrics, instrumentation, operator feedback | [S2.6.3](framework/S2.6.3.md) transparency tactics, [S3.2.1](framework/S3.2.1.md) (Observability) |
| Authentication, credentials, tokens, signatures, attribution of actions | [S3.2.2](framework/S3.2.2.md) trustworthiness |
| Sensitive data at rest, in transit, or in logs and responses | [S3.2.2](framework/S3.2.2.md) (Confidentiality), [S3.2.3](framework/S3.2.3.md) (Integrity) |
| Behavior under load, fault tolerance, recovery, state transitions | [S3.2.3](framework/S3.2.3.md) reliability |
| Adding or upgrading a dependency | [S4.5.0](framework/S4.5.0.md) dependency management, [S4.6.0](framework/S4.6.0.md) stewardship |
| Structuring new modules or refactoring: naming, unit size, coupling, API shape | [S3.2.1](framework/S3.2.1.md) maintainability, [S2.7.0](framework/S2.7.0.md) least astonishment |
| Reviewing a changeset | [S4.2.1](framework/S4.2.1.md) threat awareness, plus the attribute files [S3.2.1](framework/S3.2.1.md) to [S3.2.3](framework/S3.2.3.md) |

The full section-by-section map, including which framework sections are process rather than code, is in [framework/code-index.md](framework/code-index.md). Its own links back into `docs/framework/` are for the source repo; within this skill, use the copies in `framework/` alongside it.

## Before finishing

- Re-read the changeset against the attribute families: Maintainability ([S3.2.1](framework/S3.2.1.md)), Trustworthiness ([S3.2.2](framework/S3.2.2.md)), Reliability ([S3.2.3](framework/S3.2.3.md)). Confirm the change strengthens them, or at minimum does not degrade them.
- A threat that cannot be addressed in code defines a requirement. State it explicitly in your summary; never leave it as a silent gap.
