---
hide:
- toc
---


# Cross-Reference: AI Act Articles to Engineering Practices and System Components


| Article                                                                            | Relevant Engineering Practices                                                                                                                                                                                                                                                                    | Automation Feasibility                                                                                               |
|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| **Art. 9**:<br>[Risk Management System]                                            |                                                                                                                                                                                                                                                                                                   | 🔴 Low<br>*Requires human judgment for risk assessment, <br>but frameworks can partially automate the process.*      |
| **Art. 10**:<br>[Data and Data Governance]                                         | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;">          [Data Quality]</span><span style="flex: 1 1 45%;"> [Data Versioning]</span><span style="flex: 1 1 45%;"> [Bias Mitigation]</span></div>                                                            | 🟢 High<br>*Data governance processes can be highly automated <br>with validation pipelines and quality checks.*     |
| **Art. 11**:<br>[Technical Documentation]                                          | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;">      [Model Registry]  </span>                                                                                                                                                                              | 🟠 Medium<br>*Documentation generation can be partially automated, <br>but requires human input for context.*        |
| **Art. 12**:<br>[Record-Keeping]                                                   | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;">  [Inference Log]</span><span style="flex: 1 1 45%;"> [Data Versioning]  </span><span style="flex: 1 1 45%;"> [Experiment Tracking]  </span><span style="flex: 1 1 45%;"> [Orchestration]  </span>           | 🟢 High<br>*Logging and record-keeping are highly automatable <br>through dedicated services.*                       |
| **Art. 13**:<br>[Transparency and<br>Provision of Information<br>to the Deployers] | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;"> [Explainability]</span>                                                                                                                                                                                     | 🟠 Medium<br>*Automated generation of model cards and explanations <br>is feasible, but requires validation.*        |
| **Art. 14**:<br>[Human Oversight]                                                  | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;"> [Experiment Tracking]</span><span style="flex: 1 1 45%;"> [Explainability]</span><span style="flex: 1 1 45%;"> [Model Monitoring]</span><span style="flex: 1 1 45%;"> [Operational Monitoring]</span></div> | 🔴 Low<br>*Human oversight is, by definition, human-centered, <br>though tools can support the process.*             |br> [Operational Monitoring] | 🔴 Low<br>*Human oversight is, by definition, human-centered, <br>though tools can support the process.*                        |
| **Art. 15**:<br>[Accuracy, Robustness<br>and Cybersecurity]                        | <div style="display: flex; flex-wrap: wrap; gap: 20px;"><span style="flex: 1 1 45%;"> [Experiment Tracking]</span><span style="flex: 1 1 45%;"> [Containerization]</span><span style="flex: 1 1 45%;"> [Bias Mitigation]</span></div>                                                             | 🟢 High<br>*Testing for accuracy and robustness can be largely automated, <br>but security requires human analysis.* |



<!-- Reference Links -->
[Inference Log]: ../engineering-practice/inference-log.md
[Model Monitoring]: ../engineering-practice/model-monitoring.md
[Model Registry]: ../engineering-practice/model-registry.md
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Containerization]: ../engineering-practice/containerization.md
[Bias Mitigation]: ../engineering-practice/data-governance/bias-mitigation.md
[Data Quality]: ../engineering-practice/data-governance/data-quality.md
[Data Versioning]: ../engineering-practice/data-governance/data-versioning.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
[Orchestration]: ../engineering-practice/orchestration.md

[Technical Documentation]: technical-documentation.md
[Transparency and<br>Provision of Information<br>to the Deployers]: instructions-for-use.md
[Human Oversight]: human-oversight.md
[Data and Data Governance]: data-governance.md
[Record-Keeping]: record-keeping.md
[Accuracy, Robustness<br>and Cybersecurity]: accuracy-robustness-cybersecurity.md
[Risk Management System]: risk-management-system.md
