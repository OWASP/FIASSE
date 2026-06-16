# Developer Onboarding: How I Use FIASSE in My Day-to-Day Work

As a software engineer I understand the need to create [securable software](../framework/S2.1.0.md). This is accomplished in the way I build as part of my motivating principle of ["resiliently adding computing value"](../framework/S2.2.0.md). So, before I even start coding I confirm that I have good [requirements and acceptance criteria](../framework/S4.1.2.md). Then I [identify trust boundaries and risky inputs](../framework/S4.3.0.md) to think about how to [canonicalize](../framework/S4.4.1.md) them. Then I consider what error handling and logging would help make this feature easier to troubleshoot, maintain and secure if anything goes wrong. (Observability)

I write code so that I can understand it [(Analyzability)] when I come back later to make changes. I make sure there that there are no [hidden side effects]. I write code so that I am confident that I can make changes later without negative sideeffect [(Modifiability)]. I prove my code with Unit Tests that cover normal and abnormal values and states. I expect manual assurance tests to prove it as well. [(Testability)] If I choose to use [open source libraries], I make sure they fit these values too.

I know that I am not chasing a [static state of secure]. I am building software that is defensible as things change. I build knowing that there will be failures. I build so that failures are less likely to expose sensitive information. When things go wrong, I will need to be able to tell what caused the failure.

I value the feedback I get during [merge review](../framework/S5.2.0.md) because it helps me save rework next time. I take pride in the code I submit for merge, weather I hand wrote it or used an assistant to generate it. I want to make sure that the reviewer is able to understand the code too.

I accept that assurance may find things I did not think of, and when it does I will address these issues by applying the principles of FIASSE. This will reduce the rework that comes from hyper-focused test results based fixes because I will be looking at the context that resulted in the finding. I understand that the finding may only be one aspect of a broader issue.

FIASSE influences my approach by making security a natural output of software engineering, not a separate phase or surprise test.

## Quick Read Path

If I am new and want the fastest high-level understanding, I read in this order:

1. [Introduction and purpose](../securable_framework.md#1-introduction)
2. [Foundational principles](../framework/S2.0.0.md)
3. [SSEM model and attributes](../framework/S3.0.0.md)
4. [Practical developer guidance](../framework/S4.0.0.md)
5. [Developer role expectations](../framework/S7.3.0.md)

This gives me a clear mental model: write software that creates value and can stay defensible as the system, risks, and business needs evolve.
