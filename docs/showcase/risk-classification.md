## Risk Classification Under the EU AI Act

<!-- TODO: Add a decision diagram in Mermaid? -->

- **Determine if the system is considered AI under the EU AI Act (see |Article 3(1)|)**
    - **Reasoning**: The system uses machine learning methods (a classification model) to estimate candidates’ likely income. Machine learning is explicitly covered by the definition of AI in the EU AI Act.
    - **Outcome**: Yes, this system is within scope because it qualifies as an AI system.
- **Check whether the AI system falls outside the scope of the AI Act (see |Article 2|)**
    - **Context**: Under certain circumstances, some AI systems and operators are excluded from the regulatory requirements. This includes, for example, if the system is used exclusively for military purposes or for scientific research.
    - **Reasoning**: This recruitment system is a commercial application used by recruiters and hiring managers, so it does not qualify for exemption.
    - **Outcome**: The system is not exempt; it is still in scope.
- **Determine if the AI system poses an ‘unacceptable risk’**
    - **Reasoning**: Under |Article 5| of the EU AI Act, eight use cases are deemed to pose an ‘unacceptable risk’. This includes for example, systems that use manipulative or exploitative practices, social scoring, or emotion recognition in the workplace. A recruitment filter based on estimated salary ranges does not meet the criteria listed in Article 5.
    - **Outcome**: The system does not pose an ‘unacceptable risk.’
- **Assess whether the AI system is considered ‘high risk’**
    - **Reasoning**: The EU AI Act (in Annex III, point 4) lists AI systems used in the employment and management of workers (including to "filter job applications") as high risk. This system directly assists with filtering and selecting candidates for roles, thereby influencing employment opportunities.
    - **Outcome**: The system falls under the ‘high risk’ category.

- **Assess if additional transparency obligations apply (See |Article 50|)**
- **Reasoning**: The system does not interact with humans nor does it generate synthetic content.
    - **Outcome**: The system does not have additional transparency obligations

- **Assess if the system poses 'minamal risk'**
    - **Reasoning**: Since we have already determined it is high risk due to its recruitment use case, this consideration does not apply.
    - **Outcome**: Classification remains ‘high risk.’

**Final Outcome**

Based on the criteria outlined in the EU AI Act, the proposed recruitment AI system qualifies as a **high-risk system**.
Consequently, the system will be subject to additional legal and compliance obligations, specifically those in Chapter III of the AI Act. This includes product safety requirements like risk management, data governance, documentation and traceability, transparency requirements, and human oversight.
