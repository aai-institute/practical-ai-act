!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    ...


> (f) examination in view of possible biases that are likely to affect the health and safety of persons, have a negative impact on fundamental rights or lead to discrimination prohibited under Union law, especially where data outputs influence inputs for future operations;
> (g) appropriate measures to detect, prevent and mitigate possible biases identified according to point (f);

-   Evaluate Bias & Fairness Considerations
    -   Conduct bias audits to ensure one group is not over- or underrepresented.

-   Implement measures to identify, monitor, and mitigate potential biases in datasets that could lead to discriminatory outcomes.

    -   **Conduct Exploratory Data Analysis (EDA):** Analyze the dataset for imbalances or patterns that may suggest bias, such as over-representation or under-representation of certain groups.
    -   **Fairness Metrics:** Use fairness metrics like demographic parity, equalized odds, and disparate impact to quantify bias in datasets and model outputs.

        -   **Demographic Parity (Statistical Parity):**
            Ensures that all groups have equal probabilities of receiving a positive outcome.

        $P(Outcome=Positive∣Group=A)=P(Outcome=Positive∣Group=B)$

        -   **Equalized Odds:**
            Requires equal true positive rates (TPRs) and false positive rates (FPRs) across groups.

        $P(Predicted Positive∣Actual Positive,Group=A)=P(Predicted Positive∣Actual Positive,Group=B)$

        -   **Disparate Impact:**
            Compares the ratio of favorable outcomes for different groups. Often used to detect discrimination.

        $Disparate Impact=P(Positive Outcome∣Group=B) / P(Positive Outcome∣Group=A)$

-   **Diversity Analysis:** Evaluate the dataset's demographic diversity, ensuring it represents all relevant populations appropriately.

    -   **Group Representation:**
        Checks whether groups are proportionally represented in the dataset (calculate as fraction of the total dataset size)
    -   **Overall Accuracy Equality:**
        Ensures that accuracy rates are equal across groups.

-   **Open-Source Tools:**

    -   IBM AI Fairness 360
    -   Microsoft's Fairlearn
    -   Google's What-If Tool

-   **Resampling Techniques:** Use oversampling (e.g., SMOTE) or undersampling to balance the representation of different demographic groups.

    -   `imblearn` package

-   Synthetic Data Generation: Generate synthetic examples for under-represented groups to ensure better balance in the dataset.

-   Reweighting: Adjust the weights of data instances to ensure fair representation across groups.

-   Bias-Corrected Features: Transform features to reduce correlations with sensitive attributes (e.g., gender, race).

-   Fair Representations: Use fairness-aware models that explicitly optimize for fairness metrics alongside predictive accuracy.
    -Learning Fair Representations (LFR): Produces a transformed dataset with minimal bias.

-   **Outcome Adjustments:** Adjust decision thresholds or outputs to ensure equitable outcomes across demographic groups.

    -   **Equalized Odds Postprocessing:** Modifies predictions to satisfy equalized odds constraints.

-   Bias Mitigation Strategies: Apply fairness postprocessing methods, such as calibration by group or equalized odds adjustments.

-   Regularly audit data to ensure it is free from systemic errors or biases.
    -   **Segmentation Analysis:** Partition the dataset based on sensitive attributes and assess performance metrics for each segment to detect disparities.
    -   **Subgroup Fairness Checks:** Compare outcomes for different demographic subgroups to identify discrepancies.
    -   **Drift Detection:** Use tools to detect data or model drift that may reintroduce bias over time.

## Freestyle

-   interpretation of AI Act regarding bias (referencing Annexes)
-   definition we use in the project and why
-   identifying possible biases
-   methods to detect bias
-   what we choose for this use-case and why

*   AI Act Article X
    -   Interpretation of Activity Y in Article X
    -   Definition of Activity Y in this project
    -   How is Activity Y relevant for this project
    -   Methods for Activity Y
    -   Selected methods and tools for Activity Y
    -   Findings

## Reading

From the book [Trustworthy Machine Learning](https://trustworthyml.io/)

-   Chapter 2.8 - 2.9 (and previous chapter as mentioned in the text)
