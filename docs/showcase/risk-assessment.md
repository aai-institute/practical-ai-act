# Risk Assessment

This example of bias and discrimination risk is provided to give a first impression of what a risk analysis under |Article 9| might entail. It is **not** an exhaustive analysis in the sense of |Article 9|, which would require a comprehensive, systematic identification and assessment of all risks to health, safety, and fundamental rights throughout the AI system's lifecycle.

!!! note "**Risk of Bias and Discrimination**"

    - **Reasoning**: A classification model that predicts salary bands can inadvertently learn biased patterns from historical or non-representative data. If the training dataset underrepresents certain groups or if it carries historical inequalities, the model might systematically discriminate. This could result in unfair exclusion of qualified candidates from certain demographic or socioeconomic backgrounds.
    - **Mitigation Strategies**:
        1. **Data Quality and Diversity**: Ensure the dataset is representative of different demographic groups. Perform data audits to identify and remove or mitigate biases.
        2. **Bias Detection and Monitoring**: Use fairness metrics (e.g., disparate impact ratio, equalized odds) to assess and continually monitor the model’s outputs across different groups.
        3. **Fairness-Aware Algorithms**: Employ techniques such as reweighing or adversarial debiasing to reduce or eliminate learned biases.
        4. **Human Review**: Maintain a human-in-the-loop for critical decisions, ensuring that final filtering choices are not made solely by the AI.

In this sense, the risk management system must be a living process that extends beyond initial risk identification. In particular, high-risk AI systems must undergo continuous testing throughout their lifecycle, with mandatory testing before productization and release to end users (see Sections (6) to (8)).

We highlight that the risk management system as presented in |Article 9| is not directly tied to, but in fact a requirement for a lot of the engineering practices showcased in this repository, since they require prior knowledge about the relevant risks of the project.
