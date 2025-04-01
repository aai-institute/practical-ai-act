# Data Governance

!!! success "Compliance Info"

    --8<-- "docs/how-to/\_compliance-info-box.partial"
    - **|Article 10|**



![](https://placehold.co/600x400?text=Data+Activities+in+the+ML+lifecycle)
In general, the term data governance describes the summation of all techniques
of managing data throughout its whole lifecycle. In regard to the AI Act,
|Article 10| mandates that datasets used in the development of high-risk AI systems must be of high quality, relevant, representative, free from bias, and appropriately documented to ensure fairness, accuracy, and reliability.

Although the article specifies certain practices that should be implemented, it does not provide a clear definition of data governance and data management. Furthermore, the listed items do not address the best practices (as practiced when implementing MLOps) for effective data governance and management.



> 2. Training, validation and testing data sets shall be subject to data governance and management practices appropriate for the intended purpose of the high-risk AI system.

It is important to highlight that the article requires practices to be tailored to the system's intended purpose. For instance, a high-risk AI system in healthcare would demand practices to safeguard patient privacy. Meanwhile, an AI system in finance would prioritize ensuring datasets are representative of diverse economic groups to prevent discriminatory outcomes.







Specific to bias. Refer to the page on [bias mitigation](bias-mitigation.md) for more information.



> 3. Training, validation and testing data sets shall be relevant, sufficiently representative, and to the best extent possible, free of errors and complete in view of the intended purpose. They shall have the appropriate statistical properties, including, where applicable, as regards the persons or groups of persons in relation to whom the high-risk AI system is intended to be used. Those characteristics of the data sets may be met at the level of individual data sets or at the level of a combination thereof.










<!-- TODO formulate this without citation, or remove?-->
> 6. For the development of high-risk AI systems not using techniques involving the training of AI models, paragraphs 2 to 5 apply only to the testing data sets.

This paragraph addresses high-risk AI systems that are developed without using techniques involving the training of AI models. These systems might rely on alternative approaches, such as rule-based systems, hard-coded algorithms, or pre-existing models that do not require additional training or updates to their parameters.


- [Data Versioning](data-versioning.md)
- [Data Quality](data-quality.md)
