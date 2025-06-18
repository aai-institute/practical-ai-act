---
hide:
    - toc
---

# Cross-Reference: AI Act Articles to Engineering Practices and System Components

<!-- List of practices is wrapped automatically through CSS, no need for manual formatting -->

<!-- TODO: Remove the Automation Feasibility column, as it is highly subjective and not further elaborated -->

/// html | div.conformity-table

| Article                                                                        | Relevant Engineering Practices                                                                                                     |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **Art. 9**:<br>[Risk Management System][]                                      |                                                                                                                                    |
| **Art. 10**:<br>[Data and Data Governance][]                                   | [Data Quality][] [Data Versioning][] [Bias Mitigation][]                                                                           |
| **Art. 11**:<br>[Technical Documentation][]                                    | [Model Registry][] [Experiment Tracking][] [Explainability][]                                                                      |
| **Art. 12**:<br>[Record-Keeping][]                                             | [Inference Log][] [Data Versioning][] [Experiment Tracking][] [Orchestration][]                                                    |
| **Art. 13**:<br>[Transparency and Provision of Information to the Deployers][] | [Explainability][] [Experiment Tracking][] [Model Registry][] [Operational Monitoring][]                                           |
| **Art. 14**:<br>[Human Oversight][]                                            | [Experiment Tracking][] [Explainability][] [Model Monitoring][] [Operational Monitoring][]                                         |
| **Art. 15**:<br>[Accuracy, Robustness and Cybersecurity][]                     | [Experiment Tracking][] [Containerization][] [Bias Mitigation][] [Model Monitoring][] [Operational Monitoring][] [Model Serving][] |

///

<!-- Reference Links -->

[Inference Log]: ../engineering-practice/inference-log.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Model Registry]: ../engineering-practice/model-registry.md
[Model Serving]: ../engineering-practice/model-serving.md
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Containerization]: ../engineering-practice/containerization.md
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Data Quality]: ../engineering-practice/data-governance/data-quality.md
[Data Versioning]: ../engineering-practice/data-governance/data-versioning.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
[Orchestration]: ../engineering-practice/orchestration.md
[Technical Documentation]: technical-documentation.md
[Transparency and Provision of Information to the Deployers]: instructions-for-use.md
[Human Oversight]: human-oversight.md
[Data and Data Governance]: data-governance.md
[Record-Keeping]: record-keeping.md
[Accuracy, Robustness and Cybersecurity]: accuracy-robustness-cybersecurity.md
[Risk Management System]: risk-management-system.md
