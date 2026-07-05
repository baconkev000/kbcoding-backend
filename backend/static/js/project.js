document.addEventListener("DOMContentLoaded", () => {
  initViewToggle();
  initMediaFormset();
  initDeleteConfirm();
  initTypeSpecificFields();
  initTechTags();
  initCategoryTags();
  initDisplayMode();
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
  const bulkUploadInput = document.getElementById("bulk-media-upload");
  const deleteSelectedBtn = document.getElementById("delete-selected-media-btn");
  const formsContainer = document.getElementById("media-forms");
  const emptyFormTemplate = document.getElementById("empty-media-form");
  const totalFormsInput = document.getElementById("id_media-TOTAL_FORMS");

  if (!formsContainer || !emptyFormTemplate || !totalFormsInput) {
    return;
  }

  bulkUploadInput?.addEventListener("change", (event) => {
    const files = event.target.files;
    if (!files?.length) return;

    Array.from(files).forEach((file) => {
      addMediaFormRow(file);
    });

    event.target.value = "";
  });

  deleteSelectedBtn?.addEventListener("click", () => {
    const selected = formsContainer.querySelectorAll(".media-select-checkbox:checked");
    if (!selected.length) return;

    selected.forEach((checkbox) => {
      const mediaForm = checkbox.closest(".media-form");
      if (!mediaForm) return;

      const deleteInput = mediaForm.querySelector('input[name$="-DELETE"]');
      if (deleteInput) {
        deleteInput.checked = true;
        mediaForm.classList.add("marked-delete");
        checkbox.checked = false;
      } else {
        mediaForm.remove();
      }
    });

    updateFormIndexes();
  });

  function addMediaFormRow(file = null) {
    const formCount = parseInt(totalFormsInput.value, 10) || 0;
    const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, formCount);
    formsContainer.insertAdjacentHTML("beforeend", newFormHtml);
    totalFormsInput.value = formCount + 1;

    if (!file) return;

    const mediaForm = formsContainer.lastElementChild;
    const nameInput = mediaForm.querySelector('input[name$="-name"]');
    const fileInput = mediaForm.querySelector('input[type="file"]');

    if (nameInput) {
      nameInput.value = file.name.replace(/\.[^/.]+$/, "");
    }

    if (fileInput) {
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;
    }
  }

  function updateFormIndexes() {
    const allForms = formsContainer.querySelectorAll(".media-form");
    allForms.forEach((form, index) => {
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
    totalFormsInput.value = allForms.length;
  }
}

function initTypeSpecificFields() {
  const projectTypeSelect = document.getElementById("id_project_type");
  const config = document.getElementById("type-field-config");

  if (!projectTypeSelect || !config) return;

  const typeIds = {
    builds: config.dataset.buildsId,
    creative: config.dataset.creativeId,
    life: config.dataset.lifeId,
  };

  const toggleFields = () => {
    const selectedId = projectTypeSelect.value;

    document.querySelectorAll(".type-field").forEach((field) => {
      const showFor = field.dataset.showFor.split(",");
      const shouldShow = showFor.some((key) => typeIds[key.trim()] === selectedId);
      field.classList.toggle("hidden", !shouldShow);

      if (!shouldShow) {
        field.querySelectorAll("input:not([type='hidden'])").forEach((input) => {
          input.value = "";
        });
        if (field.id === "tech-field") {
          clearTechTags();
        }
      }
    });
  };

  projectTypeSelect.addEventListener("change", toggleFields);
  toggleFields();
}

function initDisplayMode() {
  const projectTypeSelect = document.getElementById("id_project_type");
  const config = document.getElementById("type-field-config");
  const mediaSection = document.getElementById("media-upload-section");
  const gameSection = document.getElementById("game-upload-section");
  const displayModeRadios = document.querySelectorAll('input[name="display_mode"]');

  if (!mediaSection || !gameSection) {
    return;
  }

  const updateSections = () => {
    const isBuilds =
      projectTypeSelect &&
      config &&
      projectTypeSelect.value === config.dataset.buildsId;
    const selectedMode =
      document.querySelector('input[name="display_mode"]:checked')?.value || "media";

    if (isBuilds && selectedMode === "web_game") {
      mediaSection.classList.add("hidden");
      gameSection.classList.remove("hidden");
    } else {
      mediaSection.classList.remove("hidden");
      gameSection.classList.add("hidden");
    }
  };

  displayModeRadios.forEach((radio) => {
    radio.addEventListener("change", updateSections);
  });
  projectTypeSelect?.addEventListener("change", updateSections);
  updateSections();
}

function initTechTags() {
  const techField = document.getElementById("tech-field");
  const techInput = document.getElementById("tech-tag-input");
  const techTagsContainer = document.getElementById("tech-tags");
  const techHiddenInput = document.getElementById("id_tech");

  if (!techField || !techInput || !techTagsContainer || !techHiddenInput) {
    return;
  }

  let tags = [];

  const syncHiddenInput = () => {
    techHiddenInput.value = JSON.stringify(tags);
  };

  const renderTags = () => {
    techTagsContainer.innerHTML = "";
    tags.forEach((tag) => {
      const tagEl = document.createElement("span");
      tagEl.className = "tech-tag";
      tagEl.textContent = tag;

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "tech-tag-remove";
      removeBtn.setAttribute("aria-label", `Remove ${tag}`);
      removeBtn.textContent = "×";
      removeBtn.addEventListener("click", () => {
        tags = tags.filter((item) => item !== tag);
        renderTags();
        syncHiddenInput();
      });

      tagEl.appendChild(removeBtn);
      techTagsContainer.appendChild(tagEl);
    });
  };

  const addTag = (value) => {
    const tag = value.trim();
    if (!tag || tags.includes(tag)) return;
    tags.push(tag);
    renderTags();
    syncHiddenInput();
  };

  window.clearTechTags = () => {
    tags = [];
    renderTags();
    syncHiddenInput();
    techInput.value = "";
  };

  try {
    const initial = JSON.parse(techHiddenInput.value || "[]");
    if (Array.isArray(initial)) {
      tags = initial.map((item) => String(item).trim()).filter(Boolean);
      renderTags();
      syncHiddenInput();
    }
  } catch {
    tags = [];
    syncHiddenInput();
  }

  techInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addTag(techInput.value);
      techInput.value = "";
    }
  });

  techInput.addEventListener("blur", () => {
    if (techInput.value.trim()) {
      addTag(techInput.value);
      techInput.value = "";
    }
  });

  document.getElementById("project-form")?.addEventListener("submit", syncHiddenInput);
}

