# A Framework for Integrating Application Security into Software Engineering (FIASSE)

## Abstract

This document describes the Framework for Integrating Application Security into Software Engineering (FIASSE), a vendor-independent framework that embeds application security into the software engineering discipline, and its core component, the Securable Software Engineering Model (SSEM). SSEM provides a design language grounded in established software engineering terminology, defining inherent security attributes, organized under Maintainability, Trustworthiness, and Reliability, that characterize securable software. Together they enable development teams to resiliently add computing value while reducing the probability of material impact from cyber events across the lifespan of the system.

---

## Table of Contents

- [A Framework for Integrating Application Security into Software Engineering (FIASSE)](#a-framework-for-integrating-application-security-into-software-engineering-fiasse)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [1.1. The Application Security Challenge](#11-the-application-security-challenge)
    - [1.2. Document Purpose and Scope](#12-document-purpose-and-scope)
  - [2. Foundational Principles](#2-foundational-principles)
    - [2.1. The Securable Paradigm: No Static Secure State](#21-the-securable-paradigm-no-static-secure-state)
    - [2.2. Resiliently Add Computing Value](#22-resiliently-add-computing-value)
    - [2.3. Security Mission: Reducing Material Impact](#23-security-mission-reducing-material-impact)
    - [2.4. Aligning Security with Development](#24-aligning-security-with-development)
    - [2.5. The Transparency Principle](#25-the-transparency-principle)
    - [2.6. The Principle of Least Astonishment](#26-the-principle-of-least-astonishment)
  - [3. The Securable Software Engineering Model (SSEM)](#3-the-securable-software-engineering-model-ssem)
    - [3.1. Model Overview and Design Language](#31-model-overview-and-design-language)
    - [3.2. Core Securable Attributes](#32-core-securable-attributes)
      - [3.2.1. Maintainability](#321-maintainability)
        - [3.2.1.1. Analyzability](#3211-analyzability)
        - [3.2.1.2. Modifiability](#3212-modifiability)
        - [3.2.1.3. Testability](#3213-testability)
        - [3.2.1.4. Observability](#3214-observability)
      - [3.2.2. Trustworthiness](#322-trustworthiness)
        - [3.2.2.1. Confidentiality](#3221-confidentiality)
        - [3.2.2.2. Accountability](#3222-accountability)
        - [3.2.2.3. Authenticity](#3223-authenticity)
      - [3.2.3. Reliability](#323-reliability)
        - [3.2.3.1. Availability](#3231-availability)
        - [3.2.3.2. Integrity](#3232-integrity)
        - [3.2.3.3. Resilience](#3233-resilience)
  - [4. Practical Guidance for Securable Software Development](#4-practical-guidance-for-securable-software-development)
    - [4.1. Establishing Clear Expectations](#41-establishing-clear-expectations)
      - [4.1.1. Proactive Communication](#411-proactive-communication)
      - [4.1.2. Integrating Security into Requirements](#412-integrating-security-into-requirements)
    - [4.2. Threat Modeling](#42-threat-modeling)
      - [4.2.1. Code-Level Threat Awareness](#421-code-level-threat-awareness)
      - [4.2.2. Threat Modeling Solution Framework](#422-threat-modeling-solution-framework)
    - [4.3. The Boundary Control Principle](#43-the-boundary-control-principle)
    - [4.4. Resilient Coding](#44-resilient-coding)
      - [4.4.1. Canonical Input Handling](#441-canonical-input-handling)
        - [4.4.1.1. The Request Surface Minimization Principle](#4411-the-request-surface-minimization-principle)
        - [4.4.1.2. The Derived Integrity Principle](#4412-the-derived-integrity-principle)
    - [4.5. Dependency Management](#45-dependency-management)
    - [4.6. Dependency Stewardship](#46-dependency-stewardship)
  - [5. Integrating Security into Development Processes](#5-integrating-security-into-development-processes)
    - [5.1. Natively Extending Development Processes](#51-natively-extending-development-processes)
    - [5.2. The Role of Merge Reviews](#52-the-role-of-merge-reviews)
    - [5.3. Early Integration: Planning and Requirements](#53-early-integration-planning-and-requirements)
  - [6. Common AppSec Anti-Patterns](#6-common-appsec-anti-patterns)
    - [6.1. The Control-Catalog Fallacy](#61-the-control-catalog-fallacy)
    - [6.2. The "Shoveling Left" Phenomenon](#62-the-shoveling-left-phenomenon)
      - [6.2.1. Ineffective Vulnerability Reporting](#621-ineffective-vulnerability-reporting)
      - [6.2.2. Pitfalls of Exploit-First Training](#622-pitfalls-of-exploit-first-training)
    - [6.3. Strategic Use of Security Output](#63-strategic-use-of-security-output)
  - [7. Roles and Responsibilities](#7-roles-and-responsibilities)
    - [7.1. The Role of the Security Team](#71-the-role-of-the-security-team)
    - [7.2. Senior Software Engineers](#72-senior-software-engineers)
    - [7.3. Developing Software Engineers](#73-developing-software-engineers)
    - [7.4. Product Owners and Managers](#74-product-owners-and-managers)
  - [8. Organizational Adoption of FIASSE](#8-organizational-adoption-of-fiasse)
  - [9. Conclusion](#9-conclusion)
  - [10. References](#10-references)
  - [Appendix A: Measuring SSEM Attributes](#appendix-a-measuring-ssem-attributes)
    - [A.1. Measuring Maintainability](#a1-measuring-maintainability)
      - [A.1.1. Analyzability](#a11-analyzability)
      - [A.1.2. Modifiability](#a12-modifiability)
      - [A.1.3. Testability](#a13-testability)
      - [A.1.4. Observability](#a14-observability)
    - [A.2. Measuring Trustworthiness](#a2-measuring-trustworthiness)
      - [A.2.1. Confidentiality](#a21-confidentiality)
      - [A.2.2. Accountability](#a22-accountability)
      - [A.2.3. Authenticity](#a23-authenticity)
    - [A.3. Measuring Reliability](#a3-measuring-reliability)
      - [A.3.1. Availability](#a31-availability)
      - [A.3.2. Integrity](#a32-integrity)
      - [A.3.3. Resilience](#a33-resilience)

---

## 1. Introduction

### 1.1. The Application Security Challenge

Organizations invest significantly in secure coding initiatives and security testing tools, yet often do not observe commensurate improvement in application security (AppSec) outcomes. Tangible progress can feel slow, and friction between AppSec and Development teams is a persistent impediment.

Generative AI tools for code generation have added a new dimension to this challenge. These tools can accelerate development, but they also risk propagating insecure patterns if not guided by sound engineering principles. Ensuring AI-generated code is securable requires the same foundational approach as any other code.

A more fundamental problem also persists: many well-intentioned strategies, including the prevalent "shift left" movement, have produced disappointing results in practice, failing to produce lasting change in the software being built. The failure is not in the timing. Integrating security earlier is sound. The problem is the pattern of delivering training and testing outputs in forms that developers cannot act on within their normal engineering focus. A key question underlies all of these challenges: how can development teams consistently produce securable code without requiring developers to acquire deep security expertise?

### 1.2. Document Purpose and Scope

This document introduces the Framework for Integrating Application Security into Software Engineering (FIASSE, pronounced /feiz/) and its core component, the Securable Software Engineering Model (SSEM, pronounced /si:m/).

FIASSE provides the overarching strategic approach and practices that integrate security into software engineering. SSEM, as a model within FIASSE, offers a common design language (a shared set of terms and concepts that gives a team a common vocabulary for discussing and evaluating a system's qualities) and a set of measurable attributes that guide the creation of securable software, aligning AppSec objectives with business goals.

The term "securable" is used throughout this document as a deliberate choice over "secure." Where "secure" implies a condition that is either achieved or not, "securable" describes software that is built to remain defensible: structured so that it can be understood, changed, tested, and hardened as the world around it changes. Section 2.1 develops this concept in full.

This document covers the following topics:

- Foundational principles underpinning FIASSE and SSEM (Section 2)
- The core attributes of securable software as defined by SSEM (Section 3.2)
- Practical guidance for developers to build securable code (Section 4)
- Strategies for integrating FIASSE into existing development processes (Section 5)
- Common pitfalls in AppSec and how FIASSE addresses them (Section 6)
- The roles of engineering and security personnel in adopting FIASSE (Section 7)
- The evolution of FIASSE in response to emerging trends and strategies for organizational adoption (Section 8)

This document is intended for Software Engineers, Application Security professionals, Product Security Engineers, engineering managers, and anyone involved in software development who seeks to improve application security outcomes. Within security organizations, FIASSE serves as a unifying framework: SSEM supplies the technical language and measurable attributes that support development practices to address security concerns, while the framework's emphasis on business alignment and clear expectations enables security teams to translate strategic objectives into actionable development requirements.

---

## 2. Foundational Principles

FIASSE is oriented by four core values. Framed in the spirit of the Agile Manifesto, each expresses a relative preference: both sides have worth, but when choices must be made, FIASSE favors the left.

- **Securable Attributes over Security Controls**: prefer the engineering qualities that let a system be built and kept defensible over external catalogs of controls evaluated against the system from outside the code creation process at a point in time.
- **Participation over Assessment**: prefer structured engagement between security and development throughout the lifecycle over evaluation performed after the work is done.
- **First Principle Alignment**: prefer grounding in established software engineering first principles over security-specific jargon or adversarial heuristics.
- **Business Alignment**: prefer security that sustains the organization's value creation over security pursued as an end in itself.

> **On Terminology: Controls, Features, and Attributes**
>
> The first value warrants a note on vocabulary, because the word "control" carries two distinct meanings that this framework keeps separate.
>
> In software engineering, "control" is an engineering concept (eg. control flow, version control, boundary control, control theory). In security and assurance vocabulary, "security control" is a risk-and-assurance concept: an administrative, technical, or physical measure cataloged so its presence and effectiveness can be evaluated, typically by parties external to the code creation process.
>
> Both meanings are legitimate in their own domain. FIASSE does not reject security controls as a concept; it locates them where they belong, which is in risk management, assurance, and external evaluation. It uses different vocabulary for the engineering work of building software. When discussing what developers build, FIASSE speaks of "Security Features" (specific capabilities such as Defendable Authentication; see Section 4.1.2), "Securable Attributes" (the SSEM qualities defined in Section 3.2), and Security "Acceptance Criteria" (testable conditions a feature must satisfy).
>
> The distinction matters because external security controls do not, on their own, make software secure. They measure and constrain; they do not construct. The qualities that make software defensible live in the code itself, and those qualities are what SSEM names. The first value is a statement about where engineering attention is best invested, not a dismissal of the assurance vocabulary that risk and audit functions correctly use.

The sections that follow develop these values as the foundational principles of FIASSE.

### 2.1. The Securable Paradigm: No Static Secure State

The term "securable" reflects a fundamental reality: there is no static state of "secure." A system declared secure today may be vulnerable tomorrow because of a newly discovered exploit, a dependency update, a configuration change, or a shift in the threat environment. Security is not a property a system permanently possesses; it is a capacity the system must be designed to sustain. The securable paradigm recognizes this and redirects the engineering goal accordingly: rather than asking "is it secure?", teams ask "is it built so that security can be maintained?"

Software exists in a continuously evolving threat landscape. New vulnerabilities emerge, attack vectors shift, business requirements change, and dependencies are updated. What is adequate today may be insufficient tomorrow. This reality requires a shift away from pursuing an illusory state of perfect security and toward building software with inherent qualities that allow it to adapt to and withstand evolving threats.

The securable paradigm emphasizes four organizing ideas:

- **Adaptive Resilience**: Software should be designed with the capability to respond to and recover from security events.
- **Evolutionary Security**: Security measures must evolve alongside the software and its operating environment.
- **Continuous Improvement**: Security is an iterative process that requires ongoing attention and refinement.
- **Business Alignment**: Security efforts must align with business objectives and risk tolerance, not pursue security as an end in itself.

Of these, **Business Alignment** is the value that governs the other three: adaptive resilience, evolutionary security, and continuous improvement are all judged by how well they sustain the organization's value creation, not by how much security activity they generate.

Development teams that internalize this paradigm build systems capable of maintaining their protective qualities as the system evolves, rather than becoming brittle and insecure over time.

Defendable Authentication is a direct application of this paradigm to a specific system mechanism. An authentication system evaluated as "secure" today may be inadequate tomorrow as credential attack techniques mature, MFA bypass methods emerge, or identity standards change. A system with Defendable Authentication is one whose architecture allows the team to sustain its integrity over time. The question shifts from "Is our authentication secure?" to "Is our authentication built so that security can be maintained?"

### 2.2. Resiliently Add Computing Value

In a business context, the primary directive of software engineering is to create valuable code that is robust enough to withstand change, stress, and attack. This directive is expressed concisely as: "Resiliently add computing value."

This means producing software that not only meets functional requirements but also possesses securable qualities, including Analyzability, Modifiability, and Testability, that allow it to sustain its integrity over time regardless of conditions. These qualities enable a codebase to accommodate evolving business needs while remaining resilient against threats.

Software Engineering is the broader discipline of designing, developing, and maintaining software in a systematic and organized way [ISO-24765]. Security is not a test appended at the end of this process; it is an intrinsic component of well-engineered software that contributes directly to a product's ability to deliver value reliably and sustainably.

### 2.3. Security Mission: Reducing Material Impact

The core mission of cybersecurity, as articulated by Rick Howard in "Cybersecurity First Principles," is to "reduce the probability of material impact of a cyber event" [Howard]. Complete elimination of breaches is not a practical business goal. Security strategies must therefore align with overarching business objectives through a balanced approach.

AppSec's role extends beyond formal buy-in and metrics: it encompasses enabling Development teams to meet security expectations and pass security assessments. This reduces the likelihood of a successful attack and limits potential damage when incidents occur.

### 2.4. Aligning Security with Development

A common misconception frames the gap between Security and Development as inherently problematic. The two disciplines are complementary, not adversarial: development adds value, and security works to reduce the risk of losing that value. The analogy to Accounting and Operations is apt: both serve the business from distinct vantage points without one disrupting the other's core function. Security should not need to disrupt the value-adding operation.

True alignment between security and development requires a return to first principles. This is the value of **First Principle Alignment**. Rather than imposing security-centric jargon and processes that may slow or interrupt development, FIASSE uses well-established software engineering terms to describe securable code attributes. The SSEM properties, including Analyzability, Modifiability, Testability, and Confidentiality, are concepts developers already work with. Using this shared vocabulary fosters understanding and empowers engineers to address security considerations with confidence, without requiring years of dedicated security experience.

This also requires that the expectation of mindset is calibrated correctly. The idea that all programmers should think like attackers or act as penetration testers to eliminate security problems overlooks a critical distinction: understanding how systems can be compromised is not the same as knowing how to build them to be secured. It is not reasonable for business value creation to be secondary to security. There is a significant difference between identifying a vulnerability and implementing a robust, scalable engineering solution to address it. Relying solely on an adversarial mindset does not scale.

Alignment requires specific participation from AppSec professionals early in the Software Development Lifecycle (SDLC), particularly during requirements gathering and feature planning. When security engages at those stages, developers gain the context and expectations they need to build securable software as a natural part of their workflow. This is the value of **Participation over Assessment**: shaping the system as it is being built is more effective than evaluating it after the fact, and it lets security expertise act where it produces the most leverage.

### 2.5. The Transparency Principle

Transparency is the principle of designing a system so that its internal state and behavior are observable and understandable to authorized parties. It is a foundational engineering strategy that underpins several core SSEM attributes, enabling trust and simplifying analysis. Transparency is about providing clear, contextualized visibility into how the system operates, makes decisions, and handles data.

Relying exclusively on external tooling for transparency produces a reactive posture. A system that is transparent by design, through structured logging, instrumentation, and clear audit trails, is easier to analyze, maintain, and secure from the outset.

Each SSEM attribute is demonstrated through transparency in some form. Note that transparency operates within the bound set by Confidentiality: visibility is extended only to authorized parties.

**Transparency and Maintainability**

A transparent system is easier to debug and understand. When developers can trace data flow, state changes, and decision logic through structured logs and metrics, they can diagnose deficiencies and assess the effects of changes with greater speed and accuracy. This directly supports the system's maintainability across its lifecycle.

**Transparency and Trustworthiness**

Transparency is the mechanism that makes Accountability possible. To uniquely trace an action to an entity, a clear, immutable, and auditable trail of that action must exist. Authenticity is similarly reinforced when authentication and authorization events are transparently logged, enabling verification and investigation. This verifiable behavior is the foundation of Trustworthiness.

**Transparency Tactics**

Engineering transparency into a system is an investment that benefits both security and operational stability. Practical tactics include:

- Write clear, well-documented code. Use meaningful naming conventions, precise data types, and comments that explain intent rather than just mechanics.
- Use version control (e.g., git) to provide an auditable history of modifications.
- Log events as structured data with rich context. Structured logs are machine-parsable and substantially more useful for analysis, monitoring, and alerting.
- For permission changes, data access, configuration updates, and other security-sensitive events, produce detailed and immutable audit trails. Capture the who, what, where, when, and why of each action. For example, a system that manages user roles should log the requesting administrator, the target user, the prior role, the new role, and a timestamp.
- Expose health and performance metrics through instrumentation. Key operational signals such as authentication failures, input handling error counts, and memory and CPU utilization provide real-time insight into system behavior through a standardized API.
- Log events at trust boundaries. Include the outcome of validation, sanitization, or transformation steps outside normal expectations. Debug-level logging of all boundary events is useful during development and incident analysis.

Transparency and the Principle of Least Astonishment (Section 2.6) work in concert: transparent systems tend to be astonishment-free because their operations are visible and understandable. Together, these properties reduce cognitive load on maintenance teams and increase the speed at which security concerns can be identified and addressed.

### 2.6. The Principle of Least Astonishment

The Principle of Least Astonishment (POLA) holds that systems should behave in ways that are intuitive and predictable to users, developers, and administrators. When a system diverges from reasonable expectations through unexpected behavior, hidden side effects, or unintuitive interfaces, it becomes harder to understand, reason about, and secure.

POLA is particularly relevant to securable software for four reasons:

- **Predictability aids analysis.** When code behaves as expected, developers can identify problems faster, making the system more Analyzable.
- **Reduced cognitive burden.** Unexpected behavior introduces complexity that developers must track mentally. Eliminating surprise reduces that burden and supports Modifiability.
- **Intuitive security boundaries.** Clear separation of concerns and trust boundaries makes it easier for developers to understand where security controls are needed and why.
- **Transparency complement.** POLA and Transparency reinforce each other: transparent systems are typically astonishment-free because their operations are visible and understandable.

In practice, POLA manifests as:

- Consistent naming and behavior across the codebase
- Functions and methods that do what their names indicate, without hidden side effects
- Clear, documented exceptions to expected behavior
- Predictable error handling and recovery mechanisms
- Interfaces that behave as users would naturally expect

Adhering to POLA during design and implementation produces systems that are more securable, maintainable, and trustworthy over time.

---

## 3. The Securable Software Engineering Model (SSEM)

### 3.1. Model Overview and Design Language

Section 2.4 established that true alignment between security and development requires shared vocabulary: security-centric jargon imposed on engineers creates friction, while terms already native to software engineering create common ground. SSEM is the practical expression of that principle. It provides a design language built from established software engineering terms to define the attributes that make software securable (see Section 2.1). Where Section 2.4 identifies the need and Section 2.1 explains why securability matters as a concept, SSEM makes both operational: each attribute is something a team can define goals for, measure against, and improve incrementally. By grounding security attributes in familiar engineering vocabulary, SSEM allows software engineers to integrate security considerations as a natural part of their development work, and enables security professionals to evaluate how existing code meets security expectations and where improvement is warranted.

The central shift SSEM enables is a change in the question asked during security assessment. Rather than a binary "Is it secure?" evaluation, the focus becomes: "Do we meet our defined goals for this particular securable attribute?" This framing is actionable, measurable, and compatible with iterative development.

SSEM is designed to:

- Account for the iterative nature of software development and agile methodologies.
- Serve as a mental model, a checklist, or a vehicle for expressing and setting clear expectations for securable design.
- Shift conversations away from find-and-fix monotony toward cohesive, intention-driven creation of software with inherent securable qualities.

This is the value of **Securable Attributes over Security Controls** made operational. Rather than enumerating controls for auditors to verify at a point in time, SSEM defines the engineering qualities that allow a system to be secured, measured, and improved as it evolves.

The attributes are organized into three primary categories:

| **Maintainability** | **Trustworthiness** | **Reliability** |
|:--------------------|:-------------------:|----------------:|
| Analyzability       | Confidentiality     | Availability    |
| Modifiability       | Accountability      | Integrity       |
| Testability         | Authenticity        | Resilience      |
| Observability       |                     |                 |

SSEM is not a rigid framework. It is a flexible model that adapts to various software engineering practices and emphasizes inherent qualities of software that contribute directly to security. This allows it to scale without requiring security to adopt complex processes that may conflict with development workflows.

By defining these attributes in engineering terms, SSEM creates a common design language. It equips security professionals to surface context-specific considerations, and it provides developers with the conceptual tools to discuss and reason about security using vocabulary already familiar to them. A shared design language can bring together a culture of quality across diversely skilled teams, focused on common goals rather than isolated compliance checkboxes. This cultural alignment directly influences a product's internal structure to reflect these technical values.

### 3.2. Core Securable Attributes

The following attributes are the building blocks of securable software. They are not abstract concepts; each represents a tangible characteristic that contributes directly to a system's overall security and resilience. By building toward these attributes, developers proactively construct systems that are easier to secure and protect as the threat landscape evolves.

#### 3.2.1. Maintainability

**Definition:** "The degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers" [ISO-25010]. In the context of SSEM, Maintainability means software can be evolved, corrected, and adapted to new threats or requirements without undue effort or the introduction of new vulnerabilities. This focus on ease of modification is central to securable software, as it directly supports the ability to respond to the dynamic threat landscape described in Section 2.1.

##### 3.2.1.1. Analyzability

**Definition:** "The degree of effectiveness and efficiency with which it is possible to assess the impact on a product or system of an intended change to one or more of its parts, or to diagnose a product for deficiencies or causes of failures, or to identify parts to be modified" [ISO-25010, §4.2.7.3]. In practical terms, Analyzability is the ability to locate the cause of a behavior within the code. Code must be understandable to find and fix vulnerabilities; Analyzability directly determines the speed and accuracy of vulnerability remediation.

Contributing factors:

- **Volume (Lines of Code):** Overall size of the codebase.
- **Duplication:** Percentage of duplicated code.
- **Unit Size**(e.g., method Lines of Code / class Lines of Code): Lines of code per class, method, or block.
- **Unit Complexity (e.g., Cyclomatic Complexity):** Degree of complexity within a code unit.
- **Component Balance:** Distribution and size uniformity of top-level components.

##### 3.2.1.2. Modifiability

**Definition:** "The degree to which a product or system can be effectively and efficiently modified without introducing defects or degrading existing product quality" [ISO-25010, §4.2.7.4]. Modifiability is the ability to change code without breaking existing functionality or introducing new vulnerabilities.

Contributing factors:

- **Duplication:** Duplicated code increases the risk of inconsistent changes.
- **Unit Complexity:** Complex units are harder to modify safely.
- **Module Coupling:** The number of incoming dependencies for modules; high coupling can produce cascading changes and unintended consequences.

Modifiability is particularly important for security because it enables rapid response to newly discovered vulnerabilities or changing security requirements without extensive rework.

##### 3.2.1.3. Testability

**Definition:** "The degree of effectiveness and efficiency with which test criteria can be established for a system, product or component and tests can be performed to determine whether those criteria have been met" [ISO-25010, §4.2.7.5]. Testability is the ability to write a test for a piece of code without modifying the code under test.

Contributing factors:

- **Volume:** Larger codebases are more challenging to test comprehensively.
- **Unit Complexity:** Complex units are more difficult to test thoroughly.
- **Component Independence:** The percentage of code in modules with no incoming dependencies from other top-level components; higher independence facilitates isolated testing.
- **Unit Coupling:** High coupling complicates testing by introducing dependencies that must also be exercised.

Testability enables teams to verify that security controls function as intended and that changes do not introduce new vulnerabilities. It also supports automated testing that runs continuously, directly scaling the reach of security assurance.

##### 3.2.1.4. Observability

Observability is the degree to which the internal state of a system can be inferred from its external outputs. The concept originates in Kálmán's 1960 control theory formalization [Kalman1960] and has been adapted in software engineering to encompass runtime signals. Observability is essential for security: it allows developers and security professionals to understand how the system behaves in real time, and it ensures that users and operators can comprehend the system's state and actions.

Implementing Observability involves:

- Comprehensive logging
- Monitoring
- Instrumentation
- User interface (UI) feedback mechanisms

These mechanisms provide visibility into system operations and enable proactive identification of and response to real security issues.

Observability must be achieved through instrumentation and auditing built into the code itself rather than through external tooling alone. Tooling can surface signals, but it can only surface what the code exposes. A system that is not instrumented at the code level is opaque by construction, and no amount of external scanning compensates for that. Each SSEM attribute is demonstrable through observable behavior in some form: Analyzability through structured logs that make state and data flow traceable, Accountability through immutable audit trails, Authenticity through logged authentication events, and Resilience through error and recovery telemetry.

#### 3.2.2. Trustworthiness

**Definition:** "Ability to meet stakeholder expectations in a verifiable way" [ISO-27000]. A trustworthy system operates within defined levels of trust and meets specified security properties in a manner that can be demonstrated rather than assumed. Rather than focusing on overlaid security controls, FIASSE emphasizes the inherent code qualities that enable trustworthiness: strong architectural design, clear trust boundaries, and well-defined areas of flexibility.

Key attributes contributing to trustworthiness include:

##### 3.2.2.1. Confidentiality

**Definition:** "Property that information is not made available or disclosed to unauthorized individuals, entities, or processes" [ISO-27000, §3.10]. Confidentiality ensures that sensitive information is protected from unauthorized access, whether that information is at rest, in transit, or in active use within the system.

FIASSE treats Confidentiality as an attribute achieved through the construction of software with inherent protective qualities, rather than through overlaid controls alone.

##### 3.2.2.2. Accountability

**Definition:** The property that every action taken within a system can be attributed to a specific, identified entity. Accountability involves managing principals and access rights in a way that enables attribution of actions to specific users or processes. This attribution is essential for auditing and incident response.

Achieving Accountability requires robust methods for managing principals and their access rights. While it draws on strategies common to non-repudiation, including comprehensive logging and defendable authentication, its core focus is the unique and verifiable attribution of every system action to a specific entity.

##### 3.2.2.3. Authenticity

**Definition:** "The property that an entity is what it claims to be" [ISO-27000]. Authenticity ensures that users, systems, or information are genuine and verifiable. It is strongly supported by non-repudiation: "the ability to prove the occurrence of a claimed event or action and its originating entities" [ISO-27000], which prevents entities from falsely denying having performed an action or sent a message.

> **On Terminology: Defendable Authentication**
>
> This framework uses the term *Defendable Authentication* in place of the commonly used phrase "secure authentication." The distinction follows directly from the securable paradigm (Section 2.1): "secure authentication" frames building authentication as a feature with a single linear function. *Defendable Authentication* describes a feature whose design makes defense sustainable.

Implementing Authenticity involves:

- Defendable authentication methods (e.g., token hygiene, threat tracking, attack pattern recognition, circumvention response).
- Digital signatures and certificates to verify the origin and integrity of data and communications.
- Comprehensive logging and auditing to trace actions back to their origin.

These mechanisms provide assurance that entities are genuine and accountable for their actions. They also support transparency and simplify maintenance and troubleshooting of the system.

#### 3.2.3. Reliability

**Definition:** "The degree to which a system, product or component performs specified functions under specified conditions for a specified period of time" [ISO-25010]. In SSEM, Reliability means software operates consistently and predictably, even under adverse conditions or when facing unexpected inputs or attacks.

##### 3.2.3.1. Availability

**Definition:** "Property of being accessible and usable on demand by an authorized entity" [ISO-27000, §3.7]. Availability also includes maintaining this performance during periods of adverse circumstances.

For security, Availability means the system is designed to resist attacks like Distributed Denial of Service (DDoS) and to recover quickly from failures or disruptions, ensuring it remains accessible to authorized users.

##### 3.2.3.2. Integrity

**Definition:** "Property of accuracy and completeness" [ISO-27000, §3.36]. In SSEM, Integrity applies at two levels. **System integrity** is the property that the system performs its intended function in an unimpaired manner, free from unauthorized manipulation of its code, configuration, or runtime behavior. **Data integrity** is the property that data has not been changed, destroyed, or lost through unauthorized action, accidental modification, or transmission error.

Implementing Integrity involves measures such as cryptographic hashing, checksums, and access controls to prevent unauthorized modification or corruption. Emphasizing Integrity at a fundamental level ensures that trust in the system extends to all its components, not just isolated parts. Integrity encompasses more than preventing unauthorized changes; it also ensures the system operates correctly and consistently in the face of potential threats or failures.

##### 3.2.3.3. Resilience

**Definition:** The ability of a system to continue operating during and after the failure of one or more of its parts, and to recover from that failure and restore full operations. Resilience also encompasses an application's ability to continue running predictably under unfavorable circumstances or load (as discussed in Section 4.4).

Resilience includes fault tolerance: the ability of a system to continue operating correctly even when a component has failed. Achieving Resilience means fault tolerance is designed into the system as a whole, not bolted onto specific features. The system handles errors gracefully, recovers from failures, and maintains functionality even when components are compromised or unavailable.

Strategies for building resilient systems include:

- **Defensive coding:** Writing code that anticipates input outside expected bounds and handles it without failing.
- **Predictable execution:** Ensuring code behaves consistently under varied conditions.
- **Strong trust boundaries:** Clearly defining areas of the codebase that enforce strictly controlled execution.
- **Robust error handling:** Implementing recovery mechanisms that manage partial failures effectively.

---

## 4. Practical Guidance for Securable Software Development

### 4.1. Establishing Clear Expectations

Clear expectations are foundational to building securable products. AppSec maximizes its impact by setting those expectations early and in terms that integrate naturally into development workflows. This requires alignment with the business processes involved in producing software.

#### 4.1.1. Proactive Communication

Development teams should be informed about new testing initiatives or security programs pertaining to the products they maintain. Demonstrating tools to interested engineers fosters collaboration and surfaces key contacts for ongoing partnership. Regular synchronization points provide support and maintain momentum. Effective communication is a functional prerequisite for AppSec professionals operating in this capacity.

#### 4.1.2. Integrating Security into Requirements

Active AppSec participation in formal requirements gathering moves security from a post-development review to an integral component of the product, aligning it with productivity rather than positioning it as a gate.

Key deliverables include:

- **Security Features:** Specific security capabilities that must be implemented, such as Defendable Authentication mechanisms, encryption requirements, or access controls.
- **Threat Scenarios:** Descriptions of potential misuse cases or attack paths relevant to the feature being developed, used to identify necessary controls.
- **Security Acceptance Criteria:** Specific, testable conditions a feature must satisfy to be considered secure. These criteria allow QA to perform security testing by verifying requirements. Implementation completeness against defined acceptance criteria is a measurable security outcome: a feature that satisfies all its security criteria provides a verifiable basis for confidence that is absent when criteria were never defined.

Embedding security into foundational design decisions through requirements makes attributes like Trustworthiness, Integrity, and Resilience more reliably realized. Development teams can address security concerns as part of their standard workflow, making requirements an often underutilized but powerful tool for security.

Incomplete requirements are a root cause of security gaps. When security expectations are absent from the requirements that developers work from, the resulting implementation is not deficient by error; it is deficient by design. The gap exists not because developers failed to secure the code, but because no one specified what secure looked like for that feature.

### 4.2. Threat Modeling

This section addresses two related but distinct activities: **Threat Modeling**, a formal structured analysis conducted at the system or feature level; and **Threat Awareness**, a continuous, lightweight practice applied at the code level. They serve different purposes and operate at different scopes. Conflating them risks overstating informal inquiry or, more commonly, creating the impression that a formal exercise has already been done when it has not.

**Threat Modeling** is conducted against a defined methodology, involves a cross-functional group of participants, and produces documented outputs. A complete threat modeling exercise produces a threat model: a recorded analysis of what the system is built to do, what assets it protects, what adversaries and attack paths are relevant, and what controls or design decisions address each identified threat. Methodologies such as STRIDE [STRIDE], PASTA [PASTA], and LINDDUN [LINDDUN] provide systematic frameworks for this analysis. The outputs feed directly into security requirements, architecture decisions, and acceptance criteria. Threat modeling requires dedicated time, the right participants (typically a developer, an architect, and a security professional), and a scope bounded enough to be tractable. It is most effective at the architecture and feature design stage, before implementation begins.

**Threat Awareness** is the lightweight, continuous practice of asking "What can go wrong?" at the code level, without the formality, scope, or methodology of threat modeling. It requires no formal process and is valuable precisely because it is immediate and incremental. The Four Question Framework [TM-Manifesto] (*What are we building? What can go wrong? What are we going to do about it? Did we do a good job?*) supports this practice. Threat awareness complements formal threat modeling; it does not substitute for it. Findings that reveal design-level concerns should be escalated into the formal threat model. A team relying on threat awareness alone will catch code-level issues but miss the design-level threats that only a scoped, methodical analysis can surface.

#### 4.2.1. Code-Level Threat Awareness

Asking "What can go wrong?" at the code level helps identify potential issues before they reach production. When practiced in pairs or small teams, it also helps junior engineers develop judgment about code quality. Practical contexts for code-level threat awareness include:

- **Merge Reviews:** Reviewing an entire codebase is not practical because the code continues to change. Scoping a review to the changeset of a merge provides clear context and responsibility. Earlier is less costly, and merge reviews make earlier the default.
- **Static Analysis:** Reviewing static analysis results, particularly when scoped to a merge request, with the intent of going deeper using the Four Question Framework can surface impact that automated tools alone would not flag.
- **Pair Programming:** Pair programming facilitates knowledge sharing, helps prevent security issues early, and builds comfort with the "What can go wrong?" question.

Code-level threat findings should feed back into the broader Threat Model so that threats can be assessed from a design perspective. This can surface design-level solutions that are more maintainable and scale better than localized fixes.

#### 4.2.2. Threat Modeling Solution Framework

Threats follow data. Understanding how data flows through a system is central to identifying potential vulnerabilities. Mapping data flows allows developers to pinpoint where sensitive information is handled and where it may be exposed to threats. Frameworks like STRIDE [STRIDE] are useful because they provide structure and direct attention toward categories of attack.

When addressing the question "What are we going to do about it?", the default is sometimes to state the problem in inverse language or to reach for a security control. SSEM provides a more structured alternative. Considering the SSEM attributes, particularly Trustworthiness and Reliability, can lead to existing architectural or logical solutions that address a threat more holistically. Further, when it becomes clear that a threat cannot be addressed through an inherent system attribute, that recognition defines a requirement: the gap must be addressed through explicit security requirements.

### 4.3. The Boundary Control Principle

> Control in this section refers to its software-engineering sense: the regulated handling of data and execution flow at a trust boundary, not a "security control" in the risk-and-assurance sense addressed in Section 3.1.

The Boundary Control Principle holds that flexibility within a system's interior is an engineering asset to be preserved, while control at every trust boundary is a security requirement to be enforced. These objectives are complementary, not competing: uncontrolled flexibility at a trust boundary is an attack surface; controlled flexibility throughout the interior is what makes a system maintainable. The principle directs engineers to locate control precisely at the points where trust changes, and to preserve flexibility everywhere else.

A key concept from threat modeling is the identification of trust boundaries: points in the system where data passes between entities with different levels of trust (user to application, application to database, service to service). Trust boundaries require heightened control over data and process execution.

Software engineers value flexibility in code because it facilitates feature implementation and bug fixing. Attackers seek uncontrolled flexibility as a means to force the application to deviate from intended behavior. The issue is not flexibility itself, but the exposure of flexibility through insufficient handling of trust boundaries. An example of uncontrolled flexibility is a function that executes arbitrary query statements with arbitrary bind parameters without restriction. Control is what ensures trustworthy execution, maintains system Integrity, and supports Resilience. Flexibility supports Maintainability. Both are necessary, and neither should come at the expense of the other.

To enhance security, minimize what is trusted and harden trust boundaries. Think of trust boundaries as the hard shell of a turtle: the flexible interior represents the bulk of the application's logic, while the shell represents the critical points where external data and untrusted operations are carefully controlled. Defining and communicating these boundaries during the design phase clarifies which areas of code are responsible for tight control, allowing developers to focus their efforts on maintaining the Integrity and Trustworthiness of those critical interfaces. Data Flow Diagrams are a practical tool for identifying these boundaries.

One approach to maintaining flexibility while preserving control is strict input handling at trust boundaries, producing canonical values. The boundary entry point adapts input handling to the context from which a value is arriving. This allows developers to work flexibly within the system while knowing that unexpected input cannot propagate uncontrolled into core logic. Section 4.4.1 covers this in detail.

### 4.4. Resilient Coding

Resilience refers to an application's ability to continue running predictably, even under unfavorable circumstances or load. At the code level, this is achieved through defensive coding practices that enforce predictable execution.

Practical defensive coding focuses on:

- **Strong typing:** Ensuring data is usable in the intended way.
- **Input validation at trust boundaries:** Confirming data conforms to expected formats, types, lengths, and ranges before processing.
- **Output encoding:** Properly escaping and encoding all output destined for other systems or interpreters, preventing injection attacks by ensuring data is treated as data rather than executable instructions.
- **Null value handling:** Sandboxing null values to input checks and database communication; using exceptions to handle exceptional cases rather than propagating null through business logic.
- **Comprehensive error handling:** Managing unexpected conditions gracefully rather than allowing the application to crash or behave unpredictably.
- **Immutable data structures for concurrent programming:** Preventing insecure modification and ensuring thread safety.
- **Avoidance and isolation of risky operations:** Certain programming constructs introduce disproportionate risk and should be avoided where alternatives exist. String concatenation used to construct queries or commands, deserialization of untrusted data, and dynamic execution constructs such as `eval()` are common examples. Where such operations cannot be avoided, they must be encapsulated behind a well-defined, narrow interface and isolated from the rest of the application so that their risk surface is bounded and their behavior is auditable.
- **Safe memory and resource management:** Acquiring resources explicitly and releasing them reliably, regardless of execution path. This includes file handles, database connections, network sockets, and allocated memory. Failing to release resources introduces availability risk and, in some environments, exploitable memory conditions. Use language-provided constructs (such as `try-with-resources`, `using` blocks, or RAII patterns) to ensure deterministic cleanup. Avoid holding resources longer than necessary, and prefer scoped allocation where the language supports it.
- **Graceful and secure failure:** When a component encounters an error it cannot recover from, it must fail in a way that is safe, not just visible. Graceful failure means the application transitions to a known, controlled state rather than an undefined one. Secure failure means the error path does not leak internal state, stack traces, or implementation details to untrusted parties. Error messages presented externally should be generic; detailed diagnostic information should be captured in internal logs only. A failure that exposes system internals to an attacker is not graceful, regardless of how cleanly the exception is caught.
- **Least privilege operation at the code level:** Code should request and hold only the permissions it needs for the specific operation it is performing, and for no longer than that operation requires. This applies to database access (request read access when write is not needed), filesystem operations (scope access to the specific path required), API calls (request only the scopes the operation requires), and thread or process privileges (drop elevated permissions as soon as they are no longer needed). Least privilege at the code level limits the blast radius of a compromised component and reduces the set of actions an attacker can take if they gain control of execution within that component.

These are verifiable items that AppSec can assess during review.

#### 4.4.1. Canonical Input Handling

Input handling is a critical aspect of resilient coding. The most effective approach applies a minimal acceptable range for each parameter at the point of input through three practices:

- **Canonicalization/Normalization:** Ensures input data conforms to expected formats, types, lengths, and ranges before processing, preventing unexpected or malicious data from entering the system.
- **Validation:** Confirms input data meets specific criteria before processing. Prefer allowing only explicit, known-good values rather than attempting to reject unexpected values.
- **Sanitization:** Removes or neutralizes potentially harmful content, preventing malicious data from being executed or interpreted as code.

In some platforms, it may be beneficial to signal that an input value has been fully handled by passing it as a contextualized object rather than a scalar value after validation. If this pattern is used, document and communicate it to the team.

##### 4.4.1.1. The Request Surface Minimization Principle

One tactic for resilient input handling is to avoid assuming that the entire request or envelope is intended to be processed. This encourages developers to access specific named values within a request rather than processing all values indiscriminately. This approach has allowed developers to avoid certain categories of injection attack and is a sound sanitization tactic generally. It also preserves resilience by ignoring out-of-scope values rather than attempting to handle them.

A security benefit of this approach is that the system can analyze requests for payload anomalies, fraud indicators, or probing behavior without disrupting normal application operation. Because the application only processes the values it expects, unexpected fields or values are observable as deviations rather than noise embedded in processing logic.

Requests that deviate from expectation should be logged at minimum. The log entry should capture enough context to be useful in retrospect: the specific deviation observed, the request source, a timestamp, and any relevant session or user identity. A bare count or a generic "unexpected input" message does not support meaningful analysis.

In sensitive contexts, log-and-reject is the more defensible posture, and in some cases the correct one. The reasons to prefer rejection over silent discard are:

- **Reconnaissance detection.** Unexpected fields are frequently a sign that a client is probing the API surface: testing parameter names, injecting out-of-band values, or mapping the system's behavior. Rejecting the request raises the cost of this activity and makes the behavior more visible in logs.
- **Manipulation prevention.** In business-critical flows, an unexpected field may represent an attempt to supply a value the server should be deriving (see Section 4.4.1.2). Silently ignoring it allows the request to succeed, which confirms to the attacker that the attempt went unnoticed. Rejection removes that confirmation.
- **Defense against future code changes.** A value ignored today may be processed tomorrow if the codebase changes. Rejection is a documented, enforced boundary. Silent discard is a convention that can erode without notice.
- **Compliance and audit requirements.** In regulated environments, accepting and processing requests that contain anomalous input may create audit exposure even when no immediate harm results. Rejection produces a clear, defensible record of the boundary being enforced.

The choice between log-only and log-and-reject should be made deliberately, based on the sensitivity of the context and the risk profile of the deviation. It should not be left as an implicit default.

##### 4.4.1.2. The Derived Integrity Principle

Any value critical to the integrity of a system's state or business logic must be derived or calculated in a trusted context. It must never be accepted directly from a client. This establishes a single source of truth for what is real and authoritative, rather than adopting the unknown integrity of client-supplied data.

Consider the analogy: a customer should not walk into a store, pick up an item, and tell the cashier how much it costs. The price is non-negotiable; it is derived from the store's own trusted system. The same logic applies to software. The client's role is to express intent (e.g., "I want to purchase item X"), not to dictate the facts of the transaction (e.g., "and it costs $0.01").

Applying this principle prevents entire classes of vulnerabilities related to business logic manipulation. Good candidates include:

- **Pricing and totals:** The final cost of items in a shopping cart must be calculated server-side from product IDs and quantities, referencing a secure price database.
- **User permissions:** A user's role or permission level must be loaded from a server-side session or database, not passed in a client request.
- **Object state:** The status of an order (e.g., "shipped," "paid") must be managed by an internal state machine, not accepted as a parameter from the client.

For example, when a user initiates checkout through a shopping API, the client might send:

```json
{
  "action": "checkout",
  "items": [
    {
      "itemId": "12345",
      "quantity": 2,
      "price": 5.97
    }
  ]
}
```

A server applying the Derived Integrity Principle accepts only the client's intent, specifically to check out with the specified items at the specified quantities, and discards the client-supplied price entirely. It derives the actual price from its own inventory. It may log or reject the request outright for including a price field. The client expresses intent; the server enforces integrity.

A more advanced application of this principle involves JWTs (JSON Web Tokens). If a server accepts any algorithm specified in the JWT header for signature verification, it allows the client to dictate how the token's integrity is established, which is a direct violation of the principle.

The Derived Integrity Principle is a direct application of the SSEM attribute of Integrity (Section 3.2.3.2): it ensures the system performs its intended function in an unimpaired manner, free from the manipulation that client-supplied data could otherwise introduce.

### 4.5. Dependency Management

Dependency management begins before a library is introduced to the system. Each candidate dependency should be evaluated for fit with the system and its security values. This reflects the FIASSE mindset: understanding the implications of dependencies on the securable posture of the system is part of the engineering discipline, not an afterthought.

Applying SSEM principles to dependency selection and management, going beyond scanning for known CVEs, involves considering:

- **Analyzability:** Understand each dependency's full scope, including transitive dependencies, its specific purpose within the application, and its potential attack surface. Maintain a clear inventory and a documented rationale for every included dependency.
- **Modifiability:** Design systems with loosely coupled dependencies to facilitate updates, patching, or replacement if a vulnerability is discovered, a dependency becomes obsolete, or a more secure alternative is identified.
- **Testability:** Ensure dependencies can be effectively managed during testing through mocking, stubbing, or version pinning, and that their integration points are robustly testable.
- **Trustworthiness (Authenticity and Integrity):** Verify the source and integrity of dependencies using signed packages, checksums, and trusted repositories before integrating them into the codebase.
- **Reliability:** Assess how a dependency's failure modes, including unavailability, performance degradation, and security compromise, could affect the overall system's reliability and resilience, and plan appropriate mitigations.

Not all shared code is designed for use in systems that require resilience. Once FIASSE has been adopted, candidate dependencies can be evaluated against the values the culture aims to establish, ensuring alignment with these SSEM attributes.

Additional considerations:

- Avoid unnecessary dependencies. Each one introduces ongoing maintenance requirements.
- If no direct update resolves a known flaw, further analysis is required: compensating controls, forking and patching, or re-implementation are all candidates.
- Organizations should maintain a clear policy for the use and maintenance of open-source dependencies, including processes for addressing vulnerabilities found within them.
- Relying solely on CVE (Common Vulnerabilities and Exposures) databases is insufficient. Analyze dependencies and their transitive dependencies directly.
- Regularly updating dependencies is a fundamental maintenance tactic. Updates often include fixes for known bugs, including security vulnerabilities, and should be integrated into sprints or regular maintenance cycles.

### 4.6. Dependency Stewardship

**Dependency Stewardship:** The ongoing application of SSEM attributes to the selection, integration, monitoring, and lifecycle management of third-party dependencies, with the goal of maintaining the securable posture of the system independent of supply chain attestation mechanisms.

Where dependency management addresses the mechanics of selecting, evaluating, and updating third-party code, dependency stewardship is the governing practice that treats the ongoing relationship with that code as a securable attribute of the product itself.

The distinction matters because a dependency that passes an initial evaluation may become a liability over time. Maintainers may abandon the project, the codebase may stagnate, security issues may go unaddressed, or the project's direction may diverge from the system's needs. Stewardship asks not only "is this dependency acceptable today?" but: "Would this dependency be a responsible, maintainable, and trustworthy part of this system, now and over time?"

Framing stewardship through SSEM attributes makes the question concrete and consistent with the broader engineering practice:

- **Analyzability:** Can your team understand what this dependency does, why it is included, and what it touches in your system? A dependency whose behavior is opaque, whose scope has grown beyond its original purpose, or whose transitive dependencies are undocumented is an analyzability liability. Stewardship means keeping the inventory honest and the rationale current.
- **Modifiability:** Can the dependency be updated, replaced, or removed without cascading disruption? A tightly coupled dependency that is difficult to swap out creates risk when a vulnerability is discovered or a better alternative emerges. Stewardship means preserving the ability to act when circumstances change.
- **Testability:** Can the dependency be isolated, mocked, or version-pinned reliably across the system's test suite over time? Dependencies that resist clean isolation accumulate testing debt and reduce the team's confidence in security-relevant test coverage.
- **Authenticity and Integrity:** Does the dependency continue to demonstrate trustworthy maintenance behavior over time? This includes consistent release practices, signed packages, responsive handling of reported vulnerabilities, and a maintainer community that is active and accountable. A dependency that was trustworthy at introduction may not remain so.
- **Resilience:** What happens to your system if this dependency is abandoned, compromised, or becomes unavailable? Stewardship requires thinking through failure modes at the system level: are there fallback strategies, can the functionality be re-implemented if needed, and is the dependency's health monitored as part of routine operations?

Stewardship is not a one-time evaluation. It is a recurring responsibility that belongs on the agenda of sprint planning, architecture reviews, and merge reviews, not as a separate activity, but as a standing lens applied to the work already being reviewed. When a dependency is introduced, the team takes on a relationship with that code and its maintainers. That relationship warrants the same ongoing attention given to any other securable quality of the product.

---

## 5. Integrating Security into Development Processes

### 5.1. Natively Extending Development Processes

A key principle for reducing friction and preparing development teams effectively is to integrate security into existing workflows rather than imposing separate, external security gates. This requires understanding current practices and extending them with purpose.

Security teams often occupy a reviewer position. While assurance activities matter, earlier engagement in requirements gathering, architecture, and design is more impactful and avoids positioning security as an adversary to the teams it needs to collaborate with. Security positioned as a partner is better informed and better placed to provide value.

Security teams carry responsibilities beyond assurance and development partnership, including maintaining defensive infrastructure, operating detection tooling, and coordinating incident response. These functions run continuously and independently of the development lifecycle. When software is built to the standard FIASSE describes, it reduces the burden on all three: fewer exploitable surfaces produce fewer incidents to detect and contain. These parallel responsibilities do not contradict FIASSE's integration model; they are the functions that benefit most directly when the software being defended is built to a securable standard.

Beyond the reviewer role, security can offer strategic extensions to development activities:

- **Architecture:** Incorporate security implications into architectural considerations. For example, throttling and DDoS protection help preserve business integrity.
- **Predefined checklists:** Develop flexible checklists that incorporate SSEM attributes and security considerations applicable across different contexts.
- **Usability:** Frame usability not just as aesthetics but as a foundation for trust. Clear error messages, intuitive permissions management, and predictable interface behavior all contribute to a more secure user experience.

### 5.2. The Role of Merge Reviews

While software engineering lacks the formal mentorship structures of some other engineering disciplines, the merge review (or pull request review) serves as a critical point for guidance, validation, and knowledge transfer. For security, this is where securable code review can scale effectively. It functions as an agile training ground where developers learn from peers in a constructive environment. SSEM attributes provide a concrete and shared basis for these reviews.

Teams should treat merge reviews as guardrails, not gates. The goal is to grow the FIASSE mindset within the team and to make the review process a positive experience for developers, without introducing unnecessary friction or delay.

Code review through merge requests is an effective technique for identifying security vulnerabilities early in the development process [OWASP-CRG]. Automated scans can surface known or common issues, but they cannot interpret the context of a change or understand the architecture of the system. Human review brings that context to bear.

The collaborative nature of merge reviews allows for the sharing of insight and expertise, and provides a fresh perspective that individual developers may lose through familiarity with their own code. When FIASSE-trained security professionals participate, they contribute insights that over time elevate the broader team's understanding of SSEM attributes and their implications.

Merge reviews are also an appropriate venue for practicing threat awareness at the code level: asking "What can go wrong?" within the bounded scope of a changeset makes it easier to identify risks and vulnerabilities that might be harder to isolate in a larger system review. Findings that reveal design-level concerns should be escalated into the formal threat model rather than addressed solely as code-level fixes.

### 5.3. Early Integration: Planning and Requirements

FIASSE advocates for integrating security at the earliest stages of development, particularly during planning and requirements definition. This ensures security is a foundational design element rather than a retrofit. Addressing vulnerabilities at the design phase costs a fraction of what it costs to address them in production [Boehm1981].

The primary mechanism for early integration is active security team participation in requirements gathering, as described in Section 4.1.2. By contributing Security Features, Threat Scenarios, and Security Acceptance Criteria to the requirements process, the security team ensures that security expectations are explicit, testable, and integrated into the development workflow from the start.

---

## 6. Common AppSec Anti-Patterns

### 6.1. The Control-Catalog Fallacy

Treating the external control catalog as the definition of secure software is a fallacy this framework aims to correct. Control catalogs (like NIST 800-53, ISO 27001 Annex A, PCI DSS, and their equivalents) support risk management, assurance, and external evaluation. They articulate what protections must exist within a system. However, they do not, by themselves, construct those protections. Software does not become defensible simply because a catalog has been satisfied. But when controls are recognized as input that informs security requirements, engineering translates them into features, and the two functions operate in harmony.

The fallacy occurs when this translation pathway is collapsed, when "is this software secure?" is answered by listing controls rather than examining features that fulfill corresponding requirements. This collapse causes friction between security and engineering teams. When controls are seen as engineering output, engineering is positioned as the party that must comply. Conversely, when controls are recognized as input that informs security requirements, engineering translates them into features, and the two functions operate in harmony. 

The collapse produces systems that pass audits but fail under sustained attack, because audits measure the wrong object. It also produces development teams who see security as external demands rather than a property of their work. This is when "Shoveling Left" (Section 6.2) takes hold.

The corrective discipline is the first FIASSE value (Section 2). Engineering attention belongs on qualities that make features complete and software defensible. Control catalogs belong in assurance and risk functions that evaluate from outside the code creation process. The relationship between them is a translation, not a transfer of authority. Mistaking one for the other is the fallacy.

### 6.2. The "Shoveling Left" Phenomenon

"Shoveling Left" is the practice of supplying impractical information to developers and leaving the responsibility on them to make sense of it. This anti-pattern manifests in how vulnerabilities are reported, how training is conducted, and how testing results are delivered. It undermines AppSec's credibility and leads to developer disengagement.

The corrective discipline is the **Actionable Security Intelligence Principle**: security teams collaborate with development teams on systemic flaw reductions by producing findings, guidance, and training in a form developers can act on within their normal engineering workflow. Raw tool output, exploit-centric narratives, and unfiltered vulnerability lists are information, not yet intelligence. The principle holds that security output becomes valuable only once it has been translated into prioritized, engineering-grounded direction calibrated to the developer's context. Shoveling Left is the direct inversion of this principle, and the sub-sections that follow examine two of its most common forms.

#### 6.2.1. Ineffective Vulnerability Reporting

A prime example of "Shoveling Left" is routing raw output from security scanning tools directly into the development team's backlog without context, prioritization, or actionable guidance. While initial progress may follow, momentum typically dissipates and issues tend to recur in a "whack-a-mole" pattern. Raw tool output alone is rarely sufficient to drive sustained improvement.

To avoid this pattern, AppSec should:

1. **Focus on true positives:** Validate findings to confirm accuracy before routing them to development.
2. **Analyze trends and pooling patterns:** Look across multiple findings and tools to identify systemic issues rather than isolated incidents.
3. **Identify root causes:** Address underlying structural problems rather than symptoms.
4. **Prioritize by impact:** Focus on issues that are widespread or affect sensitive resources.
5. **Collaborate on solutions:** Work with development to identify wide-impact engineering solutions rather than line-level mitigations.
6. **Verify fixes:** Confirm that remediation is effective, and consider automated regression tests to prevent recurrence.

#### 6.2.2. Pitfalls of Exploit-First Training

Security training for developers that primarily emphasizes exploitation techniques, often framed as "learn the hack to stop the attack," is another form of "Shoveling Left." As Section 2.4 establishes, understanding how to compromise a system is not the same as knowing how to engineer a robust one. The hacker mindset and the engineer mindset are complementary disciplines, not interchangeable ones.

This type of training is ineffective because it does not equip developers with the engineering principles needed for daily work. It also fails to provide the knowledge needed to identify or build code with inherently securable qualities as defined by SSEM. At best, developers gain a superficial understanding of risks without the practical knowledge to implement systemic preventative measures. This can produce a false sense of security and does little to foster the proactive, engineering-focused examination of "What can go wrong?" The goal is better design and implementation, not line-level mitigations applied after the fact.

### 6.3. Strategic Use of Security Output

Scanning and testing tools are valuable for understanding current security posture, but their output must be used strategically. It should not be assumed that security requirements are implicit, or that developers can be held responsible for missing controls if clear expectations were never set. Productive software engineers operate within a structured workflow designed to deliver value. Disrupting that workflow degrades software quality and produces the conditions that application security seeks to prevent.

Fix requests must not circumvent the processes software engineers rely on. Bypassing established workflows leads to misunderstandings and mistakes. AppSec should not expect developers to act on security findings without clear, actionable information and the opportunity to work through their standard processes.

This section is the **Actionable Security Intelligence Principle** (Section 6.1) applied to tool output. Scanner results, penetration test findings, and monitoring signals are raw material, and the principle holds that they become useful only when converted into specific, engineering-grounded direction tied to requirements, acceptance criteria, and the team's existing workflow. Treating security output as finished intelligence rather than input to it produces the same breakdown the Shoveling Left discussion describes, just arriving through a different channel.

---

## 7. Roles and Responsibilities

### 7.1. The Role of the Security Team

The security team can ensure timely delivery of securable outcomes by guiding Software Engineers through a self-governed process with verified results. Early engagement in design, requirements gathering, and architecture review sets the true guardrails for development.

The security team isn't responsible for adherence to architecture or feature requirements. That's the development team's accountability, enforced through standard Quality Assurance and User Acceptance processes. Security metrics from application security testing tools and penetration tests measure partnership effectiveness, not development compliance.

Measure partnership effectiveness through security metrics from application security testing tools and penetration tests, not development compliance. This distinction lets the security team focus on providing value through their participation in requirements, design, and assurance rather than policing developers for line-level fixes.

When requirements are complete and acceptance criteria are explicit, security metrics measure implementation completeness against a defined baseline. When requirements are absent or vague, the same metrics measure noise.

A stagnant security posture signals the need for adjustments to the development culture or leadership. The security team can influence this by promoting FIASSE and sponsoring education. Accepting its authority's limits is essential: the development team balances business value creation with security needs. The security team's effectiveness is limited by software quality.

By investing in design activities, they empower more developers to take ownership of their code's security posture, promoting a culture of collective accountability. Engineers are guided by security professionals following established engineering practices.

The security team's effectiveness is limited by software quality. SSEM makes this relationship explicit: a securable system's attributes – Analyzability, Modifiability, Testability, and others – define well-engineered software. A development team that pursues quality builds software more amenable to security analysis, faster to remediate, and more resilient over time. Application security cannot outperform the engineering practices beneath it.

### 7.2. Senior Software Engineers

Senior software engineers are crucial to any Application Security program's success, their value increasing as AI-assisted development becomes standard. AI tools generate code at scale but lack judgment, unable to evaluate design decisions, trust boundaries, or whether generated implementations meet security intent. The ability to make those assessments, grounded in SSEM attributes and established engineering principles, is a key differentiator.

Security professionals should collaborate closely with senior engineers in design activities, treating them as primary technical partners for FIASSE adoption.

Senior engineers apply the question "What can go wrong?" at every stage of development, from initial design through merge review, including AI-generated code. They drive the creation of Security Requirements, Acceptance Criteria, and Threat Scenarios that inform both human implementation and AI-assisted generation.

As AI-assisted development becomes routine, senior engineers craft and maintain prompt engineering standards that embed SSEM attributes and securable coding expectations into generation workflows.

They champion and schedule regular dependency maintenance, mentor less experienced developers, and liaise with security teams to keep security alignment anchored in engineering practice.

### 7.3. Developing Software Engineers

Developing engineers benefit from mental models like SSEM and the practices FIASSE describes. They may not yet have an intuitive sense for "What can go wrong?" but can develop it through structured guidance, merge reviews, and pair programming. They may not yet have an intuitive sense for "What can go wrong?" but can develop it through structured guidance, merge reviews, and pair programming. FIASSE provides context for why certain practices matter, helping engineers build judgment in good and bad code. This judgment is crucial in a landscape where AI coding assistants generate large volumes of plausible code quickly.

The primary objective for developing engineers is to become strong software engineers. Security outcomes follow from sound engineering practice, and the two are not separable. Working from clear Requirements and Acceptance Criteria before beginning a change gives developing engineers a visible target.

Foundational securable practices reinforce this development. Writing unit tests that cover exceptional conditions and out-of-bounds values strengthens Testability. Applying defensive coding techniques, particularly input validation and output encoding at trust boundaries, produces code that is resilient by default. Exercising due diligence before introducing new external dependencies keeps the trust surface and ongoing maintenance burden under control. Understanding trust boundaries in the code they write and seeking to understand the broader architecture grounds day-to-day decisions in the system's security model.

Engineers scrutinize AI-generated code with the same critical eye as any other source. They review output against SSEM attributes, check trust boundaries, and verify it meets defined acceptance criteria before accepting it. They also learn to incorporate FIASSE concepts into prompts, specifying securable qualities like input validation, error handling, and least privilege.

Studying FIASSE and SSEM directly builds a mental model that turns engineering fundamentals into securable outcomes.

### 7.4. Product Owners and Managers

A FIASSE-literate Product Owner is a more effective decision-maker, communicator, and team leader. Understanding SSEM attributes and FIASSE principles changes the quality of decisions and conversations they lead.

At the specification level, a FIASSE-literate Product Owner assesses backlog items for securability implications, not just feature value. Maintainability work, dependency updates, and architectural improvements become investments in the product's long-term defensibility, not technical overhead.

A Product Owner who understands SSEM can author or validate criteria that reflect genuine security intent. This reduces the gap between what was specified and what was built, directly supporting the principle that implementation completeness against defined criteria is a measurable security outcome.

As the translator of technical decisions into business terms, a FIASSE-literate Product Owner communicates risk more accurately and credibly with leadership, customers, and auditors. They interpret threat findings in business terms to make informed decisions about risk acceptance, mitigation priority, and requirement changes.

Product leadership shapes securability through scope decisions and culture. Scope cuts and deadline pressures frequently target work that appears non-functional, including input validation, error handling, logging, and dependency updates. A Product Owner familiar with SSEM recognizes when a proposed cut degrades a securable attribute. The security posture that results is a product outcome the Product Owner is accountable for. Culture follows what leadership visibly values: a Product Owner who asks about threat scenarios, requires security acceptance criteria, and treats dependency maintenance as a scheduled commitment signals that securability is a first-class product quality.

FIASSE literacy supports the external and exceptional moments of the product role. In vendor selection and third-party integration decisions, it enables substantive evaluation of whether a proposed integration introduces dependency risks, whether the vendor's practices align with the team's stewardship standards, and whether the integration design respects the system's trust boundaries. A FIASSE-literate Product Owner can engage meaningfully in incident response, understanding what was affected and what systemic changes are needed. Post-incident, they are better positioned to drive backlog changes that address root causes rather than symptoms.

---

## 8. Organizational Adoption of FIASSE

FIASSE does not require a rigid adoption sequence, but organizations benefit from a deliberate implementation plan. The following steps represent a practical path toward successful integration:

1. **Assess current practices.** Evaluate organizational readiness for FIASSE through discussions with key stakeholders and a review of existing workflows.
   - Identify existing security practices and how they align with SSEM attributes.
   - Determine the current level of familiarity with software engineering principles among development teams.
   - Identify the misalignments that FIASSE can address.

2. **Integrate SSEM terminology.** Deliberately incorporate SSEM attributes, including Maintainability, Trustworthiness, and Reliability, and their sub-attributes into developer documentation, coding standards, style guides, and training materials. This builds a common language for discussing and evaluating securability. Consider adopting terms such as *Defendable Authentication* as a broader vocabulary shift from static-state security language to securable-property language.

3. **Identify key influencers.** Find senior engineers and stakeholders who can internalize the framework and champion FIASSE adoption. These individuals should have a strong grounding in software engineering.

4. **Educate and train teams.** Provide role-specific training on FIASSE and SSEM to key influencers and integrate it into onboarding and continuous learning programs.
   - Both Development and AppSec should understand that FIASSE is to be discussed in the context of software engineering, not as a separate security initiative.
   - After initial training, ongoing delivery should occur within merge reviews, architecture discussions, and requirements sessions. Leaders should bring FIASSE into these activities directly.

5. **Foster collaboration.** Promote regular engagement between AppSec and Development. Discourage isolated reviews; encourage AppSec to participate in development activities such as requirements gathering.

6. **Monitor and improve continuously.** FIASSE is an ongoing process. Use real-time security observability to gather insights that refine security strategies and FIASSE implementation over time.

Regardless of organizational size, domain, or technology stack, the path to better security outcomes runs through the same place: engineers who understand what securable software looks like, teams that have the vocabulary to reason about it, and leaders who create the conditions for it to be built. FIASSE provides the structure to get there. The investment is in engineering culture, and the return compounds over time.

---

## 9. Conclusion

Organizations invest in secure coding initiatives and security testing, yet application security outcomes remain difficult to improve at scale. The root cause is structural. Security expertise has not been applied where it produces the most value, and developers have not been given explicit, engineering-grounded expectations for what securable software looks like. FIASSE exists to change that.

The central shift FIASSE asks for is a change in how security is applied. Securable software is software whose engineering qualities allow it to remain defensible as the system evolves and the threat landscape changes. That shift changes how engineers build, how security teams engage with development, and gives leaders the grounding to make more informed decisions about risk and investment. Securability is the engineering discipline that makes building software in an ever-shifting threat landscape reasonable.

For Software Engineers: the practices in this document are extensions of what good engineering already looks like. Apply SSEM attributes to the code you write and the code you review. Principles including defensive coding, clear trust boundaries, transparent instrumentation, complete requirements, and dependency stewardship will guide you in building securable software without weighing you down.

For security professionals: the leverage point is earlier and further upstream than testing. Requirements, design, and architecture are where security expectations become structural. Set them there. Use SSEM as the shared vocabulary that lets you engage with development teams on engineering terms rather than security mandates. Measure the partnership through implementation completeness against defined criteria, not through vulnerability counts alone.

For Product Owners: the security posture of your product is a product decision. Every scope cut that removes input validation, every sprint that defers dependency maintenance, and every story accepted without security acceptance criteria is a decision with a security consequence. FIASSE literacy makes those consequences visible before they become incidents. The adoption steps in Section 8 provide a concrete starting point.

Securability is not a destination. It is a discipline that begins with the next line of code written or generated, the next requirement authored, the next merge reviewed. Start there.

---

## 10. References

[Boehm1981] Boehm, B.W., "Software Engineering Economics", Prentice-Hall, 1981. ISBN 0-13-822122-7.

[Howard] Howard, R., "Cybersecurity First Principles: A Reboot of Strategy and Tactics", Wiley, 2023. ISBN 978-1-394-17308-2.

[ISO-24765] ISO/IEC/IEEE 24765:2017, "Systems and software engineering - Vocabulary". International Organization for Standardization.

[ISO-25010] ISO/IEC 25010:2011, "Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models". International Organization for Standardization.

[ISO-27000] ISO/IEC 27000:2018, "Information technology - Security techniques - Information security management systems - Overview and vocabulary". International Organization for Standardization.

[Kalman1960] Kalman, R.E., "On the general theory of control systems", Proceedings of the 1st IFAC Congress, Moscow, Butterworths, London, 1960, pp. 481–492.

[LINDDUN] DistriNet Research Unit, KU Leuven, "LINDDUN Privacy Threat Modeling". <https://linddun.org/>.

[OWASP-CRG] OWASP Code Review Guide. <https://owasp.org/www-project-code-review-guide/>.

[PASTA] UcedaVelez, T. and Morana, M.M., "Risk Centric Threat Modeling: Process for Attack Simulation and Threat Analysis". Wiley, 2015. ISBN 978-0-470-50096-5.

[STRIDE] Shostack, A., "Threat Modeling: Designing for Security", Wiley, 2014. ISBN 978-1-118-80999-0.

[TM-Manifesto] Braiterman, Z. et al., "Threat Modeling Manifesto". <https://www.threatmodelingmanifesto.org/>.

---

## Appendix A: Measuring SSEM Attributes

Measuring the attributes defined by SSEM quantifies and evaluates the securable qualities of software. The following approaches cover each core attribute and provide actionable indicators to guide improvement.

### A.1. Measuring Maintainability

#### A.1.1. Analyzability

**Quantitative:**

- **Volume (Lines of Code):** Tracked per module/system. Lower LoC for a given functionality can indicate better analyzability.
- **Duplication percentage:** Measured by static analysis tools (e.g., SonarQube, PMD). Lower is better.
- **Unit size (e.g., mLoC/cLoC):** Average lines of code per method or class. Excessively large units are harder to analyze.
- **Unit complexity (e.g., Cyclomatic Complexity):** Measured by static analysis tools. Lower complexity per unit is generally better.
- **Comment density/quality:** Ratio of comment lines to code lines, or qualitative review of comment usefulness.

**Qualitative/process-based:**

- **Time to Understand (TTU):** Average time for a developer unfamiliar with a section of code to understand its purpose and flow for a specific task.
- **Developer surveys:** Periodic developer ratings of the analyzability of modules they work with.

#### A.1.2. Modifiability

**Quantitative:**

- **Module coupling (afferent/efferent):** Number of incoming and outgoing dependencies for modules. Lower afferent coupling typically indicates a module is easier to change without broad impact.
- **Change impact size:** Number of files/modules typically affected by a common type of change. Smaller is better.
- **Regression rate:** Percentage of changes that introduce new defects. Lower is better.

**Qualitative/process-based:**

- **Ease of change assessment:** During code reviews, assess how difficult a hypothetical related change would be.
- **Time to implement change:** Average time to complete standard types of modifications or feature enhancements.

#### A.1.3. Testability

**Quantitative:**

- **Code coverage:** Percentage of code covered by automated tests (unit, integration). Higher is generally better.
- **Unit test density:** Number of unit tests per KLoC or per class/module.
- **Mocking/stubbing complexity:** Difficulty or setup required to isolate units for testing.

**Qualitative/process-based:**

- **Ease of writing tests:** Developer feedback on how straightforward it is to write meaningful tests for new or existing code.
- **Test execution time:** Excessively long test suite runs can reduce testing frequency, indirectly affecting testability in practice.

#### A.1.4. Observability

**Quantitative:**

- **Log coverage:** Percentage of trust boundaries and security-sensitive operations emitting structured log events with sufficient context (identity, action, outcome, timestamp).
- **Instrumentation coverage:** Fraction of critical execution paths exposing health and performance metrics through a standardized API (e.g., authentication failure counts, input validation error rates, resource utilization).
- **Alert signal-to-noise ratio:** Ratio of actionable alerts to total alerts fired over a reporting period. A low ratio indicates instrumentation that generates noise rather than insight.
- **Mean Time to Detect (MTTD):** Average elapsed time between an anomalous event occurring and its appearance in monitoring output. Lower values indicate more effective instrumentation.

**Qualitative/process-based:**

- **Structured logging review:** Assessment of whether log entries include sufficient context to support incident analysis. Specifically whether the who, what, where, when, and outcome of security-relevant events are captured, not just that an event occurred.
- **Code-level instrumentation audit:** Review of whether observability is built into the code itself at key points, or whether it depends entirely on external tooling. A system that is not instrumented at the code level is opaque by construction; this audit identifies those blind spots.
- **Failure-path observability:** Assessment of whether error and recovery paths produce observable output. Silent failures and exception swallowing are common gaps; code paths that produce no signal under failure conditions should be identified and instrumented.
- **UI and operator feedback review:** Assessment of whether the system surfaces meaningful state to operators and end users at decision points (including error messages, permission feedback, and session state) without leaking internal implementation details.

### A.2. Measuring Trustworthiness

#### A.2.1. Confidentiality

**Quantitative:**

- **Number of identified data leaks:** From penetration tests, code reviews, or incidents.
- **Access control violations:** Number of logged unauthorized access attempts, whether prevented or successful.

**Qualitative/process-based:**

- **Data classification adherence:** Review of how well data is classified and whether protections align with that classification.
- **Principle of least privilege review:** Assessment of whether components and users have only the necessary permissions.
- **Effectiveness of encryption:** Review of encryption algorithms used and key management practices.

#### A.2.2. Accountability

**Quantitative:**

- **Audit log coverage:** Percentage of critical system actions logged with sufficient detail.
- **Traceability success rate:** Percentage of audited actions that can be uniquely attributed to an entity.

**Qualitative/process-based:**

- **Audit log review findings:** Results from periodic reviews of audit logs for completeness and usefulness.
- **Non-repudiation strength:** Assessment of the evidence quality linking actions to entities (e.g., use of digital signatures).

#### A.2.3. Authenticity

**Quantitative:**

- **Authentication failures:** Number of failed login attempts (can indicate brute-forcing or misconfiguration).
- **Authentication mechanism coverage:** Percentage of authentication points implementing factors appropriate to the context, with a documented rationale for each configuration choice.

**Qualitative/process-based:**

- **Verification of identities:** Review of processes for verifying user and system identities.
- **Defendability of authentication mechanisms:** Assessment of whether the authentication system's design supports ongoing analysis, modification, and verification, testability of authentication flows, auditability of authentication events, and the ability to adapt controls as threats evolve.

### A.3. Measuring Reliability

#### A.3.1. Availability

**Quantitative:**

- Uptime percentage (e.g., 99.99%).
- Mean Time Between Failures (MTBF).
- Mean Time To Recovery (MTTR).

**Qualitative/process-based:**

- **Redundancy review:** Assessment of system redundancy for critical components.
- **Disaster recovery test results.**

#### A.3.2. Integrity

**Quantitative:**

- Number of data corruption incidents.
- Checksum/hash validation success rate for data at rest and in transit.

**Qualitative/process-based:**

- **Input validation effectiveness:** Review of input validation mechanisms at trust boundaries.
- **System file integrity monitoring alerts.**

#### A.3.3. Resilience

**Quantitative:**

- **Recovery Time Objective (RTO) adherence:** Frequency with which RTOs are met following an incident.
- **Performance under stress:** System performance metrics during load testing or simulated attacks (e.g., DDoS simulation).

**Qualitative/process-based:**

- **Defensive coding practices review:** Assessment of code for input validation, output encoding, and robust error handling.
- **Incident response plan effectiveness:** Review of how well the system and team recover from security incidents or operational failures.
