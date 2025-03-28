# Data Governance

![](https://placehold.co/600x400?text=Data+Activities+in+the+ML+lifecycle)

|Article 10| mandates that datasets used in the development of high-risk AI systems must be of high quality, relevant, representative, free from bias, and appropriately documented to ensure fairness, accuracy, and reliability.

The quality criteria for high-risk AI Systems as listed in sections 2 to 5 in |Article 10|.

> 2. Training, validation and testing data sets shall be subject to data governance and management practices appropriate for the intended purpose of the high-risk AI system.

It is important to highlight that the article requires practices to be tailored to the system's intended purpose. For instance, a high-risk AI system in healthcare would demand practices to safeguard patient privacy. Meanwhile, an AI system in finance would prioritize ensuring datasets are representative of diverse economic groups to prevent discriminatory outcomes.

Although the article specifies certain practices that should be implemented, it does not provide a clear definition of data governance and data management. Furthermore, the listed items do not address the best practices (as practiced when implementing MLOps) for effective data governance and management.


> |Art. 10(2)(b)| data collection processes and the origin of data, and in the case of personal data, the original purpose of the data collection;

From the documentation, it shall be understood:

-   How the data is collected. Which methods and procedures where used to gather the data (survey, sensor, scraping, etc.)? Which conditions apply to the data collection (consent, regulatory compliance)? How does it align with best practices and ethical standards.
-   What is the source of the data? Is it publicly available, proprietary, collected from third parties (e.g., via an API)? What are the geographical, cultural, and demographic origins of the data?
-   To ensure compliance with the GDPR, personal data can only be collected for a specific purpose and cannot be repurposed.

Before model training, data often undergoes various preprocessing steps. For example, datasets may be created by merging multiple datasets or combining different features. Simply documenting the final dataset is insufficient, as it does not allow the origin of the data to be traced. Proper documentation of data lineage is essential to maintain traceability and accountability.



> (d) the formulation of assumptions, in particular with respect to the information that the data are supposed to measure and represent;

The article mandates that any assumptions made are explicitly documented. The goal is to capture how the data aligns with the purpose of the AI system.

-   Understanding what the data represents: Identify and define specific concepts that the data is intended to measure. Especially important when data used as a proxy (e.g., income as a proxy for economic status).
-   Assumptions: Define the beliefs, whether they are implicit or explicit, about the dataset. This may include assumptions about the accuracy, scope, and relevance of the dataset.
-   Purpose alignment: Verify that the understanding (definitions) and the assumptions align with the intended use of the AI system.
-   Misinterpretation: Recognize and document any (potential) limitations (e.g., underrepresented classes).

> (e) an assessment of the availability, quantity and suitability of the data sets that are needed;

This assessment ensures that the data meets the quality standards such that it can be used.

-   Availability: Does the data exist? Is the data accessible (both technically and from the perspective of access rights)? Are there any practical, legal, or ethical restrictions that have to be resolved before accessing the data.
-   Quantity: Assess whether the dataset contains enough data points for training and validation. Is the data set large enough that is represents all relevant groups or scenarios (i.e., system boundaries)?
-   Suitability: Is the data representative of the target population and for the application/use? Is the data quality and accuracy fitting the goals of the AI System?

> (f) examination in view of possible biases that are likely to affect the health and safety of persons, have a negative impact on fundamental rights or lead to discrimination prohibited under Union law, especially where data outputs influence inputs for future operations;
> (g) appropriate measures to detect, prevent and mitigate possible biases identified according to point (f);

Specific to bias. Refer to the page on [bias mitigation](bias-mitigation.md) for more information.

> (h) the identification of relevant data gaps or shortcomings that prevent compliance with this Regulation, and how those gaps and shortcomings can be addressed.

Understand how gaps and shortcomings may lead to non-compliance. Define strategies to deal with gaps and shortcomings. Gaps and shortcomings being:

-   Data gaps: incomplete data sets, essential information missing.
-   Data shortcomings: Flaws in the data quality (errors or inconsistencies) or a biased data set.

Gaps and shortcoming may be addressed by further data collection, cleaning data, synthetic data generation.

> 3. Training, validation and testing data sets shall be relevant, sufficiently representative, and to the best extent possible, free of errors and complete in view of the intended purpose. They shall have the appropriate statistical properties, including, where applicable, as regards the persons or groups of persons in relation to whom the high-risk AI system is intended to be used. Those characteristics of the data sets may be met at the level of individual data sets or at the level of a combination thereof.

**Ensuring Data Relevance**

To ensure the dataset is relevant to the AI system's intended purpose, consider the following:

-   Clearly Define the AI System's Purpose

    -   What problem is the AI solving?
    -   Who are the end-users?
    -   What decisions will be influenced by the AI?

-   Specify Key Attributes & Variables

    -   Identify the critical features required for accurate predictions.
    -   Ensure the data captures the necessary demographic, contextual, or domain-specific factors.

-   Check for Domain Alignment

    -   Ensure the data is collected from sources that reflect the real-world environment of deployment.

-   Assess Temporal & Geographic Relevance

    -   Is the data up-to-date?
    -   Is it from the correct geographical region?

-   Validate Coverage of Target Population

    -   Ensure the dataset represents the groups the AI will serve.
    -   Avoid underrepresentation of critical demographics.

-   Assess Data Labeling and Context

    -   Verify if the labels or classifications align with domain expertise.
    -   Ensure human annotations are validated by experts where necessary.

-   Evaluate Bias & Fairness Considerations
    -   Conduct bias audits to ensure one group is not over- or underrepresented.


> 4. Data sets shall take into account, to the extent required by the intended purpose, the characteristics or elements that are particular to the specific geographical, contextual, behavioral or functional setting within which the high-risk AI system is intended to be used.

See section above.


<!-- TODO formulate this without citation, or remove?-->
> 6. For the development of high-risk AI systems not using techniques involving the training of AI models, paragraphs 2 to 5 apply only to the testing data sets.

This paragraph addresses high-risk AI systems that are developed without using techniques involving the training of AI models. These systems might rely on alternative approaches, such as rule-based systems, hard-coded algorithms, or pre-existing models that do not require additional training or updates to their parameters.


- [Data Versioning](data-versioning.md)
