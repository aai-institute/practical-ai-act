# AI-Powered HR Assistant

!!! warning "Disclaimer"
    This is a **fictional use case** created solely for demonstration and educational purposes. It is not a real deployment and should not be interpreted as a commercial or operational system. It does not represent any real recruitment system or policy and should not be used for making real-world hiring decisions.


## Use Case: Salary Band Prediction for Recruitment

### Business Context

In modern recruitment processes, determining appropriate salary bands for candidates is a critical but time-consuming task. Recruiters must consider multiple factors including education, experience, skills, and market conditions. This fictional HR Assistant demonstrates how AI could potentially support this process while maintaining fairness, transparency, and compliance with regulations.

### Intended Purpose

The AI system is designed to:

- **Predict salary bands** for job candidates based on their demographic and professional attributes
- **Assist recruiters** by providing data-driven salary band recommendations
- **Streamline initial screening** by automatically categorizing candidates into appropriate compensation ranges

The [risk classification](risk-classification.md) according to the EU AI Act shows that a system like this is classified as a high risk system.


## Core Capabilities

1. **Salary Band Classification**
     - Predicts a candidate's expected salary
     - Uses multiple salary band categories
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

- **Source**: Official US government census data (publicly available)
- **Time Period**: Recent annual data (updated yearly)
- **Sample Size**: Approximately 50,000 households


### Target Variable: Salary Bands

The model predicts configurable **salary bands** (e.g., <30K, 30-50K, 50-75K, 75-100K, >100K)
rather than exact salaries.


## Explore Further

- [System Architecture](system-overview.md) - Technical implementation details
- [Risk Classification](risk-classification.md) - EU AI Act compliance analysis
- [Code README](https://github.com/aai-institute/twai-pipeline/blob/main/README.md) - Setup and running instructions

**Resources**:

- [CPS ASEC Documentation](https://www.census.gov/data/datasets/2024/demo/cps/cps-asec-2024.html) - Official census documentation
- [Retiring Adult: New Datasets for Fair Machine Learning](https://arxiv.org/pdf/2108.04884) - Discusses limitations of older datasets and introduces better alternatives
