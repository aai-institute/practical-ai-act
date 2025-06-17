# AI-Powered HR Assistant

!!! warning "Disclaimer"

    This is a **fictional use case** created solely for demonstration and educational purposes. It is not a real deployment and should not be interpreted as a commercial or operational system. It does not represent any real recruitment system or policy and should not be used for making real-world hiring decisions.

## Use Case: Salary Compatability Prediction for Recruitment

### Business Context

HR professionals in large organizations often face the challenge of managing a high volume of applications for a single job opening.
Many of these applicants are not considered suitable candidates for the role.
Clearly, an efficient screening process is needed to identify the most suitable candidates quickly.

This showcase presents a fictional HR Assistant system that demonstrates how AI can support this process while ensuring fairness, transparency, and compliance with regulations.
The system we describe uses a machine learning model to screen and filter candidates.
It predicts whether an applicant's expected (current) salary falls within a predefined salary range for a given job position.

The underlying assumption is that candidates whose expected current income falls outside the acceptable range for a given position are unlikely to be a good fit.
Essentially, the system treats expected current income compatibility as a proxy for a candidate's suitability for a given position.
However, note that this assumption is highly simplified and does not account for many real-world factors, such as career changes, relocation, or personal circumstances.
Therefore, it should not be used as the sole criterion for hiring decisions.

Recruiters can use this binary classification to quickly identify candidates who meet the salary expectations for a position, enabling them to focus on the most relevant applications.

Keep in mind that this approach is not suitable for actual use in hiring processes, as it may introduce biases and ethical concerns.
The system is intended for educational purposes only, by demonstrating how to develop a high-risk AI system under the EU AI Act by adhering to engineering best practices, including fairness, transparency, and explainability.

### Intended Purpose

The AI system is designed to:

-   **Predict salary compatibility** for job candidates based on their demographic and professional attributes
-   **Assist recruiters** by providing binary predictions on whether candidates' expected salaries align with position requirements
-   **Streamline applicant screening** by identifying applicants whose expected income falls within the acceptable range for a job position

The [risk classification](risk-classification.md) shows that a system like this is classified as a high-risk system under the EU AI Act.

The page on [risk assessment](risk-assessment.md) provides an abridged analysis of the potential risks posed by the system, and outlines mitigation strategies to address them.

### Core Capabilities

1. **Income Class Prediction**

    - Predicts whether a candidate's likely current income falls within a specified range
    - Uses multiple income band categories
    - Provides confidence scores for predictions

2. **Explainable Predictions**

    - SHAP-based explanations for individual predictions
    - Feature importance visualization
    - Transparency into which factors most influence the prediction

3. **API-Based Integration**

    - RESTful API for easy integration with existing HR systems
    - Batch prediction capabilities for processing multiple candidates

4. **Monitoring**
    - Continuous monitoring of model performance
    - Continuous monitoring of system operation

There is a detailed [overview](system-overview.md) of the system's architecture.

## Dataset: Public Use Microdata Sample (PUMS)

The model is trained on data from the **US Census Bureau**, specifically the 2022 version of the [Public Use Microdata Sample (PUMS)](https://www.census.gov/programs-surveys/acs/microdata/access.html) data. The data is accessed via
the software package [folktables](https://github.com/socialfoundations/folktables).

### Key Data Characteristics

-   **Source**: Official US government census data (publicly available)
-   **Time Period**: Recent annual data (updated yearly)
-   **Sample Size**: Approximately 1% of the US population

### Target Variable: Salary Range Compatibility

The model performs **binary classification** to predict whether an individual's income falls within a configurable salary range (e.g., <= $45,000).
This represents whether a candidate's expected salary is compatible with the position's salary band.

## Explore Further

-   [Risk Classification](risk-classification.md) - EU AI Act compliance analysis
-   [Risk Assessment](risk-assessment.md) - Detailed risk assessment report
-   [System Overview](system-overview.md) - High-level overview of the system architecture
-   [Code README](https://github.com/aai-institute/twai-pipeline/blob/main/README.md) - Setup and running instructions

**Resources**:

-   [PUMS Documentation](https://www.census.gov/programs-surveys/acs/microdata/access.html) - Official census documentation
-   [Retiring Adult: New Datasets for Fair Machine Learning](https://arxiv.org/pdf/2108.04884) - Discusses limitations of older datasets and introduces better alternatives (The research publication underlying the folktables package)
