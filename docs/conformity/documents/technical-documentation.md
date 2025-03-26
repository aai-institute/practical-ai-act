# Technical Documentation

- Article 11

Providers of high-risk AI systems are required to prepare detailed technical documentation before placing the system on the market. This documentation must be kept up to date and should demonstrate the system's compliance with the AI Act's requirements. It should include a general description of the AI system, its intended purpose, design specifications, and information on performance evaluation. Small and medium-sized enterprises (SMEs) may provide this information in a simplified form, as specified by the EU. 


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

Annex IV provides a comprehensive list of elements that must be included in the technical documentation referred to in Article 11. This includes detailed descriptions of the AI system's design specifications, algorithms, training data sets, risk management systems, validation and testing procedures, performance metrics, and cybersecurity measures. The annex ensures that all relevant information is available to assess the system's compliance with the AI Act.