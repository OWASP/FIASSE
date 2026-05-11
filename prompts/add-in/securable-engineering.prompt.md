## Code Quality Standard: OWASP FIASSE / SSEM

All generated code must exhibit the ten Securable Software Engineering Model (SSEM) attributes. "Securable" means built to remain defensible as requirements and threats evolve — not evaluated as secure at a point in time.

### Maintainability
- **Analyzability** — Use clear naming, minimal cyclomatic complexity, no duplication, and purposeful comments. Code must be readable enough that a vulnerability's cause can be located quickly.
- **Modifiability** — Keep modules loosely coupled. Isolate change-prone logic so security-relevant updates do not cascade into unintended behavior.
- **Testability** — Write functions with clear inputs, outputs, and no hidden dependencies. Cover valid inputs, invalid inputs, and edge cases with unit tests. Code under test must not need to be modified to be tested. 
- **Observability** — Instrument code at the source. Log security-relevant events (authentication, authorization, trust boundary crossings, validation outcomes) as structured data capturing who, what, where, when, and outcome. Expose operational metrics (auth failures, error rates, resource utilization) via a standardized API. Do not rely solely on external tooling for visibility — a system not instrumented at the code level is opaque by construction.

### Trustworthiness
- **Confidentiality** — Never expose sensitive data in logs, error messages, responses, or client-visible state. Apply least privilege to data and resources. Protect data at rest and in transit.
- **Accountability** — Produce immutable, auditable logs for every security-sensitive action. Logs must uniquely attribute each action to a specific entity and support incident response without ambiguity.
- **Authenticity** — Verify entity identity at all trust boundaries. Use Defendable Authentication: design the authentication mechanism so it can be analyzed, modified, tested, and adapted as threats evolve. Log all authentication and authorization events. Apply digital signatures or checksums where origin and integrity must be provable.

### Reliability
- **Availability** — Design for graceful degradation and fault tolerance. Protect against resource exhaustion and denial-of-service conditions. Components must fail without taking the system down.
- **Integrity** — Apply the **Derived Integrity Principle**: never accept client-supplied values for server-authoritative facts (prices, roles, permissions, state). Derive them server-side from a trusted source. Manage state transitions through internal state machines. Use cryptographic validation for data at rest and in transit.
- **Resilience** — Write defensively. Validate, canonicalize, and sanitize all input at trust boundaries. Encode all output destined for other systems or interpreters. Use strong typing. Handle errors explicitly, failing to a known safe state without leaking internals. Acquire and release resources deterministically. Avoid dangerous constructs (string-concatenated queries, `eval()`, deserialization of untrusted data); where unavoidable, encapsulate behind a narrow interface.

### Boundary Control (apply at every trust boundary)
1. **Canonicalize/Normalize** — Enforce expected type, format, length, and range.
2. **Validate** — Allowlist known-good values; reject and log anything outside scope (Request Surface Minimization: access only the specific fields required, not the full envelope).
3. **Sanitize** — Remove or neutralize harmful content before passing values to downstream logic.
4. **Log deviations** — Unexpected fields or values must be logged with source, timestamp, and session context. In sensitive contexts, prefer reject-and-log over silent discard.

### Cross-cutting: Principle of Least Astonishment
Code must behave as its name and interface imply — no hidden side effects, state changes must be explicitly documented and predictable based on the interface contract, no unintuitive control flow. Predictable behavior reduces cognitive load, supports Analyzability, and makes trust boundaries obvious.