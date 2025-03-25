<style>
/* Hide the TOC sidebar to expand vertical space */
.md-sidebar--secondary {
  display: none !important;
}
</style>

<!-- Need to use embed instead of img to enable hyperlinks in the image -->

<embed src="/_images/reference-architecture.drawio.svg" id="svgFrame"
style="padding: 32px; width: 100%; box-sizing: border-box;"></embed>

<script>
// Open all local links in the top window (instead of the iframe/embed)
document.getElementById('svgFrame').addEventListener('load', function() {
    const iframe = this.getSVGDocument();
    // Need to match attribute name in all XML namespaces, since SVG <2 uses `xlink`
    const links = iframe.querySelectorAll('a[*|href^="/"]');
    links.forEach(link => link.setAttribute('target', '_top'));
});
</script>

## Further Resources

The following pages provide more detailed information on the components of the reference architecture, grouped by the phase of the machine learning lifecycle.

### Training Phase

-   [Data Versioning](data-versioning.md)
-   [Experiment Tracking](experiment-tracking.md)
-   [Model Registry](model-registry.md)

### Deployment Phase

-   [Inference Log](inference-log.md)
-   [Model Performance Monitoring](model-monitoring.md)
