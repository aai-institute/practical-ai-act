# Data and Data Governance

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"
    - [Bias Mitigation]:
        - |Art. 10(2)(g)|: Appropriate measures for bias detection, prevention, and mitigation
        - |Art. 10(3)|: Assert appropriate statistical properties regarding natural persons related to the use of the high-risk AI system
        - |Art. 10(5)|: Use of special categories of personal data in bias detection and correction
    - [Data Versioning]:
        - |Art. 10(2)(b)|: Tracking the origin of training and test data
        - |Art. 10(2)(e)|: Assessment of availability, quantity and suitability of the data sets
    - [Data Quality]:
        - |Art. 10(2)(c)|: Tracking data preparation steps like labelling, cleaning, imputation, enrichment;
        - |Art. 10(3)|: Ensuring complete, error-free, and sufficiently representative (for the respective application) training and testing data sets


## Non-technical requirements

Data governance measures serve two purposes in general in a high-risk AI use case: Transparency and accountability as well as quality assurance.
The former is important for ensuring that no systematic biases in the data influence the behavior of the AI system, and to ensure reproducibility to allow ML engineers to identify issues in the training and evaluation process.
The latter, meanwhile, is important to set up a rigorous performance evaluation ("benchmarking") process to ensure that an AI system performs as expected, and meets quality and safety standards.

_Datasheets_ can be used to document training methodologies, metadata and relevant features and characteristics of the used datasets,
as well as other non-technical aspects around the system such as the data provenance, how labels were obtained, and cleaning methods used.

In practice, an organizational focus on thorough data management pays dividends in other areas of the machine learning lifecycle as well.
Advantages of this include better awareness on different forms and versions of data, helping in crafting reproducible machine learning experiments, and higher availability of data assets to different teams, resulting in more efficient parallel workflows.

A point to remember is that since there are different aspects of data governance, this usually results in the adoption of one or more software tools to manage data.
In many cases, this means additional complexity in managing deployments, cloud operations, and/or higher staffing costs when employing personnel dedicated to managing data infrastructure.
It is therefore important to weigh the benefits of the chosen solution against its estimated complexity and costs, especially for smaller companies and teams.

## Relation to other Articles

Data governance is linked to the following articles:

- |Art. 12| (Record Keeping): For transparency on how high-risk AI systems perform in practice,
    and logging of events and input data over the course of the system's lifetime.
- |Annex IV| (Technical Documentation): To ensure the quality (especially correctness and completeness) of input data and to document engineering practices around the used data.

<!-- Reference Links -->
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Data Versioning]: ../engineering-practice/data-governance/data-versioning.md
[Data Quality]: ../engineering-practice/data-governance/data-quality.md
