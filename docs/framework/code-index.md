# FIASSE Code Application Index

This index separates the sections of the [FIASSE framework](../securable_framework.md) that pertain directly to code from the sections that guide process, roles, and adoption. Use it to decide which section document to consult while writing, generating, modifying, or reviewing code. Each section file is short; read every section whose trigger matches the work at hand.

## Sections that apply directly to code

| Section | Title | Apply when |
|---------|-------|------------|
| [S2.6.3](S2.6.3.md) | Transparency Tactics | Adding logging, audit trails, metrics, or instrumentation. Any change that touches a security-sensitive event such as a permission change, data access, or configuration update. |
| [S2.7.0](S2.7.0.md) | The Principle of Least Astonishment | Naming functions and interfaces, designing APIs, or whenever behavior could surprise a caller through hidden side effects, unusual control flow, or inconsistent conventions. |
| [S3.2.0](S3.2.0.md) | Core Securable Attributes | Orientation for any change. Introduces the ten attributes every piece of code is read against. |
| [S3.2.1](S3.2.1.md) | Maintainability (Analyzability, Modifiability, Testability, Observability) | Structuring or refactoring code. Governs unit size, complexity, duplication, coupling, test isolation, and code-level instrumentation. |
| [S3.2.2](S3.2.2.md) | Trustworthiness (Confidentiality, Accountability, Authenticity) | Handling sensitive data, authentication, credentials, tokens, or signatures, and whenever actions must be attributable to a specific entity. |
| [S3.2.3](S3.2.3.md) | Reliability (Availability, Integrity, Resilience) | Designing for load, failure, and recovery. Protecting data accuracy and managing state transitions. |
| [S4.2.1](S4.2.1.md) | Code-Level Threat Awareness | Reviewing or completing a changeset. Ask "What can go wrong?" within the scope of the change. |
| [S4.3.0](S4.3.0.md) | The Boundary Control Principle | Data crossing a trust boundary (user to application, application to database, service to service), or exposing flexible interior logic through an interface. |
| [S4.4.0](S4.4.0.md) | Resilient Coding | Writing error handling, resource management, concurrency, null handling, or output encoding. Required reading when a construct is inherently risky: string-built queries, `eval()`, or deserialization of untrusted data. |
| [S4.4.1](S4.4.1.md) | Canonical Input Handling (Canonical Parsing, Isolated Integrity) | Accepting any external input: request bodies, query parameters, headers, files, messages, CLI arguments. Also whenever a client could supply an integrity-critical value such as a price, role, object state, or token algorithm. |
| [S4.5.0](S4.5.0.md) | Dependency Management | Before adding a library or upgrading an existing one. |
| [S4.6.0](S4.6.0.md) | Dependency Stewardship | Revisiting dependencies already in the system: manifests, lockfiles, or scheduled maintenance. |

## Process, role, and adoption sections

These sections shape requirements, reviews, team practice, and organizational adoption. Consult them when working on process or planning, not while writing code. The code-facing sections above already carry their implications.

- [S1.1.0](S1.1.0.md), [S1.2.0](S1.2.0.md): introduction, purpose, and scope.
- [S2.1.0](S2.1.0.md) to [S2.5.0](S2.5.0.md): foundational principles, the securable paradigm, the quality-security relationship, and alignment between security and development.
- [S2.6.0](S2.6.0.md) to [S2.6.2](S2.6.2.md): the Transparency Principle and its relationship to Maintainability and Trustworthiness (the actionable tactics are in [S2.6.3](S2.6.3.md)).
- [S3.1.0](S3.1.0.md): SSEM model overview and design language.
- [S4.1.0](S4.1.0.md) to [S4.1.2](S4.1.2.md): setting expectations and integrating security into requirements.
- [S4.2.0](S4.2.0.md), [S4.2.2](S4.2.2.md): formal threat modeling and its solution framework (the code-level practice is [S4.2.1](S4.2.1.md)).
- [S5.1.0](S5.1.0.md) to [S5.3.0](S5.3.0.md): integrating security into development processes and merge reviews.
- [S6.1.0](S6.1.0.md) to [S6.3.0](S6.3.0.md): common AppSec anti-patterns.
- [S7.1.0](S7.1.0.md) to [S7.4.0](S7.4.0.md): roles and responsibilities.
- [S8.1.0](S8.1.0.md) to [S8.2.3](S8.2.3.md): organizational adoption and indicators of effectiveness.
- [S9.0.0](S9.0.0.md), [S10.0.0](S10.0.0.md): conclusion and references.
