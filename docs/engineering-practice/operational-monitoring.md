# Operational Monitoring

!!! success "Compliance Info"

    --8<-- "docs/engineering-practice/_compliance-info-box.partial"

    Implementing an operational metrics solution will help you in achieving compliance with the following requirements of the AI Act:

    TODO: Incomplete

    - **|Art. 15|** (Accuracy, Robustness and Cybersecurity), in particular:
        - **|Art. 15(4)|** Robustness, monitoring and alerting can help detect and mitigate potential robustness and availability issues
        - **|Art. 15(5)|** Cybersecurity, since monitoring is a crucial part of threat detection
    - **|Art. 26|** (Obligations of Deployers of High-Risk AI Systems), in particular:
        - **|Art. 26(5)|** (Monitoring of the AI system's operation by the deployer)
        - **|Art. 26(6)|** (Keeping of system logs by the deployer)

## Motivation

Besides [monitoring the performance](model-monitoring.md) of your machine learning models, it is also important to monitor the performance of the underlying technical infrastructure and services.
This includes monitoring the health of the servers, databases, and other components that support your machine learning applications.

These operational metrics can give an indication of the overall health of the system and can help you identify potential issues before they become critical.
This aligns with the AI Act obligations towards the robustness and cybersecurity of high-risk AI systems.

## Implementation Notes

Relevant metrics to monitor include:

-   **Resource usage**: CPU, GPU, memory, disk, network
-   **Service availability**: uptime, error rates
-   **Latency**: request/response times
-   **Throughput**: requests per second
-   **Custom metrics**: application-specific metrics (e.g., number of processed records, model inference times)

While it is a crucial part of an operational monitoring solution, this page does not cover the topic of alerting.
The following activities can provide a starting point to implement an alerting system:

-   Determining the thresholds for the metrics
-   Defining the escalation process for alerts
-   Setting up the alerting channels (e.g., email, Slack, PagerDuty)
-   Deploying and setting up the alerting system

## Key Technologies

### Metrics Collection and Visualization

-   [Prometheus](https://prometheus.io/), an time-series database for event and metrics collection, storage, monitoring, and alerting
    -   Many tools and frameworks can expose their operational metrics in the Prometheus format
-   [Grafana](https://grafana.com/oss/grafana/), an open-source analytics solution for visualization of metrics
-   The ELK (Elasticsearch, Logstash, Kibana) stack, in particular:
    -   [Elasticsearch](https://www.elastic.co/what-is/elasticsearch), a distributed search and analytics engine
    -   [Kibana](https://www.elastic.co/what-is/kibana), a data visualization and exploration tool for Elasticsearch

### Alerting

-   Prometheus [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/)
-   [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
