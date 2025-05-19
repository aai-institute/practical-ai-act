# Transparency and Provision of Information

|Article 13| mandates that high-risk AI systems must be accompanied by _instructions for use_, so that their operation is sufficiently transparent to deployers.

This document equips deployers with the necessary information to ensure that they can operate the system appropriately and interpret its output.

A number of engineering practices can help providers to comply with the requirements of Article 13 by ensuring that the required information is collected in a structured and accessible manner.

!!! info "Engineering Info"
--8<-- "docs/conformity/\_engineering-info-box.partial"

    - [Explainability]:
        - |Art. 13(1)|: Explainability techniques contribute to a transparent system operation
        - |Art. 13(3)(b)(iv)(vii)|: Explainability techniques directly provide information relevant to explain the system's output
        - |Art. 13(3)(d)|: Explainability techniques can be used in the human oversight process to interpret the system's behavior
    - [Experiment Tracking]:
        - |Art. 13(3)(b)(ii)|: Experiment tracking captures used performance metrics and levels of accuracy
    - [Model Cards]:
        - |Art. 13(3)(b)|: Model-specific information can be documented in a model card
        - |Art. 13(3)(e)|: Computational/hardware resources needed can be documented in a model card
    - [Model Registry]:
        - |Art. 13(3)(b)(iv)|: Logging the model architecture and hyperparameters makes the system characteristics transparent
    - [Operational Monitoring]:
        - |Art. 13(3)(e)|: Monitoring the operation of the system enables to provide statistics about the system resource usage
    - [Data Versioning]:
        - |Art. 13(3)(b)(vi)|: Data versioning ensures that the data used for training and validation is documented and can be traced back

## Contents

The information contained in the instructions for use roughly falls into two categories:

-   Information about the system in [general](#generic-information)
-   Information about the system that is [specific to the model used](#model-specific-information)

There is significant overlap between the information required for the instructions for use and the information required for the [technical documentation](technical-documentation.md) of high-risk AI systems. While the kind of information
is the same, the intended audiences are different. Article 13 requires the instructions of use to be accessible and comprehensible to the deployer. In other words, providers must give some thought to the technical capabilities and knowledge of the deployer before drafting the instructions.

Both documents can benefit from a structured approach to documentation, such as the use of [model cards](../engineering-practice/model-cards.md) or [experiment tracking](../engineering-practice/experiment-tracking.md).

### Generic information

All information which is not specific for a single model or may be stable over
a long time:

-   |Art. 13(3)(a)|: the identity and contact details of provider
-   |Art. 13(3)(b)|:
    -   (i): intended purpose of the system
    -   (vi): information about the expected input data schema; relevant information about training/validation data sets
-   |Art. 13(3)(e)|:
    -   Computational/hardware resources needed
    -   Expected lifetime of the system
    -   Necessary maintenance and care measures (including software updates)

### Model-specific information

Other parts of the information to be included in the instructions for use refer to characteristics of the actual machine learning model employed in the system.

-   |Art. 13(3)(b)|:
    -   (ii): expected level of accuracy, metrics, robustness, and cybersecurity, used for testing and validation of the system; potential circumstances that may impact these characteristics (|Art. 15|)
    -   (iii): known or forseeable circumstances which may lead to a risk (|Art. 9|); can depend on the model's type
    -   (iv): technical characteristics and capabilities of the system relevant to explain its outputs
    -   (v): statistics about the system's performance regarding specific (groups of) persons
-   |Art. 13(3)(d)|: [Human-oversight measures] under |Art. 14|; technical measures that aid the interpretation of system outputs
-   |Art. 13(3)(f)|: Information about [record-keeping] mechanisms under |Art. 12| (collection, storage, and interpretation)

[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Cards]: ../engineering-practice/model-cards.md
[Model Registry]: ../engineering-practice/model-registry.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
[Data Versioning]: ../engineering-practice/data-governance/data-versioning.md
[Record-keeping]: ../conformity/record-keeping.md
[Human-oversight measures]: ../conformity/human-oversight.md
