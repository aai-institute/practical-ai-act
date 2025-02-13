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