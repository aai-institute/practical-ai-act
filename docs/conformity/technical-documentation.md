# Technical Documentation

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - [Experiment Tracking]:
        - |Art. 11(1)| & |Annex IV(2)(g)|: Logging of validation process, in particular,
            characteristics of validation and test datasets
    - [Model Registry]:
        - |Art. 11(1)| & |Annex IV(2)(b)|: Logging the model architecture and hyperparameters makes it available for documentation
    - [Model Cards]:
        - |Art. 11(1)| & |Annex IV(1)(a,c,g)|: Documenting the model architecture, version and purpose, together with its user interface
    - [Data Documentation]:
        - |Art. 11(1)| & |Annex IV(2)(d,e)|: Creating datasheets to describe data characteristics, preprocessing, and refinement procedures

## Motivation

Providers of high-risk AI systems are required to prepare detailed technical documentation before placing the system on the market.
This documentation must be kept up to date and should demonstrate the system's compliance with the AI Act's requirements.
It should include a general description of the AI system, its intended purpose, design specifications, and information on performance evaluation.
Small and medium-sized enterprises (SMEs) may provide this information in a simplified form, as specified by the EU.

Thorough documentation can greatly improve users' and also practitioners' (i.e. deployers and implementers) understanding of the AI system, and thus make it easier to interact with the system, as well as diagnose any unexpected behavior that is observed during its operation.

On the engineering level, documentation can also be a powerful tool to make the evolution of an AI project (and software engineering projects in general) transparent, and to explain architectural and design decisions that, when studied, can be used to onboard new practitioners more quickly, and to re-evaluate central decisions during the project's lifecycle.

## Non-technical requirements

There are a number of important features of the AI system that need to be documented as per |Annex IV| of the AI Act.

Firstly, model metadata such as purpose, name of the provider, and versions of software used to run it need to be given (like a Software Bill of Materials or [SBOM](https://www.cisa.gov/sbom)).

Furthermore, the technical aspects of the system must be documented, like model architecture, algorithms used to train it, and human oversight measures to ensure safe operation in production.

There are many different ways of writing and distributing technical documentation.
In the most bare sense, documentation can be compiled into a single document, and shared with the relevant audiences as a single source of truth about the AI system.

On the other hand, it is often advantageous to host documentation on a website, giving access to features like full-text search, styling and text markup, easily accessible tables of contents and document sections, and shared access without having to distribute the documents by hand.

While not mandatory, documentation is also a suitable place to keep a record of engineering decisions made during the design and implementation of the AI system.
Commonly called architectural decision records or, in a less rigorous version, design documents, such records can serve as a red thread through the development history and lifecycle, and give transparency about the development process to implementers, and optionally users of the system.

## Annex IV: Technical Documentation Details

|Annex IV| provides a comprehensive list of elements that must be included in the technical documentation referred to in |Article 11|.
This includes detailed descriptions of the AI system's design specifications, algorithms, training data sets, risk management systems, validation and testing procedures, performance metrics, and cybersecurity measures.
The annex ensures that all relevant information is available to assess the system's compliance with the AI Act.

<!-- Reference Links -->
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Registry]: ../engineering-practice/model-registry.md
[Model Cards]: ../engineering-practice/model-cards.md
[Data Documentation]: ../engineering-practice/data-governance/documentation.md
[Explainability]: ../engineering-practice/explainability.md
