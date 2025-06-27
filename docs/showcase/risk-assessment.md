# Risk Assessment

This example of bias and discrimination risk is provided to give a first impression of what a risk analysis under |Article 9| might entail. It is **not** an exhaustive analysis in the sense of |Article 9|, which would require a comprehensive, systematic identification and assessment of all risks to health, safety, and fundamental rights throughout the AI system's lifecycle.

## Risk Assessment for Bias and Discrimination

### Risk Description

    - **Reasoning**: A classification model that predicts salary bands can inadvertently learn biased patterns from historical or non-representative data. If the training dataset underrepresents certain groups or if it carries historical inequalities, the model might systematically discriminate. This could result in unfair exclusion of qualified candidates from certain demographic or socioeconomic backgrounds.
    - **Mitigation Strategies**:
        1. **Data Quality and Diversity**: Ensure the dataset is representative of different demographic groups. Perform data audits to identify and remove or mitigate biases.
        2. **Bias Detection and Monitoring**: Use fairness metrics (e.g., disparate impact ratio, equalized odds) to assess and continually monitor the model’s outputs across different groups.
        3. **Fairness-Aware Algorithms**: Employ techniques such as reweighing or adversarial debiasing to reduce or eliminate learned biases.
        4. **Human Review**: Maintain a human-in-the-loop for critical decisions, ensuring that final filtering choices are not made solely by the AI.

!!! note "Disclaimer"

    The following fairness metrics and thresholds are provided as examples and should be adapted to the specific context of the AI system and its intended use. The choice of metrics and thresholds should be based on a thorough understanding of the potential risks and impacts of the AI system, as well as the legal and ethical requirements applicable to the system.

### Identification of Sensitive Attributes

As the showcase system deals with employment and recruitment, it is crucial to identify sensitive attributes that could lead to bias or discrimination in this context.

These attributes may include, but are not limited to:

-   Sex
-   Gender
-   Age
-   Race and/or ethnicity
-   Disability status

For the purpose of demonstration, the showcase will focus on **sex** as the sole sensitive attribute for the risk assessment.

### Appropriate Fairness Metrics and Thresholds

No single fairness metric can capture all aspects of fairness, and the choice of metrics should be context-specific. For this showcase, we will use the following metrics:

-   **Demographic Parity**/**Disparate Impact** ratio: This metric compares the selection rates of different groups. Assuming sex as the sensitive attribute, it measures whether the proportion of female and mal candidates selected for a job is similar.
-   **Equalized Odds**: This metric ensures that the true positive and false positive rates are equal across groups.

In the United States, the _Uniform Guidelines for Employee Selection Procedures_ (UGESP) provide a legal framework for evaluating fairness in federal employment practices.
Under UGESP, a selection rate for any group that is less than 80% of the rate for the group with the highest selection rate is considered _prima facie_ evidence of adverse impact (see [29 CFR Part 1607.4](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XIV/part-1607)).
This test is often referred to as the _80% rule_ or _four-fifths rule._

Although the use of this threshold is debated, it is a common practice in the United States and serves as a useful benchmark for assessing fairness in employment-related AI systems.
Therefore, the showcase will use the **80% rule as a threshold for demographic parity**:

<figure markdown>
```
0.8 <= demographic_parity_ratio <= 1.25
```
</figure>
