document.addEventListener("DOMContentLoaded", () => {
  initViewToggle();
  initMediaFormset();
  initDeleteConfirm();
});

function initViewToggle() {
  const tableView = document.getElementById("projects-table-view");
  const formView = document.getElementById("project-form-view");
  const showAddBtn = document.getElementById("show-add-form-btn");
  const cancelBtn = document.getElementById("cancel-form-btn");
  const navAddLink = document.getElementById("nav-add-project");

  if (!tableView || !formView) return;

  const showForm = () => {
    tableView.classList.add("hidden");
    formView.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const showTable = () => {
    formView.classList.add("hidden");
    tableView.classList.remove("hidden");
    if (window.location.search.includes("add=1")) {
      window.history.replaceState({}, "", window.location.pathname);
    }
  };

  showAddBtn?.addEventListener("click", showForm);
  cancelBtn?.addEventListener("click", () => {
    if (formView.querySelector('input[name="title"]')?.form?.action.includes("/edit/")) {
      window.location.href = "/";
      return;
    }
    showTable();
  });

  navAddLink?.addEventListener("click", (event) => {
    if (tableView.classList.contains("hidden")) return;
    event.preventDefault();
    showForm();
  });
}

function initMediaFormset() {
  const addBtn = document.getElementById("add-media-btn");
  const formsContainer = document.getElementById("media-forms");
  const emptyFormTemplate = document.getElementById("empty-media-form");
  const totalFormsInput = document.getElementById("id_media-TOTAL_FORMS");

  if (!addBtn || !formsContainer || !emptyFormTemplate || !totalFormsInput) {
    return;
  }

  formsContainer.addEventListener("click", (event) => {
    const removeBtn = event.target.closest(".remove-media-btn");
    if (!removeBtn) return;

    const mediaForm = removeBtn.closest(".media-form");
    if (!mediaForm) return;

    const deleteInput = mediaForm.querySelector('input[name$="-DELETE"]');
    if (deleteInput) {
      deleteInput.checked = true;
      mediaForm.classList.add("marked-delete");
      return;
    }

    mediaForm.remove();
    updateFormIndexes();
  });

  addBtn.addEventListener("click", () => {
    const formCount = formsContainer.querySelectorAll(".media-form:not(.marked-delete)").length;
    const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, formCount);
    formsContainer.insertAdjacentHTML("beforeend", newFormHtml);
    totalFormsInput.value = formCount + 1;
  });

  function updateFormIndexes() {
    const visibleForms = formsContainer.querySelectorAll(".media-form:not(.marked-delete)");
    visibleForms.forEach((form, index) => {
      form.querySelectorAll("input, select, textarea, label").forEach((el) => {
        if (el.name) {
          el.name = el.name.replace(/media-\d+-/, `media-${index}-`);
        }
        if (el.id) {
          el.id = el.id.replace(/id_media-\d+-/, `id_media-${index}-`);
        }
        if (el.htmlFor) {
          el.htmlFor = el.htmlFor.replace(/id_media-\d+-/, `id_media-${index}-`);
        }
      });
    });
    totalFormsInput.value = formsContainer.querySelectorAll(".media-form").length;
  }
}

function initDeleteConfirm() {
  document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const row = form.closest("tr");
      const name = row?.querySelector("td")?.textContent?.trim() || "this project";
      if (!window.confirm(`Delete "${name}"? This cannot be undone.`)) {
        event.preventDefault();
      }
    });
  });
}
