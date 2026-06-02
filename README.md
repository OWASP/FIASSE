# A Framework for Integrating Application Security into Software Engineering (FIASSE)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY%20SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

**Note:** This repository is an ongoing work. Contributions are welcome!

## Overview

TL;DR: please read the [DOC](docs/securable_framework.md). Explore [FIASSE website](https://fiasse.org). Visit [GitHub Discussions](https://github.com/owasp/www-project-fiasse/discussions) to contribute.

This repository contains resources and materials for the OWASP Framework for Integrating Application Security into Software Engineering (FIASSE). FIASSE (pronounced /feiz/ like 'phase') promotes a **developer-centric, principled approach** to build **securable** software — recognizing that security is a dynamic, ongoing process like development. It introduces the Securable Software Engineering Model (SSEM) as a **common design language** that uses established software engineering terms to integrate security into software architecture, design, and engineering. Integrating security into the principals that mold the code itself. The framework aims to build resilient applications that withstand threats over time.

## Purpose

To provide practical guidelines that **empower developers** to create securable software without requiring deep security expertise, and to guide security professionals in effectively integrating their security experience into software engineering. FIASSE achieves this through a **Software Engineering lens**, reducing cognitive load and fostering collaboration between development and security teams.

## How is it Different?

While assurance focused projects like the OWASP Top 10 highlight what to avoid (a block list), OWASP FIASSE provides a set of positive attributes and practices to follow (an allow list). This approach leverages existing software engineering skills to build securable software, rather than requiring developers to learn exploit techniques or adopt a vulnerability-focused mindset. The emphasis is on enabling practical, secure coding through familiar engineering principles.

By clearly defining security requirements within the development process, this framework ensures that business value is captured effectively. By establishing expectations this way, this significantly reduces the likelihood that security flaws will be discovered and need remediation later.

## Key Principles

- **The Securable Paradigm**: Acknowledging that software security is a dynamic, ongoing process, not a static "secure" state. It focuses on building inherent qualities into software to adapt to evolving threats.
- **Developer-Centric Security**: Empowering software engineers to autonomously build securable systems using familiar software engineering principles, rather than requiring them to adopt a penetration tester's mindset.
- **SSEM as a Common Design Language**: Utilizing the Securable Software Engineering Model (SSEM), which employs established software engineering terms (e.g., Analyzability, Modifiability, Testability) to define and discuss security attributes, making security more accessible to developers.
- **Aligning Security with Development & Business Goals**: Integrating security considerations seamlessly into the SDLC and assuring that security efforts support overarching business objectives and risk appetite.
- **Resiliently Adding Computing Value**: Ensuring software not only meets functional requirements but also possesses securable qualities that allow it to adapt, persist, and maintain integrity over time and under stress.
- **Requirements as a First-Class Citizen in AppSec**: Grounding secure software engineering in clearly defined security expectations and requirements from the outset.

## Repository Contents

- Definition and documentation of the Securable Software Engineering Model (SSEM)
- TODO: Implementation guides for the FIASSE methodology
- Examples have been moved to [Securability-Engineering/securable-framework-supplement](https://github.com/Securability-Engineering/securable-framework-supplement)

## Getting Started

1. Review the documentation in the `/docs` directory
2. Discuss the concepts and principles with your teams and in the [GitHub Discussions](https://github.com/Xcaciv/securable_software_engineering/discussions)
3. Start applying the principles in your software engineering practices like merge reviews and prompt engineering.

- Bonus: Install the plugin matching your IDE or AI powered commandline-agent of choice (e.g. GitHub Copilot, Claude Code, OpenCode, etc.) and use the provided prompts to generate securable code. Look for "Securability Engineering" or "FIASSE" in the prompt library.
- FIASSE is also included as part of the [OWASP Secure Agent Playbook](https://github.com/OWASP/secure-agent-playbook).

## Summary

This repository defines securable software as reliable, resilient and adaptable systems. It emphasizes that true security is an ongoing process, not a static achievement. It introduces the Securable Software Engineering Model (SSEM), which frames security as an inherent set of qualities of well-engineered software. To do this, it presents the attribute categories of Maintainability, Trustworthiness, and Reliability (which includes Resilience). FIASSE advocates for integrating security practices into the development workflow where they have the most impact. This moves from a "security as an afterthought" or a "shift left" approach to a proactive, collaborative model. The idea is that product owners, developers, and security professionals work together from the earliest stages of design, particularly through activities like security requirements definition, collaborative threat modeling, and acceptance criteria. This sets clear expectations for code activities and testing. Software engineers are given guidance on balancing flexibility and control. They are also given a definitive model for making security decisions. Ultimately, this empowers all stakeholders to contribute to building more robust, reliable, and inherently securable systems.

FIASSE differs from existing approaches by not requiring developers to become security experts or adopt an adversarial mindset. This approach aims to reduce the cognitive load on developers while ensuring that security can be confident that their concerns are addressed through specific attributes of code and software engineering processes.

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

Further milestones will be developed with the project team. Community input is welcome via [GitHub Discussions](https://github.com/owasp/www-project-fiasse/discussions).

## Complementary Resources

This repository complements the [FIASSE website](https://fiasse.org).

The [OWASP FIASSE](https://owasp.org/www-project-fiasse/) project is part of the [OWASP Foundation](https://owasp.org/), a non-profit organization focused on the mission of eliminating insecure software. The OWASP Foundation provides a wealth of resources and frameworks that align with the principles of FIASSE.

This framework is focused on Securable Software Engineering and is complemented by other OWASP projects:

- Assurance verification: [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- Assurance maturity: [OWASP Software Assurance Maturity Model (SAMM)](https://owasp.org/www-project-software-assurance-maturity-model/)
- Product security capabilities: [OWASP Product Security Capability Framework (PSCF)](https://owasp.org/www-project-product-security-capability-framework/)

OWASP also hosts numerous projects that document security requirements and features, such as [OWASP Mobile Application Security](https://mas.owasp.org/). The [OWASP Developer Guide](https://owasp.org/www-project-developer-guide/), which is a comprehensive resource for various other OWASP resources.

Another great resource for reference requirements and assurance practices is [OpenCRE](https://opencre.org/) which collects together and maps various security frameworks.

NIST [Secure Software Development Framework (SSDF)](https://csrc.nist.gov/publications/detail/sp/800-218/final) defines four phases that represent different facets for implementing secure software development practices. It aligns with FIASSE's principles by emphasizing the integration of security into the software development lifecycle.

The NCSC's [Software Security Code of Practice](https://www.ncsc.gov.uk/collection/software-security-code-of-practice-implementation-guidance) defines desired outcomes and some key strategies. While FIASSE framework focuses on first-level follow-on principles and strategies for achieving securable outcomes, intended for Development and Assurance teams to align with business strategies. SSEM specifies the attributes that are used to produce the desired outcomes, and the FIASSE methodology provides practical guidance for implementing these attributes in software engineering practices.

Carnegie Mellon University's [CERT](https://www.cert.org/) is a set of language-level rules providing both "what not to do" examples showing vulnerable code patterns and "what to do" examples. FIASSE complements these rules by providing a principled approach that helps programmers understand the "why?" behind securable code.

Software Factory Security Framework ([SF2](https://sf2framework.com/)) "provides security leaders with a strategic approach to scaling security capabilities while improving business outcomes." It is an organizational level framework that complements FIASSE's focus on software engineering practices.

## Contributing

Contributions to improve documentation and examples are welcome. Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) - see the [LICENSE](licence.txt) file for details.

## Acknowledgments

This project is a collaborative effort by the OWASP community. We thank all contributors for their valuable input and dedication to improving software security.

There is a [list of contributors](CONTRIBUTORS.md) who have participated in this project. Some early contributors that help shape the initial concepts and redteam the ideas.
