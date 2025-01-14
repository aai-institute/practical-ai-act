# Data Governance

- Establish a **data management system**
    - Centralize data storage (e.g., in a Data Lake or Data Warehouse)
        - Implement access control and restrict access to data to authorized personal and systems only
        - Avoid storing data on developer machines. Provide discovery tooling. Provide centralized compute with high-speed data access.
    - Establish a organization-wide glossary index
        - Define terms (including definition/description) and use those to annotate data set and fields in the data sets. Single source of truth for interpreting data sets and fields.

- **Document data sources** (in a Data Catalog or in a Data Card):
    - Data selection process
    - Quality improvement measures
    - Data owners
    - Description
    - Classification (applicable glossary terms)
    - Fields (name, type, description, classification) for tabular data
    - Data properties (e.g., format, resolution) for non-tabular data

- **Establish data lineage** (i.e., define upstream or downstream data sets) on data set level or on column level for tabular data.
    - Define lineage in a data catalog, or have it automatically represented in a workflow/data orchestrator
        - Keep records of the data lifecycle, including the sources of data, selection criteria, and preprocessing steps (all steps to model training).


- **Data versioning:**
    - Automation:🍏
        - Version datasets on data processing pipelines
        - Generate logs on each update
        - Execute pipelines on data changes
    - Depending on the use case and data set properties:
        - Store complete versions (suitable for small data sets only)
        - Store increments (new image objects, new partitions in time series, etc)
        - Store differences (deltas) between data set versions
    - **Rule of thumb:** You should version data whenever changes to the dataset occur that could impact its use, reproducibility, or compatibility with downstream systems.
        - Initial data set creation
        - Data updates (new data, corrections, expansions)
        - Data processing: after applying preprocessing steps (evaluate based on compute vs. storage requirements)
        - Model training: maintain a version of the data for each trained model
        - Performance: after subsampling or aggregating
        - Experiments: when experimenting with different versions, including different features, etc.
        - Collaboration: track contributions per team/person
        - Decommissioning: store the last version of the data
        - Scheduled: hourly, daily, weekly, etc.
    - **Tools:** LakeFS, DVC, Delta Lake, Git LFS🍏
    - 🍏What would the user have to think about when choosing between them ( thinking about the methodlodies that define and separate them)