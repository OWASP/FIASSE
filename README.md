# A Framework for Integrating Application Security into Software Engineering (FIASSE)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY%20SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

**Note:** This repository is an ongoing work. Contributions are welcome!

## Overview

TL;DR: please read the [DOC](docs/securable_framework.md). Explore [FIASSE website](https://fiasse.org). Visit [GitHub Discussions](https://github.com/OWASP/FIASSE/discussions) to contribute.

This repository contains resources and materials for the OWASP Framework for Integrating Application Security into Software Engineering (FIASSE). FIASSE (pronounced /feiz/ like 'phase') is a vendor-independent framework that promotes a **developer-centric, principled approach** to building **securable** software. It recognizes that security is a dynamic, ongoing process like development. It introduces the Securable Software Engineering Model (SSEM) as a **common design language** that uses established software engineering terms to integrate security into software architecture, design, and engineering by embedding security in the principles that shape the code itself. The framework enables development teams to resiliently add computing value while reducing the probability of material impact from cyber events throughout the code's lifespan.

FIASSE is a creational framework. It addresses how security is implemented in software, connecting engineering decisions directly to securable outcomes. It is not an assurance framework, a maturity model, or a replacement for control catalogs or vulnerability metrics. It complements those approaches and eases downstream pressure on assurance and compliance.

## Purpose

To provide practical guidelines that **empower developers** to create securable software without requiring deep security expertise, and to guide security professionals in effectively integrating their security experience into software engineering. FIASSE achieves this through a **Software Engineering lens**, reducing cognitive load and fostering collaboration between development and security teams.

## How is it Different?

While assurance focused projects like the OWASP Top 10 highlight what to avoid (a block list), OWASP FIASSE provides a set of positive attributes and practices to follow (an allow list). This approach leverages existing software engineering skills to build securable software, rather than requiring developers to learn exploit techniques or adopt a vulnerability-focused mindset. The emphasis is on enabling practical, secure coding through familiar engineering principles.

By clearly defining security's practical role within the development process, this framework ensures that business value is captured effectively. Setting explicit security expectations before code is written reduces the likelihood that security flaws will be discovered and need remediation later. Effective adoption should improve existing assurance metrics, reduce findings churn, produce more durable fixes, and shorten remediation time.

## Core Values

FIASSE is oriented by four core values. Each expresses a relative preference: both sides have worth, but when choices must be made, FIASSE favors the left.

- **Securable Attributes over Security Controls**: prefer the engineering qualities that let a system be built and kept defensible over security controls put in after the fact to make up for weaknesses.
- **Participation over Assessment**: prefer structured engagement between security and development throughout the lifecycle over evaluation performed after the work is done.
- **Engineering First Principles over Security Jargon**: prefer grounding in established software engineering first principles over security-specific jargon or adversarial heuristics.
- **Business Value over Security Activity**: prefer security that sustains the organization's value creation over security pursued as an end in itself.

## Key Principles

- **The Securable Paradigm**: There is no static state of "secure." A system declared secure today may be vulnerable tomorrow. FIASSE redirects the engineering goal from "is it secure?" to "is it built so that security can be maintained?" through adaptive resilience, evolutionary security, and continuous improvement.
- **Resiliently Add Computing Value**: The primary directive of software engineering in a business context. Software must meet functional requirements while sustaining the securable qualities that let it withstand the change, stress, and attack that follow each change.
- **Security Mission: Reducing Material Impact**: The mission of security is to reduce the probability of material impact of a cyber event. Complete elimination of breaches is not a practical business goal, so security strategies must align with business objectives and risk appetite.
- **The Quality-Security Relationship**: Security cannot exceed software quality. The qualities that make software easy to understand, change, test, and observe are the same qualities that make it possible to secure. Investment in engineering quality is a security investment.
- **Developer-Centric Security**: Empowering software engineers to build securable systems using familiar software engineering principles, rather than requiring them to adopt a penetration tester's mindset.
- **SSEM as a Common Design Language**: Utilizing established software engineering terms (e.g., Analyzability, Modifiability, Testability) to define and discuss security attributes. This makes security accessible to developers and gives security professionals a shared basis for assessment.
- **Aligning Security with Development and Business Goals**: Security and development are complementary, not adversarial. AppSec participates early in the SDLC, particularly during requirements gathering and feature planning, so expectations are explicit before code is written.
- **The Transparency Principle**: Systems are designed so authorized parties can understand internal state and behavior. Structured logging, instrumentation, and audit trails are built into the code rather than supplied by external tooling alone.
- **The Principle of Least Astonishment**: Systems behave in ways that are intuitive and predictable to users, developers, and administrators. Predictability aids analysis, reduces cognitive burden, and makes trust boundaries clear.
- **Requirements as a First-Class Citizen in AppSec**: Security Features, Threat Scenarios, and Security Acceptance Criteria are delivered through the requirements process. Vulnerabilities commonly trace to an expectation that was never specified, so that gap belongs in the requirements process.

## Engineering Principles

Section 4 of the framework gives developers principles that apply directly at the code level:

- **The Boundary Control Principle**: Flexibility within a system's interior is an engineering asset to be preserved. Control at every trust boundary is a security requirement to be enforced.
- **Canonical Input Handling**: Canonicalize, validate, and sanitize input at the point of entry. The **Canonical Parsing Principle** parses external input into a canonical internal type at the boundary and fails closed when parsing does not succeed.
- **The Isolated Integrity Principle**: Integrity-critical values such as prices, roles, and object state are derived from authoritative server-side sources. They are never accepted directly from a client.
- **Resilient Coding**: Defensive coding practices enforce predictable execution. These include strong typing, input validation at trust boundaries, output encoding, comprehensive error handling, safe resource management, graceful and secure failure, and least privilege at the code level.
- **Dependency Stewardship**: Apply SSEM attributes when selecting, integrating, monitoring, and maintaining dependencies for the life of the relationship.

## The Securable Software Engineering Model (SSEM)

SSEM defines the attributes that make software securable. Teams set goals for each attribute, assess systems against them, and improve incrementally. The attributes are organized into three categories:

| **Maintainability** | **Trustworthiness** | **Reliability** |
|:--------------------|:-------------------:|----------------:|
| Analyzability       | Confidentiality     | Availability    |
| Modifiability       | Accountability      | Integrity       |
| Testability         | Authenticity        | Resilience      |
| Observability       |                     |                 |

SSEM has no Authorization attribute by design. Authorization is a security feature that is gathered as a requirement and implemented against acceptance criteria. The attributes above are what make such a feature securable. Appendix A of the framework describes approaches for measuring each attribute.

## Repository Contents

- [docs/securable_framework.md](docs/securable_framework.md): the complete FIASSE framework and SSEM specification as a single document.
- [docs/framework/](docs/framework/): the framework split into one file per section. These section files are the source of truth for the framework. The [code index](docs/framework/code-index.md) separates the sections that apply directly to code from the process, role, and adoption sections. [llms.txt](docs/framework/llms.txt) provides an index for language models.
- [skills/](skills/): FIASSE and SSEM packaged as skills for AI coding agents (see below).
- TODO: Implementation guides for the FIASSE methodology
- Examples have been moved to [Securability-Engineering/securable-framework-supplement](https://github.com/Securability-Engineering/securable-framework-supplement)

## Getting Started

1. Review the documentation in the [docs](docs/) directory. Start with the [full framework](docs/securable_framework.md), or use the [code index](docs/framework/code-index.md) to find the sections that apply to the code at hand.
2. Discuss the concepts and principles with your teams and in the [GitHub Discussions](https://github.com/OWASP/FIASSE/discussions)
3. Start applying the principles in your software engineering practices like requirements gathering, merge reviews, and prompt engineering.
4. Follow the adoption steps in Section 8 of the framework: assess current practices, integrate SSEM terminology, identify key influencers, educate and train teams, adopt agentic AppSec tooling as capacity relief, foster collaboration, and monitor and improve continuously.

- Bonus: Install the plugin matching your IDE or AI powered commandline-agent of choice (e.g. GitHub Copilot, Claude Code, OpenCode, etc.) and use the provided prompts to generate securable code. Look for "Securability Engineering" or "FIASSE" in the prompt library.
- FIASSE is also included as part of the [OWASP Secure Agent Playbook](https://github.com/OWASP/secure-agent-playbook).

## Skills for AI Coding Agents

The [`skills/`](skills/) directory packages FIASSE/SSEM as ready-to-use skills for AI coding agents that support the [Agent Skills](https://code.claude.com/docs/en/skills) format (e.g. Claude Code). Copy the skill directory you need into your agent's skills path.

- **[`securability`](skills/securability/SKILL.md)**: A compact, fully self-contained reference covering all ten SSEM attributes and the core principles (No Static State of Secure, Isolated Integrity, Canonical Input Handling, Boundary Control, Least Astonishment). Intended as the default for everyday code generation and review.
- **[`securable-code`](skills/securable-code/SKILL.md)**: A deep-dive skill for context-heavy, architecturally complex work, such as trust boundary design, authentication systems, multi-service data flows, or dependency architecture. It routes to the specific bundled framework section (in `skills/securable-code/framework/`) relevant to the code at hand, trading extra context for the source framework's full reasoning.

Use `securability` by default; reach for `securable-code` when the design decisions are non-obvious enough to warrant reading the framework itself.

## Summary

This repository defines securable software as software built to remain defensible: structured so that it can be understood, changed, tested, and hardened as the world around it changes. It emphasizes that security is an ongoing process, not a static achievement. It introduces the Securable Software Engineering Model (SSEM), which frames security as an inherent set of qualities of well-engineered software. To do this, it presents the attribute categories of Maintainability, Trustworthiness, and Reliability (which includes Resilience). FIASSE advocates for integrating security practices into the development workflow where they have the most impact. This moves from a "security as an afterthought" or a "shift left" approach to a proactive, collaborative model. Product owners, developers, and security professionals work together from the earliest stages of design, particularly through security requirements definition, collaborative threat modeling, and security acceptance criteria. This sets clear expectations for code activities and testing. Merge reviews act as guardrails, not gates. Every merge produces an advisory Securability Report, and gating is a policy decision with an override path. Findings from validation and production are treated as empirical intelligence that points upstream to the stage that could have prevented them. Software engineers are given guidance on balancing flexibility and control. They are also given a definitive model for making security decisions. Ultimately, this empowers all stakeholders to contribute to building more robust, reliable, and inherently securable systems.

FIASSE differs from existing approaches by not requiring developers to become security experts or adopt an adversarial mindset. It names common AppSec anti-patterns, such as "Shoveling Left" raw tool output onto developers and exploit-first training, and replaces them with the Actionable Security Intelligence Principle. This approach aims to reduce the cognitive load on developers while ensuring that security practitioners can be confident that their concerns are addressed through specific attributes of code and software engineering processes.

FIASSE intends to be open, approachable, and collaborative.

## Roadmap

Initial milestones for the FIASSE project:

- **Project Foundation**
  - Establishment of project governance, contribution guidelines, and communication channels.
- **Core Specifications**
  - Formal publication of the FIASSE framework and SSEM specification, detailing core attributes and integration strategies.
- **Adoption and Educational Resources**
  - An SSEM Primer to introduce the model and its application.
  - A collection of initial use cases and adoption patterns to illustrate practical benefits.
  - Ongoing development of implementation guides, examples, and other educational materials.

Further milestones will be developed with the project team. Community input is welcome via [GitHub Discussions](https://github.com/OWASP/FIASSE/discussions).

## Complementary Resources

This repository complements the [FIASSE website](https://fiasse.org).

The [OWASP FIASSE](https://owasp.org/www-project-fiasse/) project is part of the [OWASP Foundation](https://owasp.org/), a non-profit organization focused on the mission of eliminating insecure software. The OWASP Foundation provides a wealth of resources and frameworks that align with the principles of FIASSE.

This framework is focused on Securable Software Engineering and is complemented by other OWASP projects:

- Security feature verification and a ready-made security requirements library: [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- Assurance maturity: [OWASP Software Assurance Maturity Model (SAMM)](https://owasp.org/www-project-samm/)
- Product security compliance: [OWASP Product Security Capability Framework (PSCF)](https://owasp.org/www-project-product-security-capability-framework/)

OWASP also hosts numerous projects that document security requirements and features, such as [OWASP Mobile Application Security](https://mas.owasp.org/). The [OWASP Developer Guide](https://owasp.org/www-project-developer-guide/) is a comprehensive resource for various other OWASP resources.

Another great resource for reference requirements and assurance practices is [OpenCRE](https://opencre.org/) which collects together and maps various security frameworks.

Control catalogs such as NIST SP 800-53, ISO/IEC 27001 Annex A, and PCI DSS support risk management, assurance, and external evaluation. FIASSE does not replace them. It treats them as input to requirements gathering, where a catalog control is translated into a security requirement with acceptance criteria before development implements it.

NIST [Secure Software Development Framework (SSDF)](https://csrc.nist.gov/publications/detail/sp/800-218/final) defines a core set of secure software development practices organized into four groups. FIASSE does not define such a practice set. It aligns with SSDF by emphasizing the integration of security into the software development lifecycle.

The NCSC's [Software Security Code of Practice](https://www.ncsc.gov.uk/collection/software-security-code-of-practice-implementation-guidance) defines desired outcomes and some key strategies. FIASSE focuses on first-level follow-on principles and strategies for achieving securable outcomes, intended for Development and Assurance teams to align with business strategies. SSEM specifies the attributes that are used to produce the desired outcomes, and the FIASSE methodology provides practical guidance for implementing these attributes in software engineering practices.

Carnegie Mellon University's [CERT](https://www.cert.org/) Secure Coding Standards are a set of language-level rules providing both "what not to do" examples showing vulnerable code patterns and "what to do" examples. FIASSE complements these rules by providing a principled approach that helps programmers understand the "why?" behind securable code.

Software Factory Security Framework ([SF2](https://sf2framework.com/)) "provides security leaders with a strategic approach to scaling security capabilities while improving business outcomes." It is an organizational level framework that complements FIASSE's focus on software engineering practices.

## Contributing

Contributions to improve documentation and examples are welcome. Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) - see the [LICENSE](licence.txt) file for details.

## Acknowledgments

This project is a collaborative effort by the OWASP community. We thank all contributors for their valuable input and dedication to improving software security.

There is a [list of contributors](CONTRIBUTORS.md) who have participated in this project. Some early contributors helped shape the initial concepts and redteam the ideas.
