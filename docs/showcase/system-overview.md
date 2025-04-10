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
   - Raw Data is ingested and version-controlled using lakeFS
   - Processed Data is also stored and versioned after preprocessing.
   - MLflow Artifacts (e.g. model binaries) and raw files are stored in MinIO, an S3-compatible object store.

## Model Training Pipeline (Dagster)
   - The data processing pipeline handles:
     - Data filtering
     - Feature engineering

   - The model training pipeline:
     - train, test split
     - automatic hyperparameter search
     - logs experiment details (hyperparameters, metrics, models) to MLflow

## Model Registry and Tracking (MLflow)
   - accuracy metrics tracking
   - fairness metrics tracking
   - model artifact registry

## Deployment Infrastructure (Docker + MLServer)
   - Trained models are packaged as Docker containers using MLServer-compatible images.
     These are deployed to a scalable inference endpoint, allowing real-time access for prediction.
   - The endpoint supports the output of SHAP values

## Application Interface (FastAPI)
   - The application is exposed via a REST API built with FastAPI.
   - Accepts incoming candidate data.
   - Sends data to the inference endpoint.
   - Returns predicted salary band and Explanation of prediction (top contributing features)

## Inference Logging Service
   - All inference requests and responses are logged into an PostgreSQL database.
   - Stored data includes:
     - input features
     - model outputs:
       - prediction
       - probabilities
       - SHAP explanations
     - Inference timestamps
     - event id
     - model meta information

## Post-deployment Monitoring

   - NannyML monitors data drift, model degradation, and performance drops post-deployment by analyzing logs and inference data.
   - Prometheus collects operational metrics (e.g., latency, error rates, throughput).
   - Grafana displays these metrics in real time on an operational dashboard for observability.
