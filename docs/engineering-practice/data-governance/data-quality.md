---
tags:
    - phase::scoping
    - phase::data engineering
---

!!! success "Compliance Info"

    --8<-- "docs/how-to/_compliance-info-box.partial"

    |Art. 10(2)(c)|: relevant data-preparation processing operations, such as annotation, labelling, cleaning, updating, enrichment and aggregation

## Data Collection

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

## Key Technologies

-   [Pandera](https://pandera.readthedocs.io/en/stable/), for data quality validation
-   [Great Expectations / GX Core](https://docs.greatexpectations.io/docs/core/introduction/), for data quality validation
