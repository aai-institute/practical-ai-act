# Transparency and Provision of Information

!!! info "Engineering Info"
    --8<-- "docs/conformity/_engineering-info-box.partial"

    - [Explainability]:
        - |Art. 13(1)|: Explainability techniques contribute to a transparent system operation
        - |Art. 13(3)(b)(iv)(vii)|: Explainability techniques directly provide information relevant to explain the system's output
        - |Art. 13(3)(d)|: Explainability techniques can be used in the human oversight process to interpret the system's behavior
    - [Experiment Tracking]:
        - |Art. 13(3)(b)(ii)|: Experiment tracking captures used performance metrics and levels of accuracy
    - [Model Registry]:
        - |Art. 13(3)(b)(iv)|: Logging the model architecture and hyperparameters makes the system characteristics transparent
    - [Operational Monitoring]:
        - |Art. 13(3)(e)|: Monitoring the operation of the system enables to provide statistics about the system resource usage

To get a more hands-on reading of Article 13, we shall assume, that there
is a fix use-case to solve and the input data have a specified format
(does this makes sense?).

The first thing to notice is, that information
must be provided to the user even on an event level. This means, that there
must be an identifier for each event (inference call, failure, ...), which can be used to trace back the
collected information. This is tightly connected to Article 12, which
handles the requirements regarding record-keeping. We can elaborate on this
by showing a simple event-based architecture using databases
to persist the information and make them available to the user via an API.

Let's consider which kind of information must be provided to the user (in the context of the AI act this is the deployer).
The requirements described in Article 13 of the EU AI Act can be broadly
seperated into two categories. The first category is static information
about the system, which is not input dependent. The second category is the
information about the output for a specific input (this is a point of discussion!).


## Static information about the system

