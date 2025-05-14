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

Furthermore, specific methods are easily available through existing software packages and utilizing them could be considered as best practice (see the upcoming [ISO/IEC DTS 6254](#iso6254) technical specification, which gives an overview of the taxonomy and techniques for explainability).

## Implementation Notes

See the [showcase](../showcase/implementation-notes/explainability.md) for an example how explainability techniques can be integrated into the AI system, with a possibility for users to request explanations for any given model prediction.

One important consideration when implementing explainability techniques is way in which the explanations are presented to the user, which has a direct impact on the requirement for human oversight in the AI Act.

### Explainability Techniques

#### Inherently interpretable models

Some machine-learning models and algorithms are _inherently interpretable_, meaning their prediction outputs can be interpreted in terms of humanly understandable concepts.
One such example is the _k-nearest-neighbor_ (KNN) classification algorithm, where the resulting model classifies any datapoint as a weighted sum of its most similar (i.e. "nearest", for a specific definition of near) points in a given feature space.

Inherent interpretability usually requires a well-established mathematical theory on the problem and the used algorithms in question.
Sometimes, this limits the feasibility of such solutions, since "black-box" approaches that are not directly interpretable compare favorably in terms of compute performance and accuracy.

#### Post-hoc explanations

For models that are not directly interpretable ("black-box" models) like deep neural networks, gradient boosting algorithms, etc., post-hoc explainability provides a means to evaluate the model decisions _after_ they made a prediction.

Post-hoc methods can provide explanations on two distinct levels, _global_ and _local_.
Local methods explain the model's behavior for a single instance, while global methods provide an overview of the model's behavior across an entire dataset.

Post-hoc methods are more widely applicable in general, since they do not require direct interpretability of the model.
One possible angle of post-hoc explainability is measuring _feature importance_, which gives an idea about which input features influence the model's decision, and how big their individual influences are (with _SHAP_ being a commonly used technique from this class, see [below](#key-technologies)).

A second class of post-hoc explainability methods are _surrogate models_, which use inherently interpretable models that approximate the behavior of a black-box model in the neighborhood of a given input (one widely used technique is _LIME_, see [below](#key-technologies)).

When offering explanations for predictions to the users of an AI system, it is important to present the values concise and in a sensible way.
One such option is to render the results in a visualization (plot), which tends to work well for feature importance scores such as SHAP explanations.

#### Empirical analysis methods

Empirical analysis methods are a class of post-hoc explainability techniques that rely on the empirical evaluation of the model's behavior.
Techniques like statistical analysis of the model's prediction errors or the response to modifications of the system (e.g., in ablation experiments, where performance is analyzed before and after the removal of a part of the model, such as an input feature) fall into this category.

Another empirical technique is the use of challenge datasets, which are datasets that are specifically designed to test the limits of a model's performance on, without the goal of testing the model's generalization performance or being representative of the targeted domain.

## Key Technologies

-   The [`shap`](https://shap.readthedocs.io/en/latest/) Python package, implements the SHAP (SHapley Additive exPlanations) method
-   The [`lime`](https://lime-ml.readthedocs.io/en/latest/index.html) Python package, another popular model-agnostic explainability method (Local Interpretable Model-agnostic Explanations)
-   Intrinsically explainable models:
    -   The [`interpret`](https://interpret.ml/) Python package providing implementations for such glassbox models

## Resources

-   As a primer, [appliedAI TransferLab series on Explainable AI](https://transferlab.ai/series/explainable-ai/)
    and the accompanying [training](https://github.com/aai-institute/tfl-training-explainable-ai)
-   [Molnar (2025) - Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/), a comprehensive book on interpretability and explainability methods
-   The chapter on explainability in [Mucsányi, et al. (2023) - Trustworthy Machine Learning](https://trustworthyml.io/)
-   <a name="iso6254"></a> The upcoming revision of the [ISO/IEC DTS 6254](https://www.iso.org/standard/82148.html) standard describes approaches and methods used to achieve explainability objectives.
