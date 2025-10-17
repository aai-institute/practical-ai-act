document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector("input.md-search__input");

  if (!searchInput) {
    return;
  }

  searchInput.addEventListener("change", function () {
    const query = searchInput.value.trim();
    if (query.length > 0) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: "site_search",
        search_term: query,
      });
    }
  });
});