This includes all information about the system, which is not input dependent.
There seem to be quite an overlap with
[Hugging Face model cards](https://huggingface.co/docs/hub/en/model-cards).

The static information can be further subdivided into those which are model-independent
and those which are model-dependent.

### Model-independent information
All information, which is not specific for a single model or may be stable over
a long time:

* identity and contact details of provider; Who is responsible for the system?
    * 13.3 a
    * This does not need much of an explanation, but we can include it in our showcase implementation as well.

* intended purpose of a system; Which problem will be solved?
    * 13.3 b(i)
    * This needs clarification about how detailed the description of the system
      has to be and which language (in the sense of using machine learning terminology) should be used. We can provide an example for the simple case of classification and regression with the census data.
    * A still vague definition is given in article 3.12.

* input data scheme; How to get an output of the model?
    * 13.2, 13.3 b(vi)
    * Although this is not mentioned explicitly, it belongs to the general instructions of use; it has to be clear and accessible to the user, how the input schema has to look like to run inference of the model.
    * Again, this information can be made accessible via an API, which provides the schema of the input data, and we can easily showcase this.


### Model-dependent information

* description of the model; What kind of model is used?
    * 13.3 b(iv)
    * this includes the description of the model type/architecture, hyperparameters and preprocessing. Here the task will be to show how to make all this information amenable for logging, e.g. automatically create a string representation.

* evaluation metrics for the model to show the performance to expect
    * 13.3 b(ii)
    * I think which metrics (in the mathematical sense) to use for which ml problem
      is pretty standard, e.g. accuracy, precision, recall, F1-score for a binary classification; Maybe it is best to not elaborate on this too much but reference a
      good source for this?
    * More important than the metrics themselves is the question of how the evaluation
      was done, e.g. how the data was split or if cross-validation was used. This
      is also tightly connected to the information about the training data. There
      should be transparency about how to reproduce the evaluation result.

* statistics about restricted performance, e.g. subgroup performance;
    * 13.3 b(v)
    * This is a point of discussion. We should explain in which scenario an isolated
      view on a specific subgroup (may it be a group having a specific feature or
      in a binary problem looking only at the positive labeled group, i.e. precision and recall) makes sense.
    * We should make the connection to Article 11 and Annex IV

* information about the training data;
    * 13.3 b(vi)
    * this information might be about the data collection process, any data transformation, basically the information collected from the data governance view point. Here it might be more challenging to find a good format for providing it
      to the user, but maybe it also makes sense to make it available via an API?
    * We should make the connection to Article 11 and Annex IV


## Information about the output for a specific input

In contrast to the information discussed so far, this includes all information
which is specific to a single input.
* logs for a specific inference call;
    * 13.3 f
    * based on an event-based architecture, we can provide a simple API to access the logs for a specific inference call and an instruction how to use the endpoints should be available.
    * again, this is tightly connected to article 12 and the record-keeping requirements.
* additional information, which allow for interpretation of the output.
    * 13.3 b(vii), 13.3 d (connection to human oversight)
    * the AI act is extremely vague in regard to this point. It uses phrase like
      "where applicable" and "enable deployers to interpret the output".
    * We should elaborate on how to make this more concrete. One way could be to speak
      about the terms interpretability and explainability how they are used in the technical community, i.e. a discussion about intrinsically interpretable models and post-hoc interpretability methods for black-box models.

## Open questions

* since explainability (XAI) and interpretability are not mentioned explicitly in article 13, but might be helpful to enable the user to handle the output ("interpret/ explain the output") in a better way, should we include it in our explanations and showcase?
    * I think we can keep the explanation part short and reference to a good source for this.
    * It should be included into the showcase, because the costs to actually implement it are not high and the information gain for the user is high.
    * it is not clear how to deal with the terms "where applicable" and "when appropriate".
* what part of the information collected for data governance should be made available to the user and how?
    * Can [Hugging Face model cards](https://huggingface.co/docs/hub/en/model-cards) be used as a template for this?
* the term "**reasonably foreseeable misuse**" is used in article 13.b (iii) and defined in article 3.13.
    * In short, any possible not intended use due to the fact that humans are humans. E.g. they are lacking skills to use the system appropriately, I think of the typical it-support scenario or the user has evil intentions.
    * Still, it is unclear how to include it in our showcase. Besides the explainability part, this will is the biggest open question.
* Art. 13(3), (b)(iv): Get a sense for "technical characteristics and capabilities" - what's the intention and rationale behind this phrasing?
* What is the connection between Article 11, Annex IV and Article 13.3 b(v, vi)? Is it instruction for use vs. technical documentation (what is the difference)?
* The meaning and intention of Article 13.3 c is completely unclear (is this something like a "diff")
* What is the difference between the terms "misuse", "abuse" and "attack" in the context of the AI act?

## Potential tasks
* Set up an event logging system and document its architecture in line with Art. 13(3), (f) and Art. 12
* starting from our use-case, think about potential misuses.
    * e.g. use the model for a different age span than in the training,
      so the model will still give an output, but it is not semantically meaning full.
* set up an automatic way to build the (provenance) information about the model, preprocessing and training data.
  * the goal should be to create transparency and traceability about the complete processing pipeline
  * e.g. sklearn pipeline steps documented included parameterization
* implement a basic API to provide the static information about the system.
* implement the usage of intrinsically explainable models and/or usage of post-hoc methods, have a look at the [interpret](https://github.com/interpretml/interpret) package.


Related Norms:
* [ISO/IEC FDIS 12792 (Transparency taxonomy of AI systems)](https://www.iso.org/standard/84111.html)
* [ISO/IEC TS 4213](https://www.iso.org/standard/79799.html)
* [ISO/IEC AWI 4213](https://www.iso.org/standard/89455.html)
* [ISO/IEC DTS 6254](https://www.iso.org/standard/82148.html)


<!-- Reference Links -->
[Explainability]: ../engineering-practice/explainability.md
[Experiment Tracking]: ../engineering-practice/experiment-tracking.md
[Model Registry]: ../engineering-practice/model-registry.md
[Operational Monitoring]: ../engineering-practice/operational-monitoring.md
