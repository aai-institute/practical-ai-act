# Risk Management System

|Article 9| of the EU AI Act establishes requirements for implementing a risk management system to identify, analyze, and manage risks and threats arising from the use of the AI system "to health, safety or fundamental rights", when used for its intended purpose or under reasonably foreseeable misuse (see |Art. 3(13)|).
Also, it requires a risk assessment for the case in which the AI system is used outside of its intended purpose, for example by a malicious actor.

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - This document does not directly reference other articles in the AI Act, since it is mostly out of scope for the engineering practices described in this project.s

## Non-technical requirements

Even though it is named a "system", the risk management system introduced in the article is not necessarily a physical system, but rather a list of actions and provisions.
Similarly, it is not meant as a single condition that an AI system must satisfy to be allowed to operate, but rather a continuous loop of evaluation for the AI system throughout its lifecycle.

Some formulations in the article are rather vague (e.g. "reasonably foreseeable misuse", cf. Section 2(b)), presumably to be qualified later in standards and supplemental documents.
As such, it might be more sensible to interpret this article not as a requirement addressed by a single software system, but rather as a guideline that should be adhered to by all personnel involved in the design and implementation of the AI system, and be applied as a "continuous iterative process" (cf. Art. 9, Section (2)) throughout the project lifecycle.

In general, a lot of the responsibilities of the AI system provider depends on the interpretation of the word "reasonable". Only the risks that can be reasonably estimated (and mitigated) need to be guarded against.
Since the threat vectors of each system are different, it is in general not feasible to automate these risk assessments.

One clear requirement however is that high-risk AI systems should be tested continuously, but at the latest before they are productionized and made available to end users (see Sections (6) to (8)).
We highlight that the risk management system as presented in Article 9 is not directly tied to, but in fact a requirement for a lot of the engineering practices showcased in this repository, since they require prior knowledge about the relevant risks of the project.

## Relation to other Articles

The most important articles related to Article 9 are:

- |Art. 14| (Human Oversight): Risks should be assessed, evaluated, and mitigated by knowledgeable personnel.
- |Art. 15| (Accuracy, Robustness and Cybersecurity): As unauthorized access to AI systems and hardware is a great risk,
    it must be continuously assessed.
