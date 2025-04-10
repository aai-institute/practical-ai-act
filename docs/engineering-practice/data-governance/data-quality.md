---
tags:
    - phase::scoping
    - phase::data engineering
---

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 10|** (Data and Data Governance), in particular:
        - **|Art. 10(2)(c)|**
        - **|Art. 10(3)|**

## Motivation

|Art. 10(3)| of the AI Act demands a certain quality of data used for training and
evaluating models, in particular these data sets should be:

- relevant,
- sufficiently representative
- complete, and
- free of errors.

To achieve those qualities, there are different techniques available at different steps in the system lifecycle.

## Implementation Notes

Note that the techniques discussed in the section focus on technical approaches for ensuring data quality.
They need to be accompanied by organizational and governance measures to become fully effective.

### Data Preprocessing

-   Detect and handle missing or incomplete data
    -   Conduct data analysis to identify missing fields.
    -   Use statistical methods to assess if missing data skews results.
    -   Implement appropriate handling (e.g., interpolation, mean/mode imputation).
-   Perform data consistency checks
    -   Enforce data schema for tabular data.
    -   Identify and remove duplicate records.
    -   Ensure data formats are consistent (e.g., all dates in correct format).
    -   Check for missing values and determine handling strategies (imputation or removal).
-   Keep preprocessing consistent, versioned and reproducible
    -   Avoid manual processing steps, rely on data pipelines in a [workflow orchestrator](../orchestration.md) instead

### Data Quality Validation

-   Validate data against ground truth
    -   Cross-check a sample of the dataset against verified real-world sources or domain experts.
-   Ensure data accuracy through automated validation
    -   Logical inconsistencies (e.g., negative age values).
    -   Outliers and anomalies using statistical methods (e.g., z-score, IQR analysis).
-   Produce automated data quality reports for human review and inclusion in [technical documentation](../../conformity/technical-documentation.md).
-   [Monitor for data drift over time](../model-monitoring.md)
    -   Set up periodic validation checks to see if the data distribution changes over time.
    -   Retrain models if significant drift is detected.

## Key Technologies

- [Pandas](https://pandas.pydata.org)
    - Other dataframe libraries with similar features exist, e.g., [Polars](https://docs.pola.rs/), [Spark `DataFrame`s](https://spark.apache.org/docs/latest/sql-programming-guide.html)
-   [Pandera](https://pandera.readthedocs.io/en/stable/), for data quality validation
-   [Great Expectations / GX Core](https://docs.greatexpectations.io/docs/core/introduction/), for data quality validation
