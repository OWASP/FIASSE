# Contributing to OWASP FIASSE

Thanks for being here. FIASSE is an OWASP Incubator project and it is young enough that your disagreement is worth as much as your agreement. If you read something that seems wrong, unclear, or ridiculous, saying so out loud is a contribution.

Start with [the framework document](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md). Conversation happens in [GitHub Discussions on this repository](https://github.com/OWASP/FIASSE/discussions). That is the one home for it; older links pointing anywhere else are being retired.

## What this project is filling

FIASSE exists because of a gap, not because the field was short on frameworks. The established security frameworks do one of three jobs: they verify what was built (assurance), they state what security features a system must have (security requirements), or they harden the platforms code runs on (infrastructure). None of them tell a software engineer how to construct code so that security work keeps its value two months from now. That is the void FIASSE fills, and it is a construction problem rather than a verification problem.

So one specific contribution is not wanted: **mappings between FIASSE and other security frameworks.** FIASSE cooperates with them (ASVS still tells you what security features look like and how to verify, SAMM still scores maturity, etc.), but cooperation is not correspondence. A mapping table misses the category it was written to address, and it teaches readers to treat SSEM attributes as controls to be evidenced rather than properties to be engineered. If a mapping question is blocking real work, open a discussion and let us discuss it in the open; that conversation is useful even when the table is not.

## Ways to contribute

### Redteam a section

Pick one section of the framework document and attack it. Is the reasoning sound? Does the claim survive your last five years of experience? Would the guidance actually change what a team ships?

Open a discussion under **Ideas** or **Q&A**. The most useful reports name the section, quote the sentence that failed, and say what you expected instead. Public disagreement is the fastest way this document improves, and it is the reason Discussions exist.

### Ask a question, or mention how you used it

Every question that has to be asked marks a place where the writing did not carry its own weight, so questions in **Q&A** are data, not interruptions.

The same goes in the other direction. If you have taken SSEM vocabulary into a merge review, a requirements session, an architecture argument, or an agent prompt, describe what happened in **Show and tell**, including the parts that went badly. Adoption reports are the evidence base this project does not have yet.

### Fix something small

Typos, dead links, an awkward sentence, a definition that drifts between sections, an example that no longer matches the text. Open a pull request directly; no discussion required first. Small corrections are welcome and merge quickly. See [open issues](https://github.com/OWASP/FIASSE/issues) if you would rather pick something up than find it yourself.

### Review a draft in progress

Two guides are open on the roadmap: an SSEM Primer for software engineers, and a guide for AppSec practitioners on using and teaching FIASSE. Both want reviewers before publication, particularly reviewers willing to say a draft is not ready.

Ask in Slack `#project-fiasse` you will be sent the current draft.

### Contribute a worked example or code example

The framework states principles; examples make them teachable. Useful shapes include a before and after of a boundary that parses instead of validating, an integrity-critical value moved to an authoritative source, a test that turns a securable property into something verifiable in review, or an agent prompt that produced better code.

Language and stack do not matter, and small is better than comprehensive. Examples live in [securable-framework-supplement](https://github.com/Securability-Engineering/securable-framework-supplement). Open a discussion first if you want to check the shape before writing it.

### Kick the tires on the plugin

Install it in Claude Code:

```
/plugin marketplace add Securability-Engineering/securable-claude-plugin
/plugin install securable-claude-plugin@securable-claude-plugin-marketplace
/reload-plugins
```

Then point it at a codebase you know well and tell us where the review was wrong. A confident and incorrect result is the most valuable report we can get, because it marks a place where the guidance did not survive contact with a real system. Prompts for Copilot and OpenCode are in the same organization.

### Write or record your own take

A blog post, a thread, a newsletter item, a video, a chapter talk you gave anyway. Critical takes are as welcome as favorable ones, and a well argued objection published under your own name does more for the framework than another summary of it.

If you publish something, drop the link in Discussions so it can be read and answered. Public commentary is how a framework gets tested by people who owe it nothing.

### Host a chapter talk

Chapter leaders: a 30 to 45 minute talk is available, vendor neutral, with a live demo and hostile questions welcomed. Virtual anywhere, in person in the US Mountain and West regions. Ask in Slack `#project-fiasse` or email fiasse@owasp.org.

## How to submit a change

The standard OWASP flow applies:

1. [Join the OWASP Slack workspace](https://owasp.org/slack/invite) and find `#project-fiasse`.
2. Browse [OWASP Projects](https://owasp.org/projects/) and the [FIASSE project page](https://owasp.org/www-project-fiasse/) to see where this work sits.
3. Read the section of the framework document you intend to change.
4. Fork this repository and clone your fork.
5. Make your change on a branch, and review it locally.
6. Open a pull request describing what changed and why.

### Pull request guidelines

- **Consistent with the project's purpose.** FIASSE is not an assurance framework, and changes that pull it toward verification, scoring, or control catalogs will be discussed rather than merged.
- **One idea per pull request.** Small and separable review faster than comprehensive.
- **Say what problem the change solves.** A sentence about the reader who was confused is worth more than a summary of the diff.
- **Cite sources for factual claims.** The document carries a reference section; new claims are expected to join it rather than stand alone.

### House style for documentation changes

- Sentences do not use dash constructions. Use a colon, a semicolon, or parentheses instead. Hyphenated compound modifiers are fine.
- Name the role rather than referring to people generically: reviewer, software engineer, security practitioner, maintainer.
- Use the vocabulary the document defines, consistently. If a term needs a new meaning, that is a discussion before it is a pull request.

## Recognition

Contributors are listed in [CONTRIBUTORS.md](https://github.com/OWASP/FIASSE/blob/main/CONTRIBUTORS.md). If your work lands and your name does not appear there, that is a bug worth reporting.

## Code of Conduct

All contributors are asked to follow the [OWASP Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct). Argue with the ideas as hard as you like; extend the courtesy to the people.

## License

Contributions are accepted under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), the license this project carries. By opening a pull request you agree your contribution may be published under it.

## Where things live

| What | Where |
|---|---|
| Framework document | [`docs/securable_framework.md`](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md) |
| Discussion and feedback | [GitHub Discussions](https://github.com/OWASP/FIASSE/discussions) |
| Issues and small tasks | [GitHub Issues](https://github.com/OWASP/FIASSE/issues) |
| Project website | [owaspfiasse.org](https://owaspfiasse.org) |
| OWASP project page | [owasp.org/www-project-fiasse](https://owasp.org/www-project-fiasse/) |
| Chat | OWASP Slack `#project-fiasse` ([join](https://owasp.org/slack/invite)) |
| Plugins, prompts, and examples | [Securability-Engineering](https://github.com/Securability-Engineering) |