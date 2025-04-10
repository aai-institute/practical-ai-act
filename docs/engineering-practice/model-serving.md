---
tags:
    - Art. 15
---

# Model Serving

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    TODO: Incomplete

    - **|Art. 15|** (Accuracy, Robustness and Cybersecurity)

## Motivation

Model serving is the process of deploying machine learning models to production environments, where they can be accessed and used by applications or users.

Not every AI system involves a real-time inference component, for example batch processing systems or offline analytics.
However, for those that do, model serving is a critical part of the machine learning lifecycle.

Model serving needs to be designed to ensure that the deployed models are accurate, robust, and secure.

## Implementation Notes

[Containerization](containerization.md) is a common practice for model serving, as it allows for the deployment of models in isolated environments, ensuring consistency and reproducibility.
It also enables the use of different versions of models and dependencies without conflicts.

The models to be deployed should be obtained from a [model registry](model-registry.md), in order to preserve the traceability and reproducibility of the models.
A model serving should be able to expose metadata about the model and its provenance, in order to associate this information with every prediction (see the page on [inference logs](inference-log.md)).

### Inference API Design

Real-time inference APIs provide the interface for applications to interact with the deployed models.

Designing the API for an interface is a trade-off between flexibility and usability.

While a bespoke API can be designed for a single model (which might be tied to a specific input data schema), a more generic API can be designed to support multiple models and input data schemas.

One such generic API is specified as the [Open Inference Protocol](https://github.com/kserve/open-inference-protocol), which is supported by several model serving frameworks.
It provides API endpoints and type definitions for inference requests (with a flexible data schema), model metadata, and model management.

## Key Technologies

-   [MLServer](https://mlserver.readthedocs.io/en/latest/)
-   [BentoML](https://docs.bentoml.org/en/latest/)
-   [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/)
-   [KServe](https://kserve.github.io/website/)
