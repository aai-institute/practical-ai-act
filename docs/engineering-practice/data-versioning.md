# Data versioning

!!! success "Compliance Info"

    --8<-- "docs/how-to/\_compliance-info-box.partial"

    TODO: Add article references to provisions addressed by data versioning

## Motivation

In fast-moving, complex environments such as the subject of AI, it is vital to keep track of where data and information originated,
not only to be transparent, or to easily share work with colleagues, but to be able to identify the root cause in the event of a problem with your system.

In the software engineering world, distributed version control systems (VCS) have seen wide adoption because they address all of these concerns.
Through a set of basic abstractions, they provide bookkeeping powers by means of unique and immutable references, distributed storage for work sharing, and a graph-based history building for detailed information keeping.
Consequently, _data version control_ or _data versioning_ systems (DVCS) can be thought of as the similar approach to all data _artifacts_ produced by your machine learning systems.

## Implementation notes

To add data versioning to a machine learning project, it is important to figure out a few steps:

1. **Collaborative development.**

A suitable data version control system needs to accommodate multiple engineers working simultaneously on different versions of the data, and ensure that changes made by one engineer do not invalidate the work of another.
This can be done for example by using a _branch_ workflow, where each person has their own siloed copy of the data, and can make changes to it without changing the canonical version (the "main" branch in this model).

```mermaid
%%{ init: {'theme': 'base'} }%%
---
title: Branching in a (data) version control system
---
gitGraph
   commit
   commit
   branch develop
   checkout develop
   commit
   commit
   checkout main
   merge develop
   commit
   commit
```

_Figure 1: A branching data version control approach, with commits (immutable snapshots of the data) shown as dots._

2. **Distributed storage.**

A data version control system should be accessible for all developers, and host the data in an off-device location to ensure easy access, fault tolerance, and availability of backups.

3. **Communication with users.**

In addition to availability, security, and fault tolerance, it is necessary that the data version control system can be easily interfaced with in AI application code.
This usually means that a selection of API clients or SDKs is available for a variety of programming languages, which allows developers to efficiently interface with the DVCS.

## Interoperability

-   Where applicable, ensure that datasets and documentation are interoperable with standard regulatory frameworks and can be audited by authorities.
    -   Standardize formats (e.g., CSV or Parquet files for tabular data)
    -   Centralize data storage (e.g., in a data lake or data warehouse) such that access to data sets can be given at any time, and it is not depending on data sets on local machines of ML Engineers and Data Scientists.

## Key technologies

1. [lakeFS](https://lakefs.io)

lakeFS models a lot of its version control abstractions like the [git VCS](https://git-scm.com/) tool.
It builds a linear history on commits, separates different avenues of work with branches, allows annotating data with tags, and also has supported for a merge workflow.
It can be set up on either local storage or a cloud storage bucket of one of the larger providers (AWS, GCP, Azure).

2. [DVC](https://dvc.org/)

DVC is a pure-Python command-line interface (CLI) for versioning data and model artifacts resulting from ML pipelines.
In addition, it has functionality for local experiment tracking, and versioning data pipelines in git together with project source code.

3. [git-lfs](https://git-lfs.com)

Git Large File Storage (LFS) stores large data assets in remote locations, and replaces the data with text pointers in git, so that data and its usage are decoupled on the storage level.
It integrates with the git command-line interface, augmenting developers' existing git workflows intuitively, and reducing the learning curve that an addition of a standalone tool would bring.
