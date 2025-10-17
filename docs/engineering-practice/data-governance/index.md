# Data Governance

In general, data governance encompasses all methodologies for managing data throughout its entire lifecycle. With respect to the AI Act, |Article 10| mandates that datasets used in developing high-risk AI systems must be of high quality, relevant, representative, free from bias, and appropriately documented to ensure fairness, accuracy, and reliability. While the article outlines certain required practices, it lacks a comprehensive definition of data governance and data management.

To enhance implementation clarity, we distinguish between components suitable for automation (engineering practices, described in this section) and those centred on process and documentation, see [Technical Documentation](../../conformity/technical-documentation.md). This is not a strict partition: each paragraph of |Art. 10| can involve both kinds of tasks, so engineering and compliance teams need to collaborate closely.

## Topics in This Section

- [Data Versioning](data-versioning.md) — Maintain lineage, storage policies, and collaborative workflows so teams can trace the origin and suitability of every dataset revision.
- [Data Quality](data-quality.md) — Structure preprocessing, validation, and drift monitoring activities so data stays clean, complete, and representative throughout the lifecycle.
- [Documentation](documentation.md) — Produce and maintain datasheets, data cards, and other artefacts that capture purpose, sourcing, and limitations of the datasets in use.
- [Bias Mitigation](bias-mitigation.md) — Detect, analyse, and mitigate unwanted bias in data to protect fundamental rights and meet fairness obligations across deployments.
