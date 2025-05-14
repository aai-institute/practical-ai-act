---
tags:
    - Art. 11
    - Art. 13
    - Annex IV
---

# Model cards

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    Keeping a model card will help you in achieving compliance with the following requirements, since they are well-suited to provide or supplement the required information:

    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation)
    - **|Art. 13(3)|** (Transparency and Provision of Information to Deployers)

## Rationale

Model cards are a somewhat standardized form of documentation that provide a comprehensive overview of an AI model, including its intended use and limitations, used datasets, evaluation results and performance metrics, and ethical considerations.
The general structure of a model card encompasses the following sections:

-   Model name and details
-   Model owners
-   Model architecture and compute infrastructure
-   Intended uses (and potential limitations)
-   Training procedure and parameters
-   Used datasets
-   Evaluation results (datasets, metrics, factors, etc.)
-   Ethical considerations
-   Caveats and recommendations

This information greatly overlaps with the information required for the [technical documentation](../conformity/technical-documentation.md) of high-risk AI systems and the necessary information that should be supplied to deployers of such systems as part of the [instructions for use](../conformity/instructions-for-use.md).

Model cards are a useful tool to increase the transparency along the value chain of an AI system, from developers and providers, to deployers, certification bodies and market authorities, and ultimately end-users.

## Implementation Notes

While no single universal format for model cards exists, the YAML-based format used by [Hugging Face](https://huggingface.co/docs/hub/model-cards) is a good starting point.
This format strikes a good balance between ease of creation and possibility for automated processing.

Parts of the information in a model card can be generated automatically from the model metadata, such as the model's architecture, training data, and evaluation results, using appropriate libraries and tools.
[Experiment tracking tools](./experiment-tracking.md), [workflow orchestrators](./orchestration.md), and [data versioning tools](data-governance/data-versioning.md) can serve as the authoritative source for this metadata.

Since the information in a model card is tied to a specific model version, it is important to ensure that the model card is appropriately versioned, such that a clear link between a model version and its accompanying model card can be established.
This can be achieved by storing the model card as an artifact alongside the model in an [experiment log](./experiment-tracking.md), or by using a version control system to track the model card.

## Key Technologies

-   [Hugging Face Model Cards](https://huggingface.co/docs/hub/model-cards), which provides a standard YAML format for model cards
    -   [Markdown template](https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1) for Hugging Face model cards
-   [Model Card Toolkit](https://www.tensorflow.org/responsible_ai/model_card_toolkit/guide), a Python library for automatic creation of model cards
-   The [`skops`](https://skops.readthedocs.io/en/latest/index.html) Python library, which can create Hugging Face model cards for scikit-learn models

## Resources

-   [Mitchell, et al. (2018) - Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993), the original research paper on model cards
-   [Ozoani, et al. (2022) - Model Card Guidebook, Hugging Face](https://huggingface.co/docs/hub/en/model-card-guidebook)
-   [Model Cards Explained](https://modelcards.withgoogle.com/), provides explanations and examples of model cards for various Google AI models
