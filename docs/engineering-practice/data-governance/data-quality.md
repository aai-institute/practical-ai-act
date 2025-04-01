---
tags:
    - phase::scoping
    - phase::data engineering
---

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    |Art. 10(2)(c)|: relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation

## Motivation

## Data Preprocessing

- Detect and Handle Missing or Incomplete Data
    -   Conduct data analysis to identify missing fields.
    -   Use statistical methods to assess if missing data skews results.
    -   Implement appropriate handling (e.g., interpolation, mean/mode imputation).

> |Art. 10(2)(c)| relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation;

The documentation of all data preparation is essential for traceability and transparency. See the point above on implementing data lineage.

Being specific and precise when documenting datasets is essential to minimize the risk of misinterpretation, both of the documentation itself and when using the data. A common approach to reduce ambiguity is to create a company-wide glossary that provides detailed definitions for terms. Datasets or fields linked to a glossary term should adhere strictly to the defined meaning, ensuring consistency and clarity.

## Data Quality Validation

**Ensuring Data is Error-Free**

-   Perform Data Consistency Checks
    -   Identify and remove duplicate records.
    -   Ensure data formats are consistent (e.g., all dates in correct format).
    -   Check for missing values and determine handling strategies (imputation or removal).

-   Validate Data Against Ground Truth
    -   Cross-check a sample of the dataset against verified real-world sources or domain experts.

-   Ensure Data Accuracy Through Automated Validation
    -   Implement automated scripts to check for:
        -   Logical inconsistencies (e.g., negative age values).
        -   Outliers and anomalies using statistical methods (e.g., z-score, IQR analysis).

-   Use Data Provenance and Source Verification
    -   Track and document the source of each dataset.
    -   Ensure it originates from reliable and ethical sources.

-   Monitor for Data Drift Over Time
    -   Set up periodic validation checks to see if the data distribution changes over time.
    -   Retrain models if significant drift is detected.

-   Human Review and Expert Validation
    -   Engage domain experts to review a portion of the dataset.
    -   Ensure labels and annotations reflect domain knowledge accurately.

> (h) the identification of relevant data gaps or shortcomings that prevent compliance with this Regulation, and how those gaps and shortcomings can be addressed.

Understand how gaps and shortcomings may lead to non-compliance. Define strategies to deal with gaps and shortcomings. Gaps and shortcomings being:

-   Data gaps: incomplete data sets, essential information missing.
-   Data shortcomings: Flaws in the data quality (errors or inconsistencies) or a biased data set.

Gaps and shortcoming may be addressed by further data collection, cleaning data, synthetic data generation.

> 4. Data sets shall take into account, to the extent required by the intended purpose, the characteristics or elements that are particular to the specific geographical, contextual, behavioral or functional setting within which the high-risk AI system is intended to be used.

See section above.

## Key Technologies

-   [Pandera](https://pandera.readthedocs.io/en/stable/), for data quality validation
-   [Great Expectations / GX Core](https://docs.greatexpectations.io/docs/core/introduction/), for data quality validation
