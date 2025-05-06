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

   - Raw data is ingested and version-controlled using lakeFS.
   - Processed data is also stored and versioned after preprocessing.
   - MLflow artifacts (e.g. model binaries) and raw files are stored in MinIO.

## Model Training Pipeline (Dagster)

   To express our model training strategy, we use the machine learning workflow or pipeline approach. This includes expressing the different steps (data sourcing, preprocessing, model training, ...) as tasks in a directed acyclic graph (DAG).
   In addition to this graph view, we get some more benefits from workflow orchestration, among them better observability (logging), scheduled jobs, caching steps and outputs, and a dashboard for powerful visualizations of pipeline runs.
   We each assume the data processing, model training, and serving/deployment to be independent workloads, leading to one pipeline for each of them.

   The data processing pipeline handles the following steps:

   - Data filtering
   - Feature engineering

   The model training pipeline contains the following steps:

   - Computing a train/test split
   - Automatic hyperparameter search
   - Logging experiment details (hyperparameters, metrics, models) to MLflow

   The serving pipeline contains these steps:

   - Versioning and packaging of deployments into Docker containers
   - Creating a scalable inference server for a model
   - Giving fairness information about a prediction
   - Logging predictions to analyze performance for data drift, degradations, and error rates.

## Model Registry and Tracking (MLflow)

   To get an overview on the performance of our trained models, and to keep track of our model artifacts in a registry, we use MLflow, an open-source experiment tracking platform.
   This provides us with out-of-the-box visualizations for our metrics of interest, as well as a central storage to retrieve model versions from. As mentioned above, MLflow storage is kept in MinIO.

   MLflow covers the following points of our ML experiment:

   - Accuracy & fairness metrics tracking
   - A central model artifact registry

## Deployment Infrastructure (Docker + MLServer)

   To deploy our models, we use a combination of Docker containers and MLServer, an open-source inference server with a REST/gRPC interface for deployed models.
   MLServer is, at the very basic level, a combination of runtime and server components, the former of which is a modular implementation of a model serving for a specific ML framework, like scikit-learn and xgboost.
   The server component contains functionality to host multiple versions of the same model kind, as well as the REST/gRPC interface implementing the V2 Inference Protocol.

   Additionally, it enables the followin features for our serving pipeline:

   - Trained models are packaged as Docker containers using MLServer-compatible images, and then deployed to a scalable inference endpoint, allowing real-time access for prediction.
   - The endpoint supports the output of SHAP values to indicate fairness evaluation of predictions (see below).

## Application Interface (FastAPI)

   Our ML models are exposed as a REST API built with FastAPI. By design, it is a middleware between the client and the aforementioned inference server, handling additional tasks around the inference request.
   Importantly, due to provisions in the AI Act, we need to log every request and response in a database. In addition to that, we provide an additional fairness assessment to explain the user how each feature contributes to their salary band prediction.

   The most important aspects of the API:

   - Accepting incoming candidate data for inference.
   - Sending data to the inference endpoint, either as a single or batch request.
   - Returning the predicted salary band and explanation of the prediction (i.e. top contributing features).

## Inference Logging Service

   Due to record-keeping provisions in the AI Act, we need to log inference requests and responses to ensure traceability and an overview of failures and errors throughout the system lifetime.
   In this example, all inference requests and responses are logged into an PostgreSQL database. This includes input features, output predictions, SHAP values explaining the output through feature contributions, and metadata.

## Post-deployment Monitoring

   After deployment, we use a cloud-native observation stack to keep track of model performance, data drift, and errors during serving operations.
   This stack consists of Grafana, Prometheus, and NannyML, where the former two are responsible for streaming logs and metrics, and for visualizing them, respectively.
   NannyML is our data drift detection tool of choice, allowing us to alert on triggers set to mark unacceptable performance losses.

   To summarize, below are the most important points of our post-deployment monitoring service:

   - NannyML monitors data drift, model degradation, and performance drops post-deployment by analyzing logs and inference data.
   - Prometheus collects operational metrics (e.g., latency, error rates, throughput).
   - Grafana displays these metrics in real time on an operational dashboard for observability.
