---
tags:
    - Art. 15
hide:
    - tags # TODO: enable when ready
---

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    TODO: This list is incomplete

    - **|Art. 15|** (Accuracy, Robustness and Cybersecurity), in particular:
        - |Art. 15(1)|, containers provide a consistent and isolated runtime environment
        - |Art. 15(4)|, containers allow for redundant, reproducible and reliable application execution

## Motivation

Deploying and running applications in a reproducible and reliable manner is a crucial part of the software development lifecycle.
Inconsistencies in the runtime environment can lead to unexpected behavior, bugs, and security vulnerabilities.
AI systems prove no exception to this rule, as they often rely on complex dependencies and configurations that can vary across different runtime environments.

Containerization provides a solution to these challenges by encapsulating applications and their runtime dependencies into isolated environments, called _containers_.

By controlling the runtime environment, containerization can improve the _resilience_ of AI systems against inconsistencies, as required by |Art. 15(4)|.

Since containers provide a uniform execution model, [monitoring](operational-monitoring.md) their lifecycle and performance is easier.
Failed containers can be restarted automatically, and their logs can be collected and analyzed to identify potential issues, in line with the fault tolerance requirements of the AI Act.

Scaling of AI systems is also simplified with containerization, as containers can be easily replicated and distributed across multiple nodes.
This addresses the redundancy requirements of |Art. 15(4)|, as multiple instances of a containerized application can be run in parallel to ensure high availability and fault tolerance.

## Implementation Notes

### Applicability

Containerization can be applied at multiple stages of the machine learning lifecycle, including:

-   **MLOps infrastructure**: tooling for data versioning, model training, and deployment
-   **Data processing**: running data pipelines in isolated environments
-   **Model training**: training models in isolated environments
-   **Model serving**: deploying models as microservices

### Traceability and Reproducibility

Special care should be exercises to ensure the traceability and reproducibility of the containerized applications by always using versioned container images,
if possible with immutable version tags or [image digests](https://docs.docker.com/engine/containers/run/#image-digests) (e.g., `my-image:1.0.0` or even `my-image@sha256:...`, instead of `my-image:latest` or `my-image`).
This practice, akin to version locking for package dependencies, ensures that the same version of the container image is used for each deployment, reducing the risk of inconsistencies, especially in distributed environments.

Avoid updating existing tags when building container images, as this can lead to confusion and inconsistencies.

Similarly, container builds should be as _reproducible_ as possible.
The following techniques can help you to achieve this goal:

-   Use versioned base images, ideally pinning to a specific image digest.
-   Specify exact versions of dependencies (e.g., by using lock files or version constraints, if supported by your package manager).
-   Avoid using `latest` tags for dependencies, as they can lead to unexpected changes in behavior.
-   Use build arguments to parameterize the build process, if needed.
-   Use multi-stage builds to separate build and runtime dependencies, if applicable.
-   Use [labels](https://docs.docker.com/reference/dockerfile/#label)/[annotations](https://specs.opencontainers.org/image-spec/annotations/) to add metadata to the image, e.g., the source code revision identifier, build date, and maintainers (the [OpenContainers annotations spec](https://specs.opencontainers.org/image-spec/annotations/) provides guidance on predefined annotation keys).

### Security Considerations

While this document does not cover security aspects of containerization in detail, it is important to consider the following points:

-   Use minimal base images to reduce the attack surface.
-   Use container vulnerability scanning tools to identify known vulnerabilities in the base images and dependencies.
-   Regularly update base images and dependencies to patch known vulnerabilities.
-   Minimize runtime privileges by using non-root users and limiting container capabilities.

## Key Technologies

Container Engines:

-   [Docker](https://www.docker.com/)
-   [Podman](https://podman.io/)

Container Orchestration:

-   [Docker Compose](https://docs.docker.com/compose/) for small-scale deployments
-   [Kubernetes](https://kubernetes.io/) or [OpenShift](https://www.openshift.com/) for large-scale, multi-node deployments

### Container Security

!!! note

    This list only includes open-source software.

    The field of container security is rapidly evolving, and new tools and techniques are constantly being developed, also as part of commercial solutions.

-   [Snyk Open Source](https://snyk.io/product/open-source-security-management/)
-   [Clair](https://quay.github.io/clair/)
-   [Grype](https://github.com/anchore/grype/)
-   [Trivy](https://trivy.dev/latest/)
