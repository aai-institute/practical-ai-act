document$.subscribe(function () {
  const feedback = document.forms.feedback;
  if (typeof feedback === "undefined") {
    return;
  }

  // Show feedback text
  feedback.hidden = false;

  feedback.addEventListener("submit", function (ev) {
    ev.preventDefault();

    feedback.firstElementChild.disabled = true;

    // Submit GTM page event
    const dataLayer = window.dataLayer || [];
    const page = document.location.pathname;
    const data = ev.submitter.getAttribute("data-md-value");
    dataLayer.push({
      event: "feedback",
      page: page,
      feedback: data,
    });

    // Show note
    const note = feedback.querySelector(
      ".md-feedback__note [data-md-value='" + data + "']"
    );
    if (note) {
      note.hidden = false;
    }
  });
});
