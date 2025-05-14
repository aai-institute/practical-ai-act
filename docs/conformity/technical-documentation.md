# Technical Documentation

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - [Experiment Tracking]:
        - |Art. 11(1)| & |Annex IV(2)(g)|: Logging of validation process, in particular,
            characteristics of validation and test datasets
    - [Model Registry]:
        - |Art. 11(1)| & |Annex IV(2)(b)|: Logging the model architecture and hyperparameters makes it available for documentation

## Motivation

Providers of high-risk AI systems are required to prepare detailed technical documentation before placing the system on the market.
This documentation must be kept up to date and should demonstrate the system's compliance with the AI Act's requirements.
It should include a general description of the AI system, its intended purpose, design specifications, and information on performance evaluation.
Small and medium-sized enterprises (SMEs) may provide this information in a simplified form, as specified by the EU.

Thorough documentation can greatly improve users' and also practitioners' (i.e. deployers and implementers) understanding of the AI system, and thus make it easier to interact with the system, as well as diagnosse any unexpected behavior that is observed during its operation.

On the engineering level, documentation can also be a powerful tool to make the evolution of an AI project (and software engineering projects in general) transparent, and to explain architectural and design decisions that, when studied, can be used to onboard new practitioners more quickly, and to re-evaluate central decisions during the project's lifecycle.

## Non-technical requirements

## Data Documentation

See also below, under "Dataset Information"


-   Data selection process
-   Quality improvement measures
-   Data owners
-   Description
-   Classification (applicable glossary terms)
-   Fields (name, type, description, classification) for tabular data
-   Data properties (e.g., format, resolution) for non-tabular data


> |Art. 10(2)(a)| the relevant design choices;

Any specific decisions made during the design and development of a high-risk AI system must be documented. Such decisions can include:

-   Architecture specific: These are choices related to the architecture, algorithms, data handling, and setup of the AI System. Depending on the architecture, different preprocessing techniques might need to be used.
-   Impact on performance: These choices influence how well the AI system performs. Techniques can be applied to increase accuracy, reliability, or to reduce bias.
-   Compliance-specific decisions: These choices are made to ensure compliance with laws and ethical guidelines. For example, anonymizing PIIs.

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

-   **Establish data lineage** (i.e., define upstream or downstream data sets) on data set level or on column level for tabular data.
    Before model training, data often undergoes various preprocessing steps. For example, datasets may be created by merging multiple datasets or combining different features. Simply documenting the final dataset is insufficient, as it does not allow the origin of the data to be traced. Proper documentation of data lineage is essential to maintain traceability and accountability.

    -   Define lineage in a data catalog, or have it automatically represented in a workflow/data orchestrator
        -   Keep records of the data lifecycle, including the sources of data, selection criteria, and preprocessing steps (all steps to model training).

> |Art. 10(2)(b)| data collection processes and the origin of data, and in the case of personal data, the original purpose of the data collection;

From the documentation, it shall be understood:

-   How the data is collected. Which methods and procedures where used to gather the data (survey, sensor, scraping, etc.)? Which conditions apply to the data collection (consent, regulatory compliance)? How does it align with best practices and ethical standards.
-   What is the source of the data? Is it publicly available, proprietary, collected from third parties (e.g., via an API)? What are the geographical, cultural, and demographic origins of the data?
-   To ensure compliance with the GDPR, personal data can only be collected for a specific purpose and cannot be repurposed.

-   Establish an organization-wide glossary index
    -   Define terms (including definition/description) and use those to annotate data set and fields in the data sets. Single source of truth for interpreting data sets and fields.

> |Art. 10(2)(c)| relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation;

The documentation of all data preparation is essential for traceability and transparency. See the point above on implementing data lineage.

Being specific and precise when documenting datasets is essential to minimize the risk of misinterpretation, both of the documentation itself and when using the data. A common approach to reduce ambiguity is to create a company-wide glossary that provides detailed definitions for terms. Datasets or fields linked to a glossary term should adhere strictly to the defined meaning, ensuring consistency and clarity.

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

## Model cards

