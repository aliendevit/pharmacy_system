// Confirm delete buttons
addEventListener("click", (e) => {
  const t = e.target.closest('[data-confirm]');
  if (!t) return;
  if (!confirm("Delete this item? This cannot be undone.")) {
    e.preventDefault();
  }
});

// Strip empty inputs from GET forms (like toolbar search)
addEventListener("submit", (e) => {
  const form = e.target.closest("form.toolbar");
  if (!form) return;

  // Drop empty input names so ?low= won’t appear
  for (const input of form.querySelectorAll("input")) {
    if (input.type !== "checkbox" && input.value.trim() === "") {
      input.dataset._name = input.name;
      input.removeAttribute("name");
    }
  }

  // Restore names after submit for usability
  setTimeout(() => {
    for (const input of form.querySelectorAll("input")) {
      if (!input.name && input.dataset._name) {
        input.name = input.dataset._name;
        delete input.dataset._name;
      }
    }
  }, 0);
});
