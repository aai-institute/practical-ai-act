---
hide:
    - toc
---

<!-- Need to use embed instead of img to enable hyperlinks in the image -->

<embed src="../../_images/reference-architecture.drawio.svg" id="svgFrame"
style="padding: 32px; width: 100%; box-sizing: border-box;"></embed>

<script>
const canonicalRootLevel = 3;  // Number of path segments in the canonical URL to strip (need to account for trailing slash)
const urlParts = new URL(window.location.href);
const siteRoot = urlParts.pathname.split('/').slice(0, -canonicalRootLevel).join('/') + "/";
console.debug('siteRoot:', siteRoot);

// Open all local links in the top window (instead of the iframe/embed)
// and rewrite their targets based on the canonical URL of the current page
document.getElementById('svgFrame').addEventListener('load', function() {
    const iframe = this.getSVGDocument();
    // Need to match attribute name in all XML namespaces, since SVG <2 uses `xlink`
    const internalLinks = iframe.querySelectorAll('a[*|href^="/"]');
    internalLinks.forEach(link => {
        link.setAttribute('target', '_top')

        // Rewrite the link target relative to the site root
        const href = link.getAttribute('xlink:href');
        if (href !== null) {
            const newHref = href.replace(/^\//, siteRoot);
            console.log("Rewriting link:", href, "to", newHref);
            link.setAttribute('xlink:href', newHref);
        }
    });
});
</script>

# System Components

## Data Layer (lakeFS + MinIO)

   To keep track of data artifacts across the machine learning lifecycle, we use lakeFS, a distributed data version control solution.
   That way, we can clearly separate different versions of data, and annotate them with metadata and information, which helps to create a clear overview of the project.
   We choose to run lakeFS on top of MinIO, an S3-compatible object store, since that can also be used to store other artifacts than data, like trained models. 
   It can also be deployed locally, which means this example can be run self-contained without the need for cloud infrastructure.

   - Raw data is ingested and version-controlled using lakeFS.
   - Processed data is also stored and versioned after preprocessing.
   - MLflow artifacts (e.g. model binaries) and raw files are stored in MinIO.

## Model Training Pipeline (Dagster)

   We use a machine learning pipeline approach to orchestrate the different steps (data loading, preprocessing, model training, performance evaluation, ...) as tasks in a workflow.
   In addition to a graph view, we get some more benefits from workflow orchestration, among them better observability (logging), scheduled jobs, caching steps and outputs, and a dashboard for powerful visualizations of pipeline runs.
   We each assume the data processing, model training, and serving/deployment to be independent parts of the machine learning lifecycle, and model each of them as one pipeline.

   The showcase uses [Dagster](https://dagster.io/) as a workflow orchestration engine.
   Its focus on data assets makes it well suited for machine learning workflows.

   The data processing pipeline handles the following steps:

   - Data preprocessing and cleaning
   - Feature engineering

   The model training pipeline contains the following steps:

   - Computing a train/test split
   - Automatic hyperparameter search
   - Logging experiment details (hyperparameters, metrics, models) to MLflow

   The serving pipeline contains these steps:

   - Versioning and packaging of deployments into container images
   - Giving fairness information on the model
   - Preparing auxiliary models and datasets (using NannyML) to analyze performance for data drift, degradations, and error rates.

## Model Registry and Tracking (MLflow)

   To get an overview of all model training runs and their outcomes, we use MLflow, an open-source experiment tracking platform.
   It also allows us to keep track of our model artifacts in a versioned registry, providing a direct link between runs and their resulting models.
   In this showcase, MLflow uses MinIO for persistent storage of artifacts.

   MLflow covers the following concerns:

   - Tracking of:
     - Training environment
     - Model (hyper-)parameters
     - Accuracy & fairness metrics
   - A central model artifact registry

## Deployment Infrastructure (Docker + MLServer)

   To deploy our models we use container images with MLserver, an open-source machine learning inference server with standardized REST/gRPC APIs.
   MLServer is, at the very basic level, a combination of runtime and server components, the former of which is a modular implementation of a model serving for a specific ML framework, like scikit-learn and xgboost.
   The server component contains functionality to host multiple versions of the same model kind, as well as the REST/gRPC interface implementing the Open Inference Protocol.

   Additionally, it enables the following features for our serving pipeline:

   - Creating a scalable inference server for a model.
   - Trained models are packaged as container images and then deployed to provide a scalable inference endpoint, allowing real-time access for prediction.
   - The endpoint supports the output of SHAP values to indicate fairness evaluation of predictions through a custom MLserver runtime (see below).

## Business application (FastAPI)

   The business logic of the HR assistant system in the showcase is implemented as a REST API service built with FastAPI.
   In order to make predictions, this service calls the aforementioned inference server, and handles additional tasks around the inference request:
   In order to fulfill the record-keeping requirements of the AI Act, all inference requests and responses are logged to a database (see below).
   In addition to that, the FastAPI application provides functionality to explain any of its decisions to the user, by showing how each feature of the input data contributes to their predicted salary band.
   This supports the right to explanation of the system's decision making as required by the AI Act for certain classes of AI systems.

   The most important aspects of the API:

   - Accepting incoming candidate data for inference.
   - Sending data to the inference endpoint, either as a single or batch request.
   - Returning the predicted salary band and explanation of the prediction (i.e. top contributing features).

## Inference Logging

   Due to record-keeping provisions in the AI Act, the system logs all inference requests and responses to ensure traceability and an overview of failures and errors throughout its lifetime.
   In this example, all inference requests and responses are logged into an PostgreSQL database.
   This includes input features, output predictions, SHAP values explaining the output through feature contributions, and metadata.
   This inference log also serves a secondary purpose by enabling post-deployment monitoring, as described in the next section.

## Post-deployment Monitoring

   After deployment, we use an observability tool stack to keep track of model performance, data drift, and operational metrics like HTTP errors or request latencies.
   This stack consists of Grafana, Prometheus, and NannyML, where the former two are responsible for streaming logs and metrics, and for visualizing them, respectively.
   NannyML is our data drift detection and model performance estimation tool of choice, allowing us to alert on triggers set to mark unacceptable performance losses.

   To summarize, below are the most important points of our post-deployment monitoring service:

   - NannyML monitors data drift, model degradation, and performance drops post-deployment by analyzing logs and inference data.
   - Prometheus collects operational metrics (e.g., latency, error rates, throughput).
   - Grafana displays these metrics in real time on an operational dashboard for observability.
