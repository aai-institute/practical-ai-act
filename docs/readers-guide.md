!!! success "Legal Disclaimer"

    The information provided on this website is for informational purposes only and does not constitute legal advice.
    The tools, practices, and mappings presented here reflect our interpretation of the EU AI Act and are intended to support understanding and implementation of trustworthy AI principles.
    Following this guidance does not guarantee compliance with the EU AI Act or any other legal or regulatory framework.

    We are not affiliated with, nor do we endorse, any of the tools listed on this website.

## Who is this website for?

This project is intended for AI practitioners, data scientists, and engineers who are interested in implementing trustworthy AI systems under the European AI Act.

The information is applicable to low- and high-risk AI systems, since it provides a sound engineering foundation for building trustworthy AI systems in general.

## Syllabus

The project is structured into three key areas, each addressing different aspects of AI system development and compliance with the EU AI Act. The content is not meant to be consumed in linear order.

-   [**Showcase**](showcase/index.md): This section introduces a demonstrational use-case that we use to develop the content. It also includes a risk classification according to the EU AI Act.
-   [**Engineering Practice**](engineering-practice/reference-architecture.md): Following software engineering best practice lay the foundation for achieving compliance.
-   [**AI Act Conformity**](conformity/index.md): Background information connecting technical artifacts to the obligations of the AI Act

## Conventions

### Page Backlinks

You might notice that some pages contain hyperlinks to other pages marked with an <em>↙</em> arrow at the top of the page:

<figure markdown="span">
![Backlinks](_images/backlinks.png){ align=center }
</figure>

These links point to other pages on this website that contain links to the current page and help you discover and navigate related content more easily.

### Compliance Information Boxes

The engineering practices contain information boxes that provide references to applicable parts of the AI Act, like the at the bottom of this section.
This information is intended to help you understand how the engineering practices relate to the legal requirements of the AI Act.

Note that these references do not imply that following a given engineering practice will guarantee compliance with the reference parts of the AI Act.

!!! success "Compliance Info"

    This is an example for the Compliance Info box.

    - **|Art. 1|** (Subject Matter)
    - **|Art. 2(1)|** (Scope)

## What is out of scope?

### Assessing your use case's risk category

If you are unsure how the AI Act applies to your use case, you should first try to determine the appropriate risk classification for your use case.

The following resources can help you with that:

-   The appliedAI Institute [Risk Classification Database](https://www.appliedai-institute.de/en/risk-classification-database), a comprehensive list of practical examples of high-risk and non high-risk use cases on AI systems under the EU AI Act
-   The [EU Act Compliance Checker](https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/), an interactive tool that helps you assess the risk category of your AI system and applicable requirements from the AI Act

### Systems covered under European Harmonized Standards

If your system is covered under European Harmonized Standards (see |Annex I|), you should refer to the relevant standards for guidance on compliance.

### General-purpose AI systems

If you are building a general-purpose AI system, you will still find the engineering resources useful, since they mirror good software engineering practices.

However, the compliance resources are specifically tailored to the requirements for high-risk AI systems under Chapter III of the AI Act.

For guidance on how to comply with Chapter V of the AI Act, you might find the following resources helpful:

-   The [European AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-office), which oversees the implementation of the AI Act, while ensuring compliance, fostering innovation, and coordinating AI governance across EU Member States.
-   The [General-Purpose AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/ai-code-practice), and an [explorer for the draft Code of Practice](https://code-of-practice.ai).

### Relationship to Privacy and Data Protection

The project does not cover the relationship between the AI Act and the General Data Protection Regulation (GDPR), or the question of privacy in Machine Learning more broadly.

The AI Act and the GDPR are separate legal frameworks, and while they may overlap in some areas, they have different objectives and requirements.
Although some of the engineering practices on this website also help you comply with the GDPR, we do not explicitly consider these privacy and data protection aspects.

## Recommended Knowledge

-   A basic understanding of machine learning and AI concepts
-   An understanding of the terminology in |Art. 3| of the AI Act
-   Familiarity with Python programming, if you want to follow along with the code examples
-   Software engineering best practices for ML:
    -   See the [Beyond Jupyter series](https://transferlab.ai/trainings/beyond-jupyter/) for an introduction
