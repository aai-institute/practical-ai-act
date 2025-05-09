---
tags:
    - Art. 11
    - Art. 13
    - Art. 14
    - Art. 86
    - Annex IV
---

# Explainability

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation), in particular:
        - |Annex IV(3)|: Explainability techniques can be part of the instructions for use to the deployer
    - **|Art. 13|** (Transparency and Provision of Information to Deployers), in particular:
        - |Art. 13(1)|: Explainability techniques contribute to a transparent system operation
        - |Art. 13(3)(b)(iv)|: Explainability techniques directly provide information relevant to explain the system's output
        - |Art. 13(3)(d)|: Explainability techniques can be used in the human oversight process to interpret the system's behavior
    - **|Art. 14|** (Human Oversight), in particular:
        - |Art. 14(3)(a)|: automated XAI features can be built directly into
            the system to generate explanations
        - |Art. 14(4)(c)|: explainability approaches provide the necessary information
            to enable human interpretation of system outputs
        - |Art. 14(4)(d)|: automated explanations provide the basis for humans
            to decide whether to use or disregard outputs
    - **|Art. 86(3)|** (Right to Explanation of Individual Decision-Making)

## Motivation

Although there is no explicit demand for using explainability methods within the AI Act, they can aid compliance with the regulation, by providing insights into the system's decision-making process.

In particular, these explanation approaches can assist the operator of the system in interpreting the system's behavior, as part of the human oversight process (see |Art. 14|) and allow affected third parties to request an explanation of the system's output (see |Art. 86(3)|).
As part of the instructions for use to the deployer (see |Art. 13(3)(b)(iv)|), they can be used to provide information relevant to explain the system's output.

Furthermore, specific methods are easily available through existing software packages and utilizing them could be considered as best practice (see upcoming [ISO norm](#iso6254)).

## Implementation Notes

TODO: Explain different explainability methods and their use cases (post-hoc, inherently explainable models, etc.).

See the [showcase](../showcase/implementation-notes/explainability.md) for an example how explainability techniques can be integrated into the AI system, with a possibility for users to request explanations for any given model prediction.

## Key Technologies

-   The [`shap`](https://shap.readthedocs.io/en/latest/) Python package, implements the SHAP (SHapley Additive exPlanations) method
-   The [`lime`](https://lime-ml.readthedocs.io/en/latest/index.html) Python package, another popular model-agnostic explainability method (Local Interpretable Model-agnostic Explanations)
-   Use of intrinsically explainable models:
    -   The [`interpret`](https://interpret.ml/) Python package providing implementation for such glassbox models

## Resources

-   As a primer, [appliedAI TransferLab series on Explainable AI](https://transferlab.ai/series/explainable-ai/)
    and the accompanying [training](https://github.com/aai-institute/tfl-training-explainable-ai)
-   From the book [Trustworthy Machine Learning](https://trustworthyml.io/), Chapter about Explainability
-   <a name="iso6254"></a> The upcoming revision of the [ISO/IEC DTS 6254](https://www.iso.org/standard/82148.html) standard will describe approaches and methods used to achieve explainability objectives.
