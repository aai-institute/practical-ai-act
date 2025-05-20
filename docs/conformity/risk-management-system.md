# Risk Management System

|Article 9| of the EU AI Act establishes requirements for implementing a risk management system to identify, analyze, and manage risks and threats arising from the use of the AI system "to health, safety or fundamental rights", when used for its intended purpose or under reasonably foreseeable misuse (see |Art. 3(13)|).
Also, it requires a risk assessment for the case in which the AI system is used outside of its intended purpose, for example by a malicious actor.

!!! info "Engineering Info"

    --8<-- "docs/conformity/\_engineering-info-box.partial"

    - This document does not directly reference other articles in the AI Act, since it is mostly out of scope for the engineering practices described in this project.s

## Non-technical requirements

Even though it is named a "system", the risk management system introduced in the article is not necessarily a physical system, but rather a list of actions and provisions.
Similarly, it is not meant as a single condition that an AI system must satisfy to be allowed to operate, but rather a continuous loop of evaluation for the AI system throughout its lifecycle.

It might be more sensible to interpret this article not as a requirement addressed by a single software system, but rather as a guideline that should be adhered to by all personnel involved in the design and implementation of the AI system, and be applied as a "continuous iterative process" (cf. Art. 9, Section (2)) throughout the project lifecycle.

In general, providers must identify, evaluate, and mitigate risks that are known and "reasonably" foreseeable.
These risks might emerge both when the system is being used as intended and when it being misused in ways that are foreseeable. Finally, providers must also mitigate risks that are identified after the system goes into production.

While these concepts may seem vague at first, it is expected that harmonized technical standards will help engineers better understand what types of risks and circumstances they should consider.

Since the threat vectors of each system are different, it is in general not feasible to automate these risk assessments.

One clear requirement however is that high-risk AI systems should be tested continuously, but at the latest before they are productionized and made available to end users (see Sections (6) to (8)).
We highlight that the risk management system as presented in Article 9 is not directly tied to, but in fact a requirement for a lot of the engineering practices showcased in this repository, since they require prior knowledge about the relevant risks of the project.
