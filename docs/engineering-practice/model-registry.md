# Model registry

!!! success "Compliance Info"

    --8<-- "docs/how-to/_compliance-info-box.partial"

    TODO: Add article references to provisions addressed by a model registry

## Motivation

After training, the resulting models are persisted to a preconfigured, often remote storage location, to make the raw models available for (internal) use.
Frequently, multiple versions of a given model are trained to assess the influence of certain parameters on the quality of the model outputs.
This, together with the requirement for reproducibility in many AI projects, necessitates a solution for managing multiple versions of models side-by-side, that is also highly available, reliable, and can be queried efficiently for any specific version.

## Implementation notes

Capabilities of a model registry can vary quite widely depending on how much of the stated responsibilities are handled by other tools in the practitioner's AI tool stack of choice.

In the simplest case, a model registry can just be a local or remote storage bucket, that keeps track of model metadata and versions by indexing them and storing the information in a database or similar systems.
If more responsibilities for the AI model lifecycle need to be handled, it is possible to use a tool that combines the storage of artifacts with their deployment, e.g. as a web application or a local assistant type of model.

Importantly, some model servers provide endpoints to query the underlying model registry for information on specific models and versions.
A noteworthy standardization of this is the [Open Inference Protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html), which specifies an API that model servers can support to allow the user of an AI model to query versions, health, and general metadata of models.

## Key Technologies

Since the task of versioning and storing models is tightly coupled to the training and tracking process itself, many experiment trackers (refer to the documentation on them [here](experiment-tracking.md)) come with a builtin model registry.
All of the experiment trackers listed in the mentioned documentation provide support for a model registry as well.

An example of a model server implementing the Open Inference Protocol is [MLServer by Seldon](https://mlserver.readthedocs.io/en/latest/), which offers supported for multi-model serving, batched requests, and parallel inference.
