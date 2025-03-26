# Accuracy

This article requires that high-risk AI systems be designed to achieve appropriate levels of accuracy, robustness, and cybersecurity. Systems should perform consistently throughout their lifecycle, be resilient to errors and faults, and have measures in place to mitigate risks associated with cybersecurity threats. The accuracy of AI systems should be declared in their instructions, and systems should be designed to minimize risks of producing biased outputs.


# Continuous testing and benchmarking of models

- Regularly test datasets to validate their quality, accuracy, and relevance to the AI system's intended use.
    - **Data quality:**
        - **Missing Values Analysis:** Identify and handle missing or incomplete data using imputation, removal, or domain-specific methods.
        - **Outlier Detection:** Use statistical or machine learning techniques to detect and address outliers (e.g., Z-scores).
        - **Duplicate Records:** Regularly check for and remove duplicate entries to maintain dataset integrity.
        - **Noise Reduction:** Identify noisy or erroneous data points using heuristics, domain knowledge, or automated tools.
    - **Relevance:**
        - **Feature Relevance Analysis:** Perform feature selection or importance ranking to ensure all features contribute meaningfully to the AI model. (SHAP)
        - **Temporal Relevance:** Test datasets periodically to ensure they remain current and relevant (e.g., avoid outdated information).
    - **Drift detection:**
        - **Concept Drift:** Regularly test for shifts in the relationship between input features and target labels over time.
        - **Data Distribution Drift:** Monitor changes in feature distributions compared to baseline distributions
            - Kolmogorov-Smirnov test
            - Earth Mover’s Distance
- **Metrics:**
    - ***Regression:***
        - Mean Absolute Error (MAE)
        - Median Absolute Error (MedAE)
        - Mean Squared Error (MSE)
        - Root Mean Squared Error (RMSE)
        - R-Squared
    - ***Classification:***
        - Accuracy (Balanced accuracy)
        - Logarithmic Loss
        - Precision
        - Recall
        - F1-score
        - Area Under the ROC Curve (AUC-ROC)
- T**ools:**
    - Great Expectations, Pandas, Evidently AI, NannyML
- Ensure that datasets are updated as necessary to reflect current conditions or contexts.



## Reading
From the book [Trustworthy Machine Learning](https://trustworthyml.io/)
* Chapter 5.1