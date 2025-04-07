The aim of the section is to give an overview about the (fictitious) use-case,
we employ for demonstration. This AI system is designed to assist recruiters and hiring
managers in the recruitment process by automatically predicting salary bands
for job candidates, so helping to streamline candidate filtering and matching.



# Data
- [Census data](https://www2.census.gov/programs-surveys/cps/datasets/)

## Risk Classification Under the EU AI Act

- **Determine if the system is considered AI under the EU AI Act (see Article 2)**
    - **Reasoning**: The system uses machine learning methods (a classification model) to estimate candidates’ likely income. Machine learning is explicitly covered by the definition of AI in the EU AI Act.
    - **Outcome**: Yes, this system is within scope because it qualifies as an AI system.
- **Check whether the AI system falls under any excluded or exempted categories**
    - **Reasoning**: Some AI systems, such as research prototypes, are excluded from the regulatory requirements. This recruitment system is a commercial application used by recruiters and hiring managers, so it does not qualify for exemption.
    - **Outcome**: The system is not exempt; it is still in scope.
- **Determine if the AI system poses an ‘unacceptable risk’**
    - **Reasoning**: Under Article 5 of the EU AI Act, ‘unacceptable risk’ systems typically involve manipulative or exploitative practices, social scoring, or contraventions of fundamental rights. A recruitment filter based on estimated salary ranges does not constitute a form of social scoring or manipulative practice aimed at harming individuals.
    - **Outcome**: The system is not considered ‘unacceptable risk.’
- **Assess whether the AI system is considered ‘high risk’**
    - **Reasoning**: The EU AI Act (in Annex III, point 4) lists AI systems used in the employment and management of workers (e.g., for recruitment or selection) as high risk. This system directly assists with filtering and selecting candidates for roles, thereby influencing employment opportunities.
    - **Outcome**: The system falls under the ‘high risk’ category.
- **If not high risk, classify as ‘limited’ or ‘minimal risk’**
    - **Reasoning**: Since we have already determined it is high risk due to its recruitment use case, there is no need to downgrade to ‘limited’ or ‘minimal risk.’
    - **Outcome**: Classification remains ‘high risk.’

**Final Outcome**

Based on the criteria outlined in the EU AI Act, the proposed recruitment AI system qualifies as a high-risk system. Although it does not engage in manipulative practices or social scoring that would render it unacceptable, it does fall squarely under the employment-related use cases the EU AI Act classifies as high risk. Consequently, the system will be subject to additional legal and compliance obligations (once the EU AI Act is in force), including risk management, data governance, documentation and traceability, transparency requirements, and human oversight.


## Risk Assessment

### **Risk of Bias and Discrimination**

- **Reasoning**: A classification model that predicts salary bands can inadvertently learn biased patterns from historical or non-representative data. If the training dataset underrepresents certain groups or if it carries historical inequalities, the model might systematically discriminate. This could result in unfair exclusion of qualified candidates from certain demographic or socioeconomic backgrounds.
- **Mitigation Strategies**:
    1. **Data Quality and Diversity**: Ensure the dataset is representative of different demographic groups. Perform data audits to identify and remove or mitigate biases.
    2. **Bias Detection and Monitoring**: Use fairness metrics (e.g., disparate impact ratio, equalized odds) to assess and continually monitor the model’s outputs across different groups.
    3. **Fairness-Aware Algorithms**: Employ techniques such as reweighing or adversarial debiasing to reduce or eliminate learned biases.
    4. **Human Review**: Maintain a human-in-the-loop for critical decisions, ensuring that final filtering choices are not made solely by the AI.

### 2. **Transparency and Explainability**

- **Reasoning**: Users (recruiters, hiring managers) and candidates may not understand why certain salary band predictions are made, raising concerns about opaque or “black-box” decision-making. Under the AI Act, high-risk systems are required to provide clear information about how decisions are reached.
- **Mitigation Strategies**:
    1. **Explainable AI Techniques**: Implement model-agnostic explainability tools such as LIME or SHAP to show which features significantly influenced the classification.
    2. **User-Friendly Explanations**: Provide recruiters with straightforward explanations or scoring breakdowns to facilitate oversight and accountability.
    3. **Documentation and Transparency**: Maintain proper documentation on data sources, model training methodologies, and known limitations, and make this documentation available to relevant stakeholders.

### 3. **Accuracy and Reliability**

- **Reasoning**: Inaccurate classification could prevent qualified candidates from advancing, or it might lead to oversights in filtering out those misaligned with salary expectations. Ensuring the system’s reliability is crucial to protect both the employer’s interests and the candidate’s opportunities.
- **Mitigation Strategies**:
    1. **Robust Model Validation**: Use cross-validation, hold-out tests, and performance benchmarking to ensure the model is consistently accurate across various subpopulations and roles.
    2. **Continuous Learning and Updates**: Periodically retrain and update the model to reflect market changes, salary trends, and evolving job roles.
    3. **Fallback Procedures**: If the system’s confidence in a candidate’s classification is below a certain threshold, trigger a human review rather than an automatic rejection.

### 4. **Overreliance on Automation**

- **Reasoning**: There is a risk that recruiters might rely too heavily on automated filters and fail to exercise human judgment or contextual understanding. This could further marginalize candidates who do not fit the typical patterns learned by the AI.
- **Mitigation Strategies**:
    1. **Human-in-the-Loop**: Ensure the final decision is made or reviewed by a human, with the AI acting as a supportive tool.
    2. **Defined Escalation Paths**: Create processes that allow candidates to challenge or appeal decisions, or for recruiters to spot-check questionable outcomes.
    3. **Training for Recruiters**: Provide guidance and training so that hiring managers understand the AI’s limitations and know when to override its recommendations.

### 5. **Data Privacy and Governance**

- **Reasoning**: Because the model uses personal data (e.g., job history, educational background) to infer salary bands, it must comply with GDPR and the EU AI Act’s provisions on data governance.
- **Mitigation Strategies**:
    1. **Data Minimization and Purpose Limitation**: Collect and process only the data necessary for salary classification, and clearly define the scope.
    2. **Consent and Transparency**: Inform candidates about how their data will be used and processed, ensuring clear consent where appropriate.
    3. **Secure Infrastructure and Protocols**: Implement strong data encryption, secure data storage, and controlled data access.
    4. **Regular Audits**: Conduct data protection impact assessments (DPIAs) and AI audits to ensure ongoing compliance.

### 6. **Risk of Exclusion and Reduced Opportunities**

- **Reasoning**: Automated filtering could inadvertently exclude individuals who might be excellent fits despite having atypical backgrounds or career trajectories. This risk combines elements of bias and overreliance on automation.
- **Mitigation Strategies**:
    1. **Holistic Profiling**: Use multiple factors beyond just historical average salaries or titles—consider special projects, alternative educational backgrounds, or unique skills.
    2. **Conservative Threshold Setting**: When filtering, apply conservative decision thresholds to reduce false negatives, then have humans review borderline cases.
    3. **Feedback Mechanisms**: Enable candidates to provide additional information or context if they believe the AI misclassified them.

### Implementation Feasibility and Harm Prevention

Given the high-risk nature of AI systems in recruitment, strict compliance with the EU AI Act is essential. However, with appropriate bias mitigation, transparency, data governance, and human oversight mechanisms in place, the potential harm to individuals—especially those filtered out of the recruitment pipeline—can be significantly reduced. By designing the system to encourage regular audits, explainability, and opportunities for appeal, candidates and recruiters alike can retain trust in the process and minimize the adverse effects of automation.

### **Final Recommendations**

Implementing this AI-based recruitment filter is viable if the above mitigation strategies are rigorously followed. In line with the EU AI Act’s requirements for high-risk AI systems, organizations should adopt robust data governance, regular bias and performance audits, and ensure clear documentation on model decision-making. Maintaining a human-in-the-loop at critical decision points—supported by transparency measures and candidate feedback channels—will help safeguard against discriminatory outcomes and maintain fairness. If these steps are properly executed and continuously monitored, the recruitment AI system can enhance efficiency without causing undue harm to individuals.


**Reading**:
- [Retiring Adult: New Datasets for Fair Machine Learning](https://arxiv.org/pdf/2108.04884)

**Resources**:
- [folktables](https://github.com/socialfoundations/folktables)
