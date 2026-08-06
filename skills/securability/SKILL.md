---
name: securability
description: Write code that stays defensible as threats and requirements change. Use for any application code - features, endpoints, input handling, data access, auth, error handling, state, concurrency - even when security is not explicitly requested.
---

# Securability

There is no static state of secure. Code must be built so security can be maintained as the system evolves. While coding, ask: "What can go wrong?"

Resiliently add computing value: every change should deliver working capability and leave the system able to withstand what comes after it. Value without resilience is capability the business will lose later. Resilience without value is waste.

## Maintainability

- **Analyzability** - Keep units small, simple, and free of duplication. A vulnerability's cause must be findable quickly.
- **Modifiability** - Keep modules loosely coupled so a fix or change doesn't cascade into unrelated code.
- **Testability** - Give functions clear inputs and outputs with no hidden dependencies. Cover invalid input and edge cases, not just the happy path. Never modify code just to make it testable.
- **Observability** - Log security-relevant events (auth, boundary crossings, validation outcomes) as structured data: who, what, where, when, outcome. Instrument the code itself; don't rely on external tooling alone.

## Trustworthiness

- **Confidentiality** - Never expose sensitive data in logs, error messages, or responses. Apply least privilege to data and resource access.
- **Accountability** - Every security-relevant action must be attributable to a specific entity, via immutable, auditable logs.
- **Authenticity** - Verify identity at every trust boundary. Log authentication and authorization events. Use signatures or checksums where origin and integrity must be provable.

## Reliability

- **Availability** - Design for graceful degradation. A failing component must not take the system down.
- **Integrity** - Apply the **Isolated Integrity Principle**: never trust a client-supplied value for a server-authoritative fact (price, role, permission, state). Derive it server-side.
- **Resilience** - Validate, canonicalize, and sanitize input at every trust boundary (**Canonical Input Handling**). Encode output for its destination. Handle errors explicitly and fail to a known safe state without leaking internals. Avoid dangerous constructs (string-built queries, `eval()`, untrusted deserialization); isolate them behind a narrow interface if unavoidable.

## Boundary Control Principle

Keep the interior of the system flexible; enforce strict control only at trust boundaries (user to app, app to database, service to service). Uncontrolled flexibility at a boundary is an attack surface. Controlled flexibility everywhere else is what keeps the system maintainable.

## Principle of Least Astonishment

Code should behave exactly as its name and interface suggest: no hidden side effects, no surprising control flow. Predictable code is easier to analyze, secure, and trust.
