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

## Further Resources

The following pages provide more detailed information on the components of the reference architecture, grouped by the phase of the machine learning lifecycle.

### Training Phase

-   [Experiment Tracking](experiment-tracking.md)
-   [Model Registry](model-registry.md)
-   [Data Governance](data-governance/index.md)
    -   [Bias Mitigation](data-governance/bias-mitigation.md)
    -   [Data Versioning](data-governance/data-versioning.md)
    -   [Data Quality](data-governance/data-quality.md)
-   [Measuring Accuracy](accuracy.md)

### Deployment Phase

-   [Inference Log](inference-log.md)
-   [Model Explainability](explainability.md)
-   [Model Performance Monitoring](model-monitoring.md)
-   [Operational Monitoring](operational-monitoring.md)
-   [Containerization](containerization.md)
