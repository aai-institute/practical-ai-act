!!! warning "Legal Disclaimer"

    The information provided on this website is for informational purposes only and does not constitute legal advice.
    The tools, practices, and mappings presented here reflect our interpretation of the EU AI Act and are intended to support understanding and implementation of trustworthy AI principles.
    Following this guidance does not guarantee compliance with the EU AI Act or any other legal or regulatory framework.

    We are not affiliated with, nor do we endorse, any of the tools listed on this website.

## Who is this website for?

This project is intended for AI practitioners, data scientists, and engineers who are interested in implementing trustworthy AI systems under the European AI Act.

The information is applicable to low- and high-risk AI systems, since it provides a sound engineering foundation for building trustworthy AI systems in general.

## Syllabus

This project is structured around three interconnected areas, each addressing a key aspect of AI system development in the context of EU AI Act compliance. The content is modular and designed for flexible navigation—readers are encouraged to explore the connections between legal requirements, engineering practices, and implementation choices.

A central aim of this work is to bridge the gap between regulatory obligations and technical execution. By making the relationships between legal texts, software engineering practice, and actual implementations explicit, we hope to support teams in building AI systems that are not only effective, but also aligned with compliance goals from the ground up.

-   [**Showcase**](showcase/index.md): Presents a practical use case that runs throughout the project. It illustrates the application of compliance concepts in context and includes a risk classification based on the EU AI Act.
-   [**Engineering Practice**](engineering-practice/index.md): Provides a set of software engineering best practices that form the technical foundation for compliance. Each practice is mapped to relevant AI Act provisions to guide implementation.
-   [**AI Act Conformity**](conformity/index.md): Breaks down the legal requirements of the EU AI Act and connects them to concrete engineering actions, helping translate regulatory language into actionable guidance.

Depending on your background, different entry points may make more sense.
If you're from a technical or engineering background, you might start with [Engineering Practice](engineering-practice/index.md). If you're approaching from a legal, regulatory, or policy perspective, [AI Act Conformity](conformity/index.md) may be the best starting point.
If you prefer to see things in context first, the [Showcase](showcase/index.md) offers a concrete example that ties the other sections together.

## Navigation

Due to the connections between requirements originating from the AI Act and engineering best
practice being a core value of this project, we want to provide an easy navigation
between these sections. As there is no clear one-to-one relation (it is more many-to-one or one-to-many) between requirements and engineering practice, the challenge is
to find a good representation, which makes it easier to handle the complexity.
If you view this as a network and the practices and requirements
are being the knots, then it is import to make the edges between those explicit.

On the section pages [Engineering practice](engineering-practice/index.md) resp. [AI Act Conformity](conformity/index.md), you will find overview tables, which summarize
these connections. Moreover, on every page in these sections you find info boxes
([Compliance Information Boxes](#compliance-information-boxes) in the [Engineering practice](engineering-practice/index.md) section, resp. [Engineering Information Boxes](#engineering-information-boxes) in the [AI Act Conformity](conformity/index.md) section) giving more details on the linking.



### Compliance Information Boxes

The engineering practices contain information boxes that provide references to applicable parts of the AI Act, like the one at the bottom of this section.
This information is intended to help you understand how the engineering practices relate to the legal requirements of the AI Act.

Note that these references do not imply that following a given engineering practice will guarantee compliance with the reference parts of the AI Act.

!!! success "Compliance Info"

    This is an example for the Compliance Info box.

    - **|Art. 14|** (Human Oversight), in particular:
        - |Art. 14(4)(e)|, continuous monitoring the operation of the systems helps
            to detect conditions requiring potential intervention

### Engineering Information Boxes
Coming from requirements induced by the AI Act, it is of interest to link
certain aspects of the respective requirement to corresponding engineering practices.
This is represented by information boxes, like the one at the bottom of this section.
You can think of them as the reverse direction of the connections collected
in [Compliance Information Boxes](#compliance-information-boxes).

Again, following these practices may not guarantee compliance, as there might be
parts of the requirement, which are not amenable to automation.

!!! info "Engineering Info"

    This is an example for the Compliance Info box.

    - [**Operational Monitoring**](engineering-practice/operational-monitoring.md):
        -   |Art. 14(4)(e)|, continuous monitoring the operation of the systems helps
            to detect conditions requiring potential intervention

### Page Backlinks

You might notice that some pages contain hyperlinks to other pages marked with an <em>↙</em> arrow at the top of the page:

<figure markdown="span">
![Backlinks](_images/backlinks.png){ align=center }
</figure>

These links point to other pages on this website that contain links to the current page and help you discover and navigate related content more easily, even if it is not mentioned in the info box of the page.

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
