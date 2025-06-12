# AI-Powered HR Assistant

!!! warning "Disclaimer"

    This is a **fictional use case** created solely for demonstration and educational purposes. It is not a real deployment and should not be interpreted as a commercial or operational system. It does not represent any real recruitment system or policy and should not be used for making real-world hiring decisions.

## Use Case: Salary Band Prediction for Recruitment

### Business Context

HR professionals in large organizations often face the challenge of managing a high volume of applications for a single job opening.
Many of these applicants are not considered suitable candidates for the role.
Clearly, an efficient screening process is needed to identify the most suitable candidates quickly.

This showcase presents a fictional HR Assistant system that demonstrates how AI can support this process while ensuring fairness, transparency, and compliance with regulations.
The system we describe uses a machine learning model to screen and filter candidates.
It predicts an applicant's expected (current) salary based on demographic and other attributes and matches them to predefined salary bands for a given job position.

The underlying assumption is that candidates whose expected current income is far above or below the range for a given position are unlikely to be a good fit.
Essentially, the system treats expected current income as a proxy for a candidate's suitability for a given position.
However, note that this assumption is highly simplified and does not account for many real-world factors, such as career changes, relocation, or personal circumstances.
Therefore, it should not be used as the sole criterion for hiring decisions.

Recruiters can use this categorization to quickly identify candidates who meet the salary expectations for a position, enabling them to focus on the most relevant applications.

Keep in mind that this approach is not suitable for actual use in hiring processes, as it may introduce biases and ethical concerns.
The system is intended for educational purposes only, by demonstrating how to develop a high-risk AI system under the EU AI Act by adhering to engineering best practices, including fairness, transparency, and explainability.

### Intended Purpose

The AI system is designed to:

-   **Predict (current) income** for job candidates based on their demographic and professional attributes
-   **Assist recruiters** by providing data-driven salary band recommendations
-   **Streamline applicant screening** by matching applicants to predefined salary bands for a job position

The [risk classification](risk-classification.md) shows that a system like this is classified as a high-risk system under the EU AI Act.

The page on [risk assessment](risk-assessment.md) provides an abridged analysis of the potential risks posed by the system, and outlines mitigation strategies to address them.

### Core Capabilities

1. **Income Class Prediction**

    - Predicts a candidate's likely current income
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

## Dataset: US Census Current Population Survey (CPS)

The model is trained on data from the **US Census Bureau's Current Population Survey**, specifically the 2024 version of the [Annual Social and Economic Supplement (ASEC)](https://www.census.gov/data/datasets/2024/demo/cps/cps-asec-2024.html) data.

### Key Data Characteristics

-   **Source**: Official US government census data (publicly available)
-   **Time Period**: Recent annual data (updated yearly)
-   **Sample Size**: Approximately 50,000 households

### Target Variable: Salary Bands

The model predicts configurable **salary bands** (e.g., <30K, 30-50K, 50-75K, 75-100K, >100K)
rather than exact salaries.

## Explore Further

-   [Risk Classification](risk-classification.md) - EU AI Act compliance analysis
-   [Risk Assessment](risk-assessment.md) - Detailed risk assessment report
-   [System Overview](system-overview.md) - High-level overview of the system architecture
-   [Code README](https://github.com/aai-institute/twai-pipeline/blob/main/README.md) - Setup and running instructions

**Resources**:

-   [CPS ASEC Documentation](https://www.census.gov/data/datasets/2024/demo/cps/cps-asec-2024.html) - Official census documentation
-   [Retiring Adult: New Datasets for Fair Machine Learning](https://arxiv.org/pdf/2108.04884) - Discusses limitations of older datasets and introduces better alternatives
