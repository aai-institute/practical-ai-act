# Transparency and Provision of Information

To get a more hands-on reading of article 13, we shall assume, that there
is a fix use-case to solve and the input data have a specified format
(does this makes sense?).

The first thing to notice is, that information
must be provided to the user even on an event level. This means, that there
must be an identifier for each event (inference call, failure, ...), which can be used to trace back the
collected information. This is tightly connected to article 12, which
handles the requirements regarding record-keeping. We can elaborate on this
by showing a simple event-based architecture using databases
to persist the information and make them available to the user via an API.

Let's talk about which kind of information must be provided to the user.
The requirements described in article 13 of the EU AI Act can be broadly
seperated into two categories. The first category is static information
about the system, which is not input dependent. The second category is the
information about the output for a specific input (this is a point of discussion!).


## Static information about system

This includes all information about the system, which is not input dependent.
These can be further subdivided.

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

* input data scheme; How to get an output of the model?


### Model-dependent information
* type of the AI system; What kind of model is used? What are the limitations, due to the model architecture, 13.3 b(iv)
* evaluation metrics for the model to show the performance to expect, e.g. accuracy, precision, recall, F1-score; How good is the model? 13.3 b(ii)
* statistics about restricted performance, e.g. subgroup performance; How good is the model for different groups? 13.3 b(v)
* information about the training data; How was the model trained? 13.3 b(vi)


## Information about the output for a specific input
* additional information, which allow for interpretation of the output.
  In the text, it is mentioned "where applicable", which leads to a discussion
  about intrinsically interpretable models and post-hoc interpretability methods
  for black-box models. 13.3 b(vii), 13.3 d (connection to human oversight)