A good **model card** is a structured document that provides clear, concise, and comprehensive information about a machine learning model:

- **Model Overview:**
    - **Model Name and Version**
    - **Model Description:** A brief overview of the model's purpose, capabilities, and intended use.
    - **Contact Information:** Details of the organization, department, team or individual responsible for the model, including contact information.
- **Intended Use:**
    - **Primary Use Cases:** Description of the specific tasks the model is designed for.
    - **Out-of-Scope Use Cases:** Explicitly state where the model should not be used
- **Dataset Information:**
    - **Training Data:** Details of the dataset used to train the model, including its source, size, and key characteristics.
    - **Validation and Test Data:** Information about datasets used for validation and testing (similar to training data).
    - **Preprocessing:** Description of any preprocessing steps applied to the data.
        - normalization, encoding, handling missing values, feature engineering, etc.
- **Performance Metrics:**
    - **Overall Performance:** See metrics for Accuracy
    - **Subgroup Performance:** Performance metrics broken down by demographic or contextual subgroups (e.g., age, gender, race, etc.).
    - **Benchmarks:** Comparison against other models (or older versions of the model)
- **Fairness and Bias Analysis:**
    - **Evaluation:** Results of bias testing across demographic groups, including fairness metrics used
    - **Mitigation:** Actions taken to address identified biases in the model or training data.
- **Limitations:**
    - **Known Limitations:** Description of scenarios where the model may not perform well or could produce unreliable results.
    - **Uncertainties:** Aspects of the model's behavior that are not well understood or tested.

- **Ethical Considerations:**
    - **Potential Harms:** Risks or harms that may arise from misuse or unintended use of the model.
    - **Privacy Concerns:** Details on how the model handles sensitive data, compliance with GDPR.
- **Risk Management:**
    - **Risk Assessment:** Identification of risks associated with the model and measures taken to mitigate them.
    - **Fail-Safes and Controls:** Mechanisms for monitoring and managing model outputs, including fallback procedures.
- **Technical Specifications:**
    - **Model Architecture:** A description of the underlying algorithm or architecture.
    - **Input and Output:** Details of the expected input formats and output types
    - **Dependencies:** Required software, libraries, or hardware for using the model.
- **Transparency and Explainability:**
    - **Explainability Techniques:** Methods used to make the model's decision-making interpretable (e.g., SHAP, LIME).
    - **Interpretation Guidelines:** Instructions for understanding and using model outputs responsibly.
- **Maintenance and Updates:🍏**
    - **Update Schedule:** Information about planned updates or retraining of the model.
    - **Changelog:** A log of changes made to the model, datasets, or documentation over time.
    - Use case dependent: what are example use cases? Can you group tasks?
- **Compliance Information:**
    - Regulatory Compliance: Statement of compliance with relevant regulations (e.g., the EU AI Act, GDPR)
    - Standards and Certifications: Details of standards followed (e.g., Code of Practice)
- **Usage Guidelines:**
    - **Installation and Deployment:** Steps for deploying and using the model in various environments.
    - **Monitoring and Evaluation:** Recommendations for ongoing performance monitoring and evaluation.
    - **Decommissioning:** Guidance for safely retiring the model when it's no longer in use. State when the model has to be decommissioned.
- **Licensing:**
    - **Usage License:** The terms under which the model can be used, modified, or distributed.
    - **Third-Party Content:** Attribution and licensing for any third-party datasets, libraries, or tools used.

## Annex IV: Technical Documentation Details

|Annex IV| provides a comprehensive list of elements that must be included in the technical documentation referred to in |Article 11|.
This includes detailed descriptions of the AI system's design specifications, algorithms, training data sets, risk management systems, validation and testing procedures, performance metrics, and cybersecurity measures.
The annex ensures that all relevant information is available to assess the system's compliance with the AI Act.


## Readings:
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [The Data Cards Playbook](https://sites.research.google/datacardsplaybook/)


<!-- Reference Links -->
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Registry]: ../engineering-practice/model-registry.md
[Explainability]: ../engineering-practice/explainability.md
