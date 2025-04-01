# Data Governance

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"
    - **|Article 10|**



![](https://placehold.co/600x400?text=Data+Activities+in+the+ML+lifecycle)

In general, data governance encompasses all methodologies for managing data throughout its entire lifecycle. With respect to the AI Act, |Article 10| mandates that datasets used in developing high-risk AI systems must be of high quality, relevant, representative, free from bias, and appropriately documented to ensure fairness, accuracy, and reliability.
While the article outlines certain required practices, it lacks a comprehensive definition of data governance and data management.

To enhance implementation clarity, we distinguish between components suitable for automation (engineering practices, described in this section) and those centered on process and documentation,
see [Technical Documentation](../../conformity/documents/technical-documentation.md).
This is not a simple mapping of paragraphs to either or, moreover each paragraph
of |Art. 10| can include both types of tasks.






Specific to bias. Refer to the page on [bias mitigation](bias-mitigation.md) for more information.














<!-- TODO formulate this without citation, or remove?-->
> 6. For the development of high-risk AI systems not using techniques involving the training of AI models, paragraphs 2 to 5 apply only to the testing data sets.

This paragraph addresses high-risk AI systems that are developed without using techniques involving the training of AI models. These systems might rely on alternative approaches, such as rule-based systems, hard-coded algorithms, or pre-existing models that do not require additional training or updates to their parameters.


- [Data Versioning](data-versioning.md)
- [Data Quality](data-quality.md)
