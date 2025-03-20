# Data versioning

!!! success "Compliance Info"
    TODO: Add article references to provisions addressed by data versioning

## Motivation

In fast-moving, complex environments such as the subject of AI, it is vital to keep track of where data and information originated,
not only to be transparent, or to easily share work with colleagues, but to be able to identify the root cause in the event of a problem with your system.

In the software engineering world, distributed version control systems (VCS) have seen wide adoption because they address all of these concerns.
Through a set of basic abstractions, they provide bookkeeping powers by means of unique and immutable references, distributed storage for work sharing, and a graph-based history building for detailed information keeping.
Consequently, *data version control* or *data versioning* can be thought of as the similar approach to all data *artifacts* produced by your machine learning systems.

## Key technologies

1. [lakeFS](https://lakefs.io)

lakeFS borrows a lot of its version control abstractions from the git VCS tool.
It builds a linear history on commits, separates different avenues of work with branches, allows annotating data with tags, and also has supported for a merge workflow.
For storage, it can always be used with a local machine file system, but it can also be set up on a cloud storage bucket of one of the larger providers (AWS, GCP, Azure).

lakeFS can ingest data via a command-line interface (CLI), ``lakectl``, or be addressed through one of its client libraries, most notably that in Python.
On top of that, an fsspec implementation (https://lakefs-spec.org) allows users to transfer files with minimal setup directly in Python code, and simplifies integration with data frame libraries and OLAP systems like duckDB.
