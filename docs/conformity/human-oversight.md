# Human Oversight

|Article 14| of the EU AI Act establishes requirements for human oversight of high-risk
AI systems. When implementing human oversight requirements,
it's crucial to understand that automation opportunities are primarily limited to the
collection of metrics and supporting information. The substantive aspects
of oversight—interpretation, decision-making, and intervention—must remain human-driven.

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"
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


<!-- Reference Links -->
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
