# Accuracy, Robustness and Cybersecurity

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - [Bias Mitigation]:
        - |Art. 15(4)|, Bias mitigation increases resilience against bias-related errors and inconsistencies
    - [Containerization]:
        - |Art. 15(1)|, Containers provide a consistent and isolated runtime environment
        - |Art. 15(4)|, Containers allow for redundant, reproducible and reliable application execution
    - [Experiment Tracking]:
        - |Art. 15(3)|, Experiment tracking captures used performance metrics and levels of accuracy
    - [Model Monitoring]:
        - |Art. 15(4)|, Resilience and robustness through continuous monitoring of model performance
    - [Operational Monitoring]:
        - |Art. 15(4)| Monitoring and alerting can help detect and mitigate potential robustness and availability issues
        - |Art. 15(5)| Monitoring is a crucial part of threat detection

## Motivation

This article requires that high-risk AI systems be designed to achieve appropriate levels of accuracy, robustness, and cybersecurity. However, these terms are not clearly defined within the context of the AI Act. It makes sense to get an understanding, which dimensions of the AI systems shall be addressed.

## Accuracy

|Art. 15(2)| makes it clear that _accuracy_ in the context of the AI Act _does not_ equal the established metric by the same name, but rather should be understood as a set of quality measures of a system.
In the case of a classification the accuracy metric might one but not the only applicable quality measure.

Which specific metric is most suitable as quality measure heavily depends on the problem type at hand.

The accuracy of AI systems should be declared in their [instructions for use](./instructions-for-use.md).

Systems that continually learn after being put in production should be designed to minimize risks of producing biased outputs based on feedback loops.

## Robustness

Systems should perform consistently throughout their lifecycle, be resilient to errors and faults, and have measures in place to mitigate risks associated with cybersecurity threats.

ISO/IEC 25059:2023 (_Artificial intelligence concepts and terminology_) defines robustness as the "ability of a system to maintain its level of performance under any circumstances".
This contrasts with the definition of accuracy, which focuses on the performance on a distinct evaluation data set.

## Cybersecurity

<!-- Reference Links -->
[Containerization]: ../engineering-practice/containerization.md
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md

## Resources

- [ISO/IEC TS 4213:2022](https://www.iso.org/standard/79799.html):
    - provides a broad overview of statitical metrics suitable for various forms of classfification problems.
    - The upcoming replacement, currently in its draft stage as [ISO/IEC AWI 4213](https://www.iso.org/standard/89455.html) broadens the scope to include measures of performance for classification, regression, clustering and recommendation tasks
- [TODO: Check if we want to keep this link](https://encord.com/blog/model-robustness-machine-learning-strategies/)
- [Robustness and Explainability of Artificial Intelligence](https://publications.jrc.ec.europa.eu/repository/handle/JRC119336)