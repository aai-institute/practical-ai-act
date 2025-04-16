# Record-Keeping

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"
    - [Inference Log], logging inference events including corresponding meta information
            allows in particular for:
        - |Art. 12(2)(a)|: Identifying inputs, which cause an unwanted behavior of the system
        - |Art. 12(2)(b)|: Drift detection as a realization of a post-market monitoring
        - |Art. 12(2)(c)|: Monitoring of the AI system's operation
    - [Experiment Tracking]:
        - |Art. 12(2)(a)|: Backtracking to used training data
    - [Data Versioning]:
        - |Art. 12(2)(a)|: Identifying used datasets (training and reference data) by a unique identifier
    - [Orchestration]:
        - |Art. 12(2)(a)|: Reconstructing a complete model generation process through usage
            of a unique run id


<!-- Reference Links -->
[Inference Log]: ../engineering-practice/inference-log.md
[Data Versioning]: ../engineering-practice/data-governance/data-versioning.md
[Orchestration]: ../engineering-practice/orchestration.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