function initCategoryTags() {
  const tagInput = document.getElementById("category-tag-input");
  const tagsContainer = document.getElementById("category-tags");
  const hiddenInput = document.getElementById("id_tag_names");
  const suggestionsList = document.getElementById("category-tag-suggestions");

  if (!tagInput || !tagsContainer || !hiddenInput) {
    return;
  }

  let tags = [];
  let availableTags = [];

  const syncHiddenInput = () => {
    hiddenInput.value = JSON.stringify(tags);
  };

  const renderTags = () => {
    tagsContainer.innerHTML = "";
    tags.forEach((tag) => {
      const tagEl = document.createElement("span");
      tagEl.className = "tech-tag";
      tagEl.textContent = tag;

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "tech-tag-remove";
      removeBtn.setAttribute("aria-label", `Remove ${tag}`);
      removeBtn.textContent = "×";
      removeBtn.addEventListener("click", () => {
        tags = tags.filter((item) => item !== tag);
        renderTags();
        syncHiddenInput();
      });

      tagEl.appendChild(removeBtn);
      tagsContainer.appendChild(tagEl);
    });
  };

  const addTag = (value) => {
    const tag = value.trim();
    if (!tag || tags.includes(tag)) return;
    tags.push(tag);
    if (!availableTags.includes(tag)) {
      availableTags.push(tag);
      availableTags.sort((a, b) => a.localeCompare(b));
      renderSuggestions();
    }
    renderTags();
    syncHiddenInput();
  };

  const renderSuggestions = () => {
    if (!suggestionsList) return;
    suggestionsList.innerHTML = "";
    availableTags.forEach((name) => {
      const option = document.createElement("option");
      option.value = name;
      suggestionsList.appendChild(option);
    });
  };

  fetch("/api/tags/")
    .then((response) => response.json())
    .then((data) => {
      availableTags = (Array.isArray(data) ? data : data.results || [])
        .map((item) => item.name)
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b));
      renderSuggestions();
    })
    .catch(() => {});

  try {
    const initial = JSON.parse(hiddenInput.value || "[]");
    if (Array.isArray(initial)) {
      tags = initial.map((item) => String(item).trim()).filter(Boolean);
      renderTags();
      syncHiddenInput();
    }
  } catch {
    tags = [];
    syncHiddenInput();
  }

  tagInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addTag(tagInput.value);
      tagInput.value = "";
    }
  });

  tagInput.addEventListener("blur", () => {
    if (tagInput.value.trim()) {
      addTag(tagInput.value);
      tagInput.value = "";
    }
  });

  document.getElementById("project-form")?.addEventListener("submit", syncHiddenInput);
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
