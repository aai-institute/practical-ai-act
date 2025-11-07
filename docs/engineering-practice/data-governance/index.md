# Data Governance

In general, data governance encompasses all methodologies for managing data throughout its entire lifecycle. With respect to the AI Act, |Article 10| mandates that datasets used in developing high-risk AI systems must be of high quality, relevant, representative, free from bias, and appropriately documented to ensure fairness, accuracy, and reliability. While the article outlines certain required practices, it lacks a comprehensive definition of data governance and data management.

To enhance implementation clarity, we distinguish between components suitable for automation (engineering practices, described in this section) and those centred on process and documentation, see [Technical Documentation](../../conformity/technical-documentation.md). This is not a strict partition: each paragraph of |Art. 10| can involve both kinds of tasks, so engineering and compliance teams need to collaborate closely.

## Topics in This Section

- [Data Versioning](data-versioning.md) — Track dataset lineage, record changes through branching or tagging, and control access so provenance and suitability remain transparent.
- [Data Quality](data-quality.md) — Run structured preprocessing, validation, reporting, and drift monitoring to keep datasets complete, accurate, and representative over time.
- [Documentation](documentation.md) — Maintain datasheets, data cards, and related records that describe sourcing, curation, and limitations for each dataset.
- [Bias Mitigation](bias-mitigation.md) — Analyse datasets for existing bias and apply mitigation techniques so models uphold fairness obligations and fundamental rights.
