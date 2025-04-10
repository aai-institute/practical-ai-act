---
hide:
- toc
---


# Cross-Reference: AI Act Articles to Engineering Practices and System Components


| Article                                                                            | Relevant Engineering Practices                                                | Relevant System Components                                            | Automation Feasibility                                                                                                          |
|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| **Art. 9**:<br>Risk Management System                                              |                                                                               |                                                                       | 🔴 Low<br>*Requires human judgment for risk assessment, <br>but frameworks can partially automate the process.*                 |
| **Art. 10**:<br>Data and Data Governance                                           |                                                                               |                                                                       | 🟢 High<br>*Data governance processes can be highly automated <br>with validation pipelines and quality checks.*                |
| **Art. 11**:<br>[Technical Documentation]                                          |                                                                               |                                                                       | 🟠 Medium<br>*Documentation generation can be partially automated, <br>but requires human input for context.*                   |
| **Art. 12**:<br>Record-Keeping                                                     | • [Inference Log]<br><br>• [Model Monitoring] | • [Inference Logging Service]<br><br>• [Post Deployment Monitoring] | 🟢 High<br>*Logging and record-keeping are highly automatable <br>through dedicated services.*                                  |
| **Art. 13**:<br>[Transparency and<br>Provision of Information<br>to the Deployers] | • [Explainability]                                                            |                                                                       | 🟠 Medium<br>*Automated generation of model cards and explanations <br>is feasible, but requires validation.*                   |
| **Art. 14**:<br>Human Oversight                                                    | • [Experiment Tracking]<br><br>• [Explainability]                             | • [Post Deployment Monitoring]<br><br>• [Model Registry and Tracking] | 🔴 Low<br>*Human oversight is, by definition, human-centered, <br>though tools can support the process.*                        |
| **Art. 15**:<br>Accuracy, Robustness<br>and Cybersecurity                          | • [Experiment Tracking]<br><br>• [Containerization]<br><br>• [Bias Mitigation] | • [Model Training Pipeline]<br><br>• [Model Registry and Tracking]    | 🟢 High<br>*Testing for accuracy and robustness can be largely automated, <br>but security requires human analysis.* |


<!-- Reference Links -->
[Inference Log]: ../engineering-practice/inference-log.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Containerization]: ../engineering-practice/containerization.md
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Inference Logging Service]: ../showcase/system-overview.md/#inference-logging-service
[Post Deployment Monitoring]: ../showcase/system-overview.md/#post-deployment-monitoring
[Model Registry and Tracking]: ../showcase/system-overview.md/#model-registry-and-tracking-mlflow
[Model Training Pipeline]: ../showcase/system-overview.md/#model-training-pipeline-dagster
[Technical Documentation]: technical-documentation.md
[Transparency and<br>Provision of Information<br>to the Deployers]: instructions-for-use.md
