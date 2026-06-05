// M365 Agent Templates — landing page interactions
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("primary-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "메뉴 닫기" : "메뉴 열기");
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (nav.classList.contains("is-open")) {
          nav.classList.remove("is-open");
          toggle.setAttribute("aria-expanded", "false");
          toggle.setAttribute("aria-label", "메뉴 열기");
        }
      });
    });
  }

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  /* ---------- Template rendering ---------- */
  const grid = document.getElementById("template-grid");
  const noResults = document.getElementById("no-results");
  const searchInput = document.getElementById("template-search");
  const tabs = Array.from(document.querySelectorAll(".filter-tab"));

  let cards = [];
  let currentFilter = "agent";
  let currentQuery = "";

  const initialFilter = new URLSearchParams(window.location.search).get("filter");
  if (initialFilter && tabs.some((tab) => tab.getAttribute("data-filter") === initialFilter)) {
    currentFilter = initialFilter;
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderCard(template, index) {
    const article = document.createElement("article");
    article.className = "template-card";
    article.dataset.type = template.type || "agent";
    if (template.id) article.dataset.id = template.id;

    const downloads = (template.downloads || [])
      .map((d) => {
        const fileType = d.fileType || "";
        const isUrlLink = !fileType || fileType.toUpperCase() === "URL";
        const url = d.url || "#";
        const isPlaceholder = !d.url || d.url === "#";

        const aria = !isUrlLink && fileType
          ? `${template.title} ${d.label} (${fileType})`
          : `${template.title} ${d.label}`;

        let linkAttrs = "";
        if (!isPlaceholder) {
          linkAttrs = isUrlLink
            ? ' target="_blank" rel="noopener noreferrer"'
            : ' download';
        }

        const badge = (!isUrlLink && fileType)
          ? '<span class="file-type">.' + escapeHtml(fileType) + "</span>"
          : "";

        return (
          '<a class="download-row" href="' + escapeHtml(url) + '"' +
          ' aria-label="' + escapeHtml(aria) + '"' +
          linkAttrs + ">" +
            "<span>" + escapeHtml(d.label) + "</span>" +
            badge +
          "</a>"
        );
      })
      .join("");

    const fallback = escapeHtml(template.fallbackEmoji || "📦");

    article.innerHTML =
      '<div class="template-icon">' +
        '<img src="' + escapeHtml(template.icon) + '" alt=""' +
        " onerror=\"this.parentElement.classList.add('placeholder');this.outerHTML='" + fallback + "'\">" +
      "</div>" +
      '<div class="template-body">' +
        '<div class="template-head">' +
          "<h3>" + (index + 1) + ". " + escapeHtml(template.title) + "</h3>" +
          '<span class="tag" data-tag="' + escapeHtml(template.type) + '">' + escapeHtml(template.tagLabel) + "</span>" +
        "</div>" +
        '<p class="template-desc">' + escapeHtml(template.description) + "</p>" +
        '<div class="downloads-label">Downloads</div>' +
        downloads +
      "</div>";

    return article;
  }

  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function applyFilters() {
    if (!cards.length) return;
    let visibleCount = 0;
    const query = normalize(currentQuery);

    cards.forEach((card) => {
      const type = card.getAttribute("data-type") || "";
      const text = normalize(card.textContent);

      const matchesType = currentFilter === "all" || type === currentFilter;
      const matchesQuery = query === "" || text.includes(query);
      const visible = matchesType && matchesQuery;

      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    if (noResults) {
      noResults.classList.toggle("is-visible", visibleCount === 0);
    }
  }

  function renderTemplates(items) {
    if (!grid) return;
    grid.innerHTML = "";
    const frag = document.createDocumentFragment();
    const perTypeCount = {};
    items.forEach((t) => {
      const type = t.type || "all";
      const localIndex = perTypeCount[type] || 0;
      perTypeCount[type] = localIndex + 1;
      frag.appendChild(renderCard(t, localIndex));
    });
    grid.appendChild(frag);
    grid.setAttribute("aria-busy", "false");
    cards = Array.from(grid.querySelectorAll(".template-card"));
    applyFilters();
  }

  function renderMessage(message) {
    if (!grid) return;
    grid.innerHTML = "";
    grid.setAttribute("aria-busy", "false");
    const p = document.createElement("p");
    p.className = "template-loading";
    p.textContent = message;
    grid.appendChild(p);
  }

  async function loadTemplates() {
    if (!grid) return;
    try {
      const res = await fetch("templates.json", { cache: "no-cache" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const manifest = await res.json();
      const categories = (manifest && manifest.categories) || [];
      if (!Array.isArray(categories) || categories.length === 0) {
        throw new Error("Invalid templates.json manifest shape");
      }

      const groups = await Promise.all(
        categories.map(async (cat) => {
          const r = await fetch(cat.source, { cache: "no-cache" });
          if (!r.ok) throw new Error(cat.source + " HTTP " + r.status);
          const json = await r.json();
          const items = (json && json.items) || [];
          return items.map((item) => Object.assign({}, item, {
            type: cat.type,
            tagLabel: cat.tagLabel,
          }));
        })
      );

      const merged = groups.reduce((acc, arr) => acc.concat(arr), []);
      renderTemplates(merged);
    } catch (err) {
      console.error("[templates] load failed", err);
      renderMessage(
        "템플릿을 불러오지 못했습니다. 페이지를 새로고침해 주시거나 templates.json / data/*.json을 확인해 주세요."
      );
    }
  }

  /* ---------- Filter tabs ---------- */
  tabs.forEach((tab) => {
    const isActive = (tab.getAttribute("data-filter") || "all") === currentFilter;
    tab.classList.toggle("is-active", isActive);
    tab.setAttribute("aria-selected", String(isActive));
  });

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => {
        t.classList.remove("is-active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("is-active");
      tab.setAttribute("aria-selected", "true");
      currentFilter = tab.getAttribute("data-filter") || "all";
      applyFilters();
    });
  });

  /* ---------- Search ---------- */
  if (searchInput) {
    let debounceId;
    searchInput.addEventListener("input", (event) => {
      clearTimeout(debounceId);
      const value = event.target.value;
      debounceId = setTimeout(() => {
        currentQuery = value;
        applyFilters();
      }, 80);
    });
  }

  /* ---------- "Download all" placeholder behavior ---------- */
  const downloadAllBtn = document.getElementById("download-all");
  if (downloadAllBtn) {
    downloadAllBtn.addEventListener("click", () => {
      const visibleCards = cards.filter((c) => !c.hidden).length;
      const total = cards.length;
      const label = visibleCards === total
        ? "전체 템플릿 패키지는 곧 제공될 예정입니다."
        : "현재 표시 중인 " + visibleCards + "개 항목을 묶는 번들은 준비 중입니다.";
      // eslint-disable-next-line no-alert
      alert(label + "\n각 카드의 개별 다운로드를 이용해 주세요.");
    });
  }

  /* ---------- Boot ---------- */
  loadTemplates();
})();

