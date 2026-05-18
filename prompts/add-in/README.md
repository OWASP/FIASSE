# Securable Engineering Prompt Add-In

This folder contains a prompt add-in you can append to a normal code-generation prompt when you want securable outcomes.

The add-in is in:
- `securable-engineering.prompt.md`

It applies the OWASP FIASSE / SSEM qualities so generated code is designed to remain defensible as requirements and threats evolve.

## Intended Usage

Use your normal request first (feature, bug fix, refactor, API, etc.), then append the full contents of `securable-engineering.prompt.md`.

This is meant to steer implementation behavior, not replace architecture review, threat modeling, or testing.

## Recommended Prompt Pattern

1. Write your base coding task.
2. Add your project context (language, framework, constraints).
3. Append the full add-in text from `securable-engineering.prompt.md`.
4. Optionally add output expectations (tests, logging, rationale).

## Copy/Paste Template

```text
Task:
<describe the code you want generated or changed>

Project context:
- Language/runtime: <example: Python 3.12>
- Framework: <example: FastAPI>
- Constraints: <performance, backward compatibility, deployment model>

Securable outcome requirements:
Append and apply the full text from prompts/add-in/securable-engineering.prompt.md.

Deliverables:
- Updated code
- Tests for valid, invalid, and edge cases
- Structured security-relevant logs at trust boundaries
- Brief explanation of how the implementation satisfies the securable attributes
```

## Example

```text
Implement a password reset endpoint for existing users.
Use Node.js + Express and keep compatibility with current API responses.
Append and apply the full text from prompts/add-in/securable-engineering.prompt.md.
Include unit tests and structured logs for authentication events.
```

## Notes

- Prefer appending the add-in exactly as written to avoid weakening requirements.
- If your task is narrow, keep the base request short and let the add-in enforce security quality expectations.
- If your repository has stricter security rules, include those before appending this add-in.