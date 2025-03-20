# Inference Log

!!! success "Compliance Info"

    Implementing an inference log will help you in achieving compliance with the following regulations:

    - **|Art. 12|** (Record-Keeping)
    - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)

## Rationale

An inference log is a permanent record of all inferences made by the AI system, including the input and output data, the model used, and relevant additional metadata.

The inference log serves as the basis for monitoring the AI system's operation, ensuring that it behaves as intended and complies with legal and ethical requirements.
As such, it enables post-deployment monitoring activities, such as [model performance monitoring](model-monitoring.md).

## Key Technologies

-   Any database or storage solution that supports the required data structure
    -   Our reference architecture uses [PostgreSQL](https://www.postgresql.org/)
