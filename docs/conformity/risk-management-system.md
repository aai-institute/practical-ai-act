# Risk Management System

|Article 9| of the EU AI Act establishes requirements for implementing a risk management system to identify risks and threats arising from the use of the AI system "to health, safety or fundamental rights", when used for its intended purpose.
Also, it requires a risk assessment for the case in which the AI system is used outside of its intended purpose, for example by a malicious actor.

<!-- TODO: Add Art. 9b to the containerization article list -->

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - [Containerization]:
        - |Art. 9(b)|: Containerizing applications to prevent jailbreaks and unauthorized access to servers.

## Non-technical requirements

Even though it is named a "system", the risk management system introduced in the article is not necessarily a physical system, but rather a list of actions and provisions.
Similarly, it is not meant as a single condition that an AI system must satisfy to be allowed to operate, but rather a continuous loop of evaluation for the AI system throughout its lifecycle.

Some formulations in the article are left unexplained and rather vague (e.g. "reasonably foreseeable misuse", cf. Section 2(b)), presumably to be qualified later in standards and supplemental documents.
As such, it might be more sensible to interpret this article not as a requirement addressed by a single software system, but rather as a guideline that should be adhered to by all personnel involved in the design and implementation of the AI system.

In general, a lot of the responsibilities of the AI system implementer depends on the interpretation of the word "reasonable". Only the risks that can be reasonably estimated (and mitigated) need to be guarded against.
Since the threat vectors of each system are different, it is in general not feasible to automate these risk assessments.

## Relation to other Articles

The most important articles related to Article 9 are:

- |Art. 14| (Human Oversight): Risks should be assessed, evaluated, and mitigated by knowledgeable personnel.
- |Art. 15| (Accuracy, Robustness and Cybersecurity): As unauthorized access to AI systems and hardware is a great risk,
    it must be continuously assessed.


<!-- Reference Links -->
[Containerization]: ../engineering-practice/containerization.md