# Accuracy, Robustness and Cybersecurity

This article requires that high-risk AI systems be designed to achieve appropriate levels of accuracy, robustness, and cybersecurity. However, these terms are not clearly defined within the context of the AI Act. It makes sense to get an understanding, which dimensions of the AI systems shall be addressed.

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


## Accuracy

|Art. 15(2)| makes it clear that _accuracy_ in the context of the AI Act _does not_ equal the established metric by the same name, but rather should be understood as a set of quality measures of a system.
In the case of a classification the accuracy metric might one but not the only applicable quality measure.

Which specific metric is most suitable as quality measure heavily depends on the problem type at hand.
A good overview for the case of classification problems can be found in the norm document [ISO/IEC TS 4213:2022](#iso4213).
The upcoming replacement of this specification broadens the scope to include measures of performance for classification, regression, clustering and recommendation tasks.

|Annex IV| mandates that the technical documentation must include a description of the metrics used to measure the accuracy of the system.
In order to achieve a better level of transparency, information about the accuracy of AI systems should also be included in their [instructions for use](./instructions-for-use.md).

## Robustness

Systems should perform consistently throughout their lifecycle, be resilient to errors and faults, and have measures in place to mitigate risks associated with cybersecurity threats.

ISO/IEC 25059:2023 (_Artificial intelligence concepts and terminology_) defines robustness as the "ability of a system to maintain its level of performance under any circumstances".
This contrasts with the definition of accuracy, which focuses on the performance on a distinct evaluation data set.

In practice, this means that there is a trade-off between maximizing the accuracy of a system, as evaluated on a test set, and ensuring its robustness in the real world.

A valuable synergy emerges from making AI systems more [interpretable and explainable](../engineering-practice/explainability.md) as this can also help to improve their robustness, by providing measures which allow to identify and mitigate potential issues with the system's performance.
[Model monitoring techniques](../engineering-practice/model-monitoring.md) like anomaly detection can also be used to identify potential issues with the system's performance.

See chapter 10 of the [ISO/IEC TS 25058:2024](#iso25058) (_Guidance for quality evaluation of artificial intelligence (AI) systems_) for guidance on how to evaluate the robustness of AI systems.
For neural networks in particular, also refer to the [ISO/IEC TR 24029](#iso24029) (_Assessment of the robustness of neural networks_) series for concrete assessment methods.

### Prevention of Bias Feedback Loops

High-risk AI systems that continually learn after being put in production should be designed to minimize risks of producing biased outputs based on feedback loops. 

To make this more concrete, consider our [use-case](../showcase/index.md) example of an assistant system for hiring processes. If the system (without proper mitigation measures) is biased against applicants from a certain demographic, it may negatively affect the hiring chances for the applicants.
If the output of the HR system is subsequently used to retrain the AI system, it may lead to a feedback loop that further amplifies the pre-existing bias.

See the page on [bias mitigation](../engineering-practice/data-governance/bias-mitigation.md) to understand how to address bias concerns when building an AI system.

## Cybersecurity

Besides the classical issues of cybersecurity, such as confidentiality, integrity, and availability, the AI Act also requires that high-risk AI systems be designed to be resilient attacks specific to AI systems:

- Data poisoning
- Model poisoning
- Adversarial attacks / model evasion
- Confidentiality attacks, like model inversion or model theft

In practice, this means that the cybersecurity measures for high-risk AI systems should encompass both traditional cybersecurity measures and the tactics, techniques, and procedures that are unique to AI systems.
Framework like [MITRE ATLAS](https://atlas.mitre.org) can help to identify and mitigate these risks.

It is worth noting that the cybersecurity provisions of the AI Act interact with other legal frameworks, such as the EU Cyber Resilience Act (see below), which also impose requirements on the cybersecurity of software and hardware products.

<!-- Reference Links -->
[Containerization]: ../engineering-practice/containerization.md
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md

## Resources

!!! note
    According to |Art. 15(2)|, we can expect concrete guidance for the implementation of these requirements in the form of upcoming benchmarks and measurement methodologies.

- <a name="iso4213" />[ISO/IEC TS 4213:2022](https://www.iso.org/standard/79799.html):
    - provides a broad overview of statistical metrics suitable for various forms of classification problems.
    - The upcoming replacement, currently in its draft stage as [ISO/IEC AWI 4213](https://www.iso.org/standard/89455.html) broadens the scope to include measures of performance for classification, regression, clustering and recommendation tasks
- <a name="iso25058" />[ISO/IEC TS 25058:2024](https://www.iso.org/standard/89454.html) (_Guidance for quality evaluation of artificial intelligence (AI) systems_)
- <a name="iso24029" />[ISO/IEC TR 24029](https://www.iso.org/standard/77609.html) (_Artificial Intelligence (AI) — Assessment of the robustness of neural networks_)
- [Hamon, et al. (2020) - Robustness and Explainability of Artificial Intelligence, EUR 30040 EN, Publications Office of the European Union](https://publications.jrc.ec.europa.eu/repository/handle/JRC119336)
- [OWASP Machine Learning Security Top Ten](https://mltop10.info/)
- [MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems)](https://atlas.mitre.org)
- [Annex I of the EU Cyber Resilience Act](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847&qid=1747733433953#anx_I) list essential requirements for the cybersecurity of products with digital elements.
