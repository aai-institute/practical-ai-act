# Human Oversight

|Article 14| of the EU AI Act establishes requirements for human oversight of high-risk
AI systems. When implementing human oversight requirements,
it's crucial to understand that automation opportunities are primarily limited to the
collection of metrics and supporting information. The substantive aspects
of oversight—interpretation, decision-making, and intervention—must remain human-driven.

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    Related engineering practice focus on implementing comprehensive oversight measures
    that enable human supervision of AI systems. These measures must be integrated
    throughout the system's lifecycle—from design to deployment and
    operation—ensuring humans can make informed interventions.

    - [Experiment Tracking]:
        -   |Art. 14(4)(a)|, understand the limitation of the underlying model by
            interpreting performance on reference data
    - [Explainability]:
        -   |Art. 14(3)(a)|, automated XAI features can be built directly into
            the system to generate explanations
        -   |Art. 14(4)(c)|, explainability approaches provide the necessary information
            to enable human interpretation of system outputs
        -   |Art. 14(4)(d)|, automated explanations provide the basis for humans
            to decide whether to use or disregard outputs
    - [Model Monitoring]:
        -   |Art. 14(4)(a)|, automated tracking of drift and performance degradation
            helps to understand the capacities of the system during its lifetime
        -   |Art. 14(4)(e)|, observing degradation overtime enables to intervene and
            initialize a retraining, for example
    - [Operational Monitoring]:
        -   |Art. 14(4)(e)|, continuous monitoring the operation of the systems helps
            to detect conditions requiring potential intervention


## Non-technical Requirements
The text of |Art. 14| itself focuses on the suitability of oversight measures,
which should enable human operators. There is a rather implicit requirement, namely
that the designated person has to be able to digest, interpret those and launch appropriate
actions based on the bespoken oversight measures. While the technical features
of oversight (e.g. explainability, monitoring, alerts) provide the means, they
must be matched with human readiness to act on them. This is also connected to
the requirements stated in |Art. 4 (AI literacy)|.


## Relation to other Articles

In addition to |Art. 4|, the following connections are prevalent:

- |Art. 9| (Risk Management System): Oversight measures should be embedded into
    the risk management strategy, particularly for monitoring risks during operation.
- |Art. 11| (Technical Documentation): For oversight to be actionable and traceable,
    systems must be accompanied by clear, structured, and accessible documentation.
- |Art. 13| (Transparency and Provision of Information to Deployers): Provide
    the context necessary for humans to interpret system behavior and make informed
    decisions about its use.

<!-- Reference Links -->
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
