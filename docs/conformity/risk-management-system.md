# Risk Management System

|Article 9| of the EU AI Act establishes requirements for implementing a risk management system to identify, analyze, and manage risks and threats arising from the use of the AI system "to health, safety or fundamental rights", when used for its intended purpose or under reasonably foreseeable misuse (see |Art. 3(13)|).
Also, it requires a risk assessment for the case in which the AI system is used outside of its intended purpose, for example by a malicious actor.

!!! info "Engineering Info"

    --8<-- "docs/conformity/\_engineering-info-box.partial"

    - This document does not directly reference other articles in the AI Act, since it is mostly out of scope for the engineering practices described in this project.

## Non-technical requirements

Even though it is named a "system", the risk management system introduced in the article is not necessarily a physical system, but rather a list of actions and provisions.
Similarly, it is not meant as a single condition that an AI system must satisfy to be allowed to operate, but rather a continuous loop of evaluation for the AI system throughout its lifecycle.

It might be more sensible to interpret this article not as a requirement addressed by a single software system, but rather as a guideline that should be adhered to by all personnel involved in the design and implementation of the AI system, and be applied as a "continuous iterative process" (see |Art. 9(2)|) throughout the project lifecycle.

In general, providers must identify, evaluate, and mitigate risks that are known and "reasonably" foreseeable.
These risks might emerge both when the system is being used as intended and when it being misused in ways that are foreseeable. Finally, providers must also mitigate risks that are identified after the system goes into production.

While these concepts may seem vague at first, it is expected that harmonized technical standards will help engineers better understand what types of risks and circumstances they should consider.

Since the sources and types of risks of each system are different, it is in general not feasible to automate these risk assessments.
Nevertheless, to give an example for an analysis and a mitigation strategy, we can have a look at a specific risk in our [showcase](../showcase/index.md):

!!! note "**Risk of Bias and Discrimination**"

    - **Reasoning**: A classification model that predicts salary bands can inadvertently learn biased patterns from historical or non-representative data. If the training dataset underrepresents certain groups or if it carries historical inequalities, the model might systematically discriminate. This could result in unfair exclusion of qualified candidates from certain demographic or socioeconomic backgrounds.
    - **Mitigation Strategies**:
        1. **Data Quality and Diversity**: Ensure the dataset is representative of different demographic groups. Perform data audits to identify and remove or mitigate biases.
        2. **Bias Detection and Monitoring**: Use fairness metrics (e.g., disparate impact ratio, equalized odds) to assess and continually monitor the model’s outputs across different groups.
        3. **Fairness-Aware Algorithms**: Employ techniques such as reweighing or adversarial debiasing to reduce or eliminate learned biases.
        4. **Human Review**: Maintain a human-in-the-loop for critical decisions, ensuring that final filtering choices are not made solely by the AI.


This example of bias and discrimination risk is provided to give a first impression of what a risk analysis under |Article 9| might entail. It is **not** an exhaustive analysis in the sense of |Article 9|, which would require a comprehensive, systematic identification and assessment of all risks to health, safety, and fundamental rights throughout the AI system's lifecycle.

In this sense, the risk management system must be a living process that extends beyond initial risk identification. In particular, high-risk AI systems must undergo continuous testing throughout their lifecycle, with mandatory testing before productization and release to end users (see Sections (6) to (8)).

We highlight that the risk management system as presented in |Article 9| is not directly tied to, but in fact a requirement for a lot of the engineering practices showcased in this repository, since they require prior knowledge about the relevant risks of the project.

<!-- Link to aAI Institute resources on Rsi-->
