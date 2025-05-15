---
tags:
    - Art. 10
    - Art. 11
    - Art. 13
    - Annex IV
---
# Data documentation

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    - **|Art. 10|** (Data and Data Governance), in particular:
        - |Art. 10(2)|, clear and structured documentation of data sets supports other data governance practices
    - **|Art. 11(1)|** in conjunction with **|Annex IV|** (Technical Documentation), in particular:
        - |Annex IV(2)(d)|, datasheets for training data sets are explicitly mentioned
        - |Annex IV(2)(g)|, validation and test data sets should be documented and characterized
    - **|Art. 13|** (Transparency and Provision of Information to Deployers), in particular:
        - |Art. 13(3)(b)(vi)|, training, validation, and test data sets should be appropriately documented

## Rationale

As part of the overall data governance strategy, data documentation is a key practice to ensure that data sets are well understood and properly managed.

This includes documenting the purpose of the data, its sources, curation method, its structure, and any transformations or processing that have been applied to it.
Consideration of limitations, potential biases, and ethical implications of the data is also important.

<!-- TODO: Relationship with data catalogs, mention those here if we choose to describe them elsewhere -->

## Implementation Notes

Most data documentation methodologies (see below) provide predefined templates or guidelines for documenting data sets, in order to ensure consistent application of these practices.

Data documentation should be treated as a living artifact, and as such should be versioned appropriately (e.g., using a version control system like Git).
Plain text formats like Markdown are well-suited for this purpose, as they are easy to read and edit, and can be easily converted to other formats (e.g., HTML or PDF) for publication.

## Key Technologies

Several approaches and formats exist for documenting data sets, including:

- _Datasheets for Datasets_, proposed in [Gebru, et al. (2021) - Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [_Data Cards_](https://sites.research.google/datacardsplaybook/), proposed in [Pushkarna, et al. (2022) - Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI](https://dl.acm.org/doi/fullHtml/10.1145/3531146.3533231)
- [_Data Statements_](https://techpolicylab.uw.edu/data-statements/)
- [_Dataset Nutrition Labels_](https://labelmaker.datanutrition.org/), proposed in [Holland, et al. (2018) - Data Nutrition Labels: A Framework to Drive Higher Data Quality Standards](https://arxiv.org/abs/1805.03677)

While these approaches differ in their concrete structure and content, they all aim to provide a comprehensive overview of the data set, including its purpose, sources, curation methods, and any limitations or ethical considerations, in line with the requirements for technical documentation in |Annex IV|.

## Resources

- Section on data-focused documentation tools in the Hugging Face [Landscape of ML Documentation Tools](https://huggingface.co/docs/hub/en/model-card-landscape-analysis#data-focused-documentation-tools), provides an overview of existing data documentation methodologies
