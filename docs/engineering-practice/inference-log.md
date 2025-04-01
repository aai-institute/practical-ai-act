# Inference Log

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    Implementing an inference log will help you in achieving compliance with the following regulations:

    - **|Art. 12|** (Record-Keeping), in particular:
        - **|Art. 12(1)|**, since the inference log enables the recording of events
        - **|Art. 12(2)|**, since the inference log allows the identification of potentially harmful situations and facilitates the post-market monitoring
    - **|Art. 19|** (Automatically Generated Logs)
    - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)
    - **|Art. 72|** (Post-Market Monitoring)

## Rationale

An inference log is a permanent record of all inferences made by the AI system, including the input and output data, the model used, and relevant additional metadata.

The inference log serves as the basis for monitoring the AI system's operation, ensuring that it behaves as intended and complies with legal and ethical requirements.
As such, it enables post-deployment monitoring activities, such as [model performance monitoring](model-monitoring.md).

Logging of inference data should allow for the reconstruction of the AI system's decision-making process, including the input data, the model used, and the output data.
This is essential for understanding the AI system's behavior and for identifying and addressing any issues that may arise.

## Implementation Notes

### Database Schema

The database schema for the inference log should include tables for storing the following information:

-   **Requests**: Information about the inference requests, including the input data, model used, and timestamp.
-   **Responses**: Information about the inference responses, including the output data and timestamp.
-   **Errors**: Information about any errors that occurred during inference, including the error message and the response data.
-   **Metadata**: Additional metadata about the inference requests and responses.

In order to allow for a variety of data types and structures, the input and output data should be stored as JSON or JSONB fields.
The data types from the standardized [_Open Inference Protocol v2 REST API specification_](https://github.com/kserve/open-inference-protocol/blob/main/specification/protocol/inference_rest.md) can be used as a reference for the structure of the input and output data.
Using a standardized data structure will make it easier to integrate the inference log with other components of the AI system, such as the [model performance monitoring](model-monitoring.md) component.

```mermaid
erDiagram
    REQUESTS {
        TEXT id PK
        TIMESTAMPTZ timestamp
        JSONB parameters
        JSONB inputs
        JSONB outputs
        JSONB raw_request
    }

    RESPONSES {
        TEXT id PK, FK
        TEXT model_name
        TEXT model_version
        TIMESTAMPTZ timestamp
        JSONB parameters
        JSONB outputs
        JSONB raw_response
    }

    ERRORS {
        TEXT id PK, FK
        TEXT error
        JSONB response
    }

    METADATA {
        TEXT id PK, FK
        JSONB metadata
    }

    REQUESTS ||--|| RESPONSES : "has"
    REQUESTS ||--|| ERRORS : "has"
    REQUESTS ||--|| METADATA : "has"
```

Choose a database or storage solution that supports the required data structure and provides the necessary performance and scalability characteristics for the AI system's workload.
Additionally, consider the data retention requirements of |Art. 19| and the need for data protection and privacy (e.g., interactions with GDPR) when selecting a log storage solution.

### Application Middleware

In order to ensure that all inference requests are automatically logged, the inference log should be implemented as a middleware component in the AI system's application code.

The middleware should intercept all incoming inference requests, log the relevant data, and then pass the request on to the model (inference server) for processing.

When using the FastAPI, the inference log can be injected as a _dependency_ into the application's route handlers or other dependencies.
By further encapsulating the interface to the model itself in another dependency, the inference log can be easily integrated into the application's request handling pipeline.

```mermaid
flowchart TD
    A[Route Handler] --> B[Model Inference Dependency] --> C[Inference Log Dependency]
```

## Key Technologies

-   Any database or storage solution that supports the required data structure
    -   The showcase implementation uses [PostgreSQL](https://www.postgresql.org/)
    -   Other choice include [ElasticSearch](https://www.elastic.co/elasticsearch/), [MongoDB](https://www.mongodb.com/), or [SQLite](https://www.sqlite.org/index.html)
-   [Open Inference Protocol specification](https://github.com/kserve/open-inference-protocol/), as a standardized data structure for the input and output data
-   [FastAPI](https://fastapi.tiangolo.com/) for building the AI system's application code
