---
tags:
    - Art. 10
---

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 10|** (Data and Data Governance), in particular:
        - **|Art. 10(2)(c)|**: Maintaining documented preprocessing routines for labelling, cleaning, imputation, and enrichment keeps every data preparation step traceable.
        - **|Art. 10(3)|**: Routine validation, reporting, and drift monitoring ensures training, validation, and test datasets remain complete, accurate, and representative.

## Motivation

|Art. 10(3)| of the AI Act demands a certain quality of data used for training and
evaluating models, in particular, these data sets should be:

-   relevant,
-   sufficiently representative
-   complete, and
-   free of errors.

To achieve those qualities, there are different techniques available at different steps in the system lifecycle.

## Implementation Notes

Note that the techniques discussed in the section focus on technical approaches for ensuring data quality.
They need to be accompanied by organizational and governance measures to become fully effective.

### Data Preprocessing

Preparing data for training begins with making each transformation explicit, measurable, and reproducible. This enables auditors to understand how raw inputs were converted into model-ready datasets.

#### Handle Missing or Incomplete Data
Profile the dataset to surface null or placeholder values, then quantify whether the missingness introduces bias. Choose remediation techniques—such as interpolation, mean/mode imputation, or domain-specific defaults—and [document](documentation.md) them so the same logic applies across training and evaluation runs.

#### Enforce Consistency and Schemas
Apply schema validation to tabular data to guarantee types, ranges, and required fields stay aligned across ingestion sources. Deduplicate records, normalize formats (for example, timestamps), and ensure foreign keys or categorical labels stay within expected vocabularies before the data enters downstream pipelines.

#### Keep Pipelines Reproducible
Automate preprocessing in versioned workflows instead of manual notebooks. Use a [workflow orchestrator](../orchestration.md) or data pipeline tool that tracks parameters, input snapshots, and code revisions so the same preprocessing steps can be replayed during audits or incident investigations.

### Data Quality Validation

Once preprocessing is locked down, validate that the resulting datasets remain faithful to reality and behave as expected over time.

#### Validate Against Ground Truth
Regularly sample records and compare them with verified business systems or domain experts. This check confirms that labelling, enrichment, and cleaning steps did not introduce errors and that sensitive attributes stay accurate.

#### Automate Accuracy Checks and Reporting
Run automated validation suites to catch logical conflicts—such as negative ages or impossible category combinations—and flag statistical outliers via z-score, interquartile range, or model-based anomaly detection. Summaries should flow into the regular data quality reports that analysts review and attach to the [data governance documentation](documentation.md) to keep stakeholders informed.

#### Monitor Drift and Trigger Remediation
[Monitor the model over time](../model-monitoring.md) and schedule periodic validation runs that compare live data against historical baselines. When the reports show significant drift in the data distribution, trigger investigation or retraining workflows.

## Key Technologies

-   [Pandas](https://pandas.pydata.org)
    -   Other dataframe libraries with similar features exist, e.g., [Polars](https://docs.pola.rs/), [Spark `DataFrame`s](https://spark.apache.org/docs/latest/sql-programming-guide.html)
-   [Pandera](https://pandera.readthedocs.io/en/stable/), for data quality validation
-   [Great Expectations / GX Core](https://docs.greatexpectations.io/docs/core/introduction/), for data quality validation
-   [Giskard](https://www.giskard.ai/products/open-source), an evaluation and testing framework for AI systems
