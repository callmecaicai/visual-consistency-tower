const KB = window.KNOWLEDGE_BASE;

const ROLE_LABELS = {
  all: "全部角色",
  index: "总导航",
  "stage-entry": "阶段入口",
  "stage-extension": "阶段扩展",
  locator: "定位卡",
  mechanism: "主机制",
  expansion: "扩展 / 专题",
  conclusion: "结语",
  appendix: "补章",
  "cross-cut": "横切",
  application: "应用域",
  archive: "归档",
  skill: "技能",
  "skill-meta": "技能导航",
  meta: "导航 / 协议",
  document: "其他文档",
};

const state = {
  layer: "all",
  role: "all",
  query: "",
  chapter: "",
  includeArchived: false,
  selectedId: null,
};

const refs = {
  searchInput: document.getElementById("searchInput"),
  layerFilter: document.getElementById("layerFilter"),
  roleFilter: document.getElementById("roleFilter"),
  archiveToggle: document.getElementById("archiveToggle"),
  stageTree: document.getElementById("stageTree"),
  docList: document.getElementById("docList"),
  previewPane: document.getElementById("previewPane"),
  statsBar: document.getElementById("statsBar"),
  resultCount: document.getElementById("resultCount"),
  locatorInput: document.getElementById("locatorInput"),
  locatorButton: document.getElementById("locatorButton"),
  locatorOutput: document.getElementById("locatorOutput"),
};

function applyUrlState() {
  const params = new URLSearchParams(window.location.search);
  const layer = params.get("layer");
  const role = params.get("role");
  const chapter = params.get("chapter");
  const q = params.get("q");
  const locate = params.get("locate");
  const doc = params.get("doc");
  const archive = params.get("archive");

  if (layer) state.layer = layer;
  if (role) state.role = role;
  if (chapter) state.chapter = chapter;
  if (doc) state.selectedId = doc;
  if (archive === "1") state.includeArchived = true;

  if (q) {
    state.query = q;
    refs.searchInput.value = q;
  }

  if (locate) {
    refs.locatorInput.value = locate;
  }
}

function layerLabel(value) {
  if (value === "all") return "全部层级";
  if (value === "ROOT") return "根目录";
  return value;
}

function roleLabel(role) {
  return ROLE_LABELS[role] || role;
}

function chapterLabel(doc) {
  return doc.chapter || doc.stage || doc.topLevel;
}

function unique(values) {
  return [...new Set(values)];
}

function normalize(text) {
  return String(text || "").toLowerCase();
}

function buildTerms(text) {
  const normalized = normalize(text);
  const ascii = normalized.match(/[a-z0-9\-\+\.]{2,}/g) || [];
  const chinese = normalized.match(/[\u4e00-\u9fff]{2,}/g) || [];
  return unique([...ascii, ...chinese]).slice(0, 40);
}

function scoreKeywords(text, keywords) {
  const normalized = normalize(text);
  const hits = [];
  let score = 0;
  keywords.forEach((keyword) => {
    if (normalized.includes(normalize(keyword))) {
      hits.push(keyword);
      score += Math.max(2, keyword.length);
    }
  });
  return { score, hits };
}

function scoreDocument(doc, terms) {
  let score = 0;
  const hits = [];
  terms.forEach((term) => {
    if (doc.searchBlob.includes(term)) {
      score += Math.max(1, term.length);
      hits.push(term);
    }
  });
  return { score, hits: unique(hits) };
}

function filteredDocs() {
  return KB.docs
    .filter((doc) => (state.includeArchived ? true : !doc.archived))
    .filter((doc) => (state.layer === "all" ? true : doc.topLevel === state.layer))
    .filter((doc) => (state.role === "all" ? true : doc.role === state.role))
    .filter((doc) => (state.chapter ? doc.chapter === state.chapter : true))
    .filter((doc) => {
      if (!state.query) return true;
      return doc.searchBlob.includes(normalize(state.query));
    })
    .sort((a, b) => {
      if (a.retrievalTier !== b.retrievalTier) {
        return a.retrievalTier - b.retrievalTier;
      }
      return a.sortKey.localeCompare(b.sortKey, "zh-CN");
    });
}

function renderStats() {
  const chips = [
    `<span class="stat-chip">${KB.stats.documents} docs</span>`,
    `<span class="stat-chip">${KB.stats.chapters} chapters</span>`,
    `<span class="stat-chip">${KB.stats.archived} archived</span>`,
  ];
  refs.statsBar.innerHTML = chips.join("");
}

function renderFilters() {
  const layerOptions = [
    { value: "all", label: "全部层级" },
    ...KB.topLevelOrder
      .filter((name) => KB.stats.byTopLevel[name])
      .map((name) => ({ value: name, label: layerLabel(name) })),
  ];
  refs.layerFilter.innerHTML = layerOptions
    .map((option) => `<option value="${option.value}">${option.label}</option>`)
    .join("");

  const roleOptions = [{ value: "all", label: ROLE_LABELS.all }].concat(
    unique(KB.docs.map((doc) => doc.role))
      .sort()
      .map((role) => ({ value: role, label: roleLabel(role) })),
  );
  refs.roleFilter.innerHTML = roleOptions
    .map((option) => `<option value="${option.value}">${option.label}</option>`)
    .join("");
}

function renderStageTree() {
  const docs = filteredDocs();
  refs.resultCount.textContent = `${docs.length} 篇`;

  const groups = KB.topLevelOrder
    .filter((name) => KB.docs.some((doc) => doc.topLevel === name))
    .map((topLevel) => {
      const topLevelDocs = KB.docs.filter((doc) => doc.topLevel === topLevel && (state.includeArchived ? true : !doc.archived));
      const chapters = unique(topLevelDocs.map((doc) => doc.chapter).filter(Boolean)).sort((a, b) => a.localeCompare(b, "zh-CN"));
      return { topLevel, count: topLevelDocs.length, chapters };
    });

  refs.stageTree.innerHTML = groups
    .map((group) => {
      const chapterHtml = group.chapters.length
        ? group.chapters
            .map((chapter) => {
              const active = state.chapter === chapter ? "active" : "";
              return `<button class="tree-chip ${active}" type="button" data-chapter="${chapter}">${chapter}</button>`;
            })
            .join("")
        : `<span class="field-label">无章节号</span>`;
      return `
        <section class="stage-group">
          <h3 class="stage-title">
            <button class="tree-chip ${state.layer === group.topLevel ? "active" : ""}" type="button" data-layer="${group.topLevel}">
              ${layerLabel(group.topLevel)}
            </button>
            <span class="mono">${group.count}</span>
          </h3>
          <div class="chapter-tags">${chapterHtml}</div>
        </section>
      `;
    })
    .join("");

  refs.stageTree.querySelectorAll("[data-layer]").forEach((node) => {
    node.addEventListener("click", () => {
      state.layer = state.layer === node.dataset.layer ? "all" : node.dataset.layer;
      state.chapter = "";
      refs.layerFilter.value = state.layer;
      rerender();
    });
  });

  refs.stageTree.querySelectorAll("[data-chapter]").forEach((node) => {
    node.addEventListener("click", () => {
      state.chapter = state.chapter === node.dataset.chapter ? "" : node.dataset.chapter;
      rerender();
    });
  });
}

function renderDocList() {
  const docs = filteredDocs();
  if (!docs.length) {
    refs.docList.innerHTML = `<div class="empty-state">没有符合当前筛选条件的文档。</div>`;
    refs.previewPane.innerHTML = `<div class="empty-state">从左侧调整筛选或搜索条件。</div>`;
    return;
  }

  if (!state.selectedId || !docs.some((doc) => doc.id === state.selectedId)) {
    state.selectedId = docs[0].id;
  }

  refs.docList.innerHTML = docs
    .map((doc) => {
      const active = doc.id === state.selectedId ? "active" : "";
      const badges = [
        `<span class="badge">T${doc.retrievalTier}</span>`,
        doc.stage && `<span class="badge">${doc.stage}</span>`,
        doc.chapter && `<span class="badge">${doc.chapter}</span>`,
        `<span class="badge">${roleLabel(doc.role)}</span>`,
        doc.archived && `<span class="badge">归档</span>`,
      ]
        .filter(Boolean)
        .join("");
      return `
        <article class="doc-card ${active}" data-doc-id="${doc.id}">
          <div class="doc-meta-row">${badges}</div>
          <h3>${doc.title}</h3>
          <div class="mono">${doc.path}</div>
          <p>${doc.excerpt || "无摘要可用。"}</p>
        </article>
      `;
    })
    .join("");

  refs.docList.querySelectorAll("[data-doc-id]").forEach((node) => {
    node.addEventListener("click", () => {
      state.selectedId = node.dataset.docId;
      renderDocList();
      renderPreview();
    });
  });

  renderPreview();
}

function renderPreview() {
  const doc = KB.docs.find((item) => item.id === state.selectedId);
  if (!doc) {
    refs.previewPane.innerHTML = `<div class="empty-state">没有选中的文档。</div>`;
    return;
  }

  const badges = [
    `<span class="badge">T${doc.retrievalTier}</span>`,
    doc.stage && `<span class="badge">${doc.stage}</span>`,
    doc.chapter && `<span class="badge">${doc.chapter}</span>`,
    `<span class="badge emphasis">${roleLabel(doc.role)}</span>`,
    doc.archived && `<span class="badge">归档</span>`,
  ]
    .filter(Boolean)
    .join("");

  const metaRows = Object.entries(doc.meta)
    .map(
      ([key, value]) => `
        <div class="preview-meta-row">
          <span class="field-label">${key}</span>
          <span>${value}</span>
        </div>
      `,
    )
    .join("");

  refs.previewPane.innerHTML = `
    <h3>${doc.title}</h3>
    <div class="badge-row">${badges}</div>
    <a class="open-link mono" href="${encodeURI(doc.openPath)}" target="_blank" rel="noreferrer">${doc.path}</a>
    <div class="preview-meta">${metaRows || `<div class="empty-state">该文档前部暂无稳定元数据头。</div>`}</div>
    <p>${(doc.excerpt || "无摘要可用。").replace(/\n/g, "<br>")}</p>
  `;
}

function locateInput() {
  const input = refs.locatorInput.value.trim();
  if (!input) {
    refs.locatorOutput.textContent = "输入一段摘要或需求，系统会给出阶段/章节候选和相关文档。";
    refs.locatorOutput.className = "locator-output empty-state";
    return;
  }

  const schemaMatches = KB.locatorSchema
    .map((node) => {
      const { score, hits } = scoreKeywords(input, node.keywords || []);
      return { node, score, hits };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);

  const terms = buildTerms(input);
  const docMatches = KB.docs
    .filter((doc) => (state.includeArchived ? true : !doc.archived))
    .map((doc) => {
      const { score, hits } = scoreDocument(doc, terms);
      return { doc, score, hits };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      return a.doc.retrievalTier - b.doc.retrievalTier;
    })
    .slice(0, 6);

  refs.locatorOutput.className = "locator-output";
  refs.locatorOutput.innerHTML = `
    <div class="suggestion-card">
      <h3>章节候选</h3>
      ${
        schemaMatches.length
          ? schemaMatches
              .map(
                ({ node, hits }) => `
                  <p><strong>${node.title}</strong> · ${node.summary}</p>
                  <p class="mono">命中关键词: ${hits.join(", ")}</p>
                `,
              )
              .join("<hr>")
          : `<p>没有命中预设章节关键词，建议先查看阶段总纲与横切协议。</p>`
      }
    </div>
    <div class="suggestion-card">
      <h3>相关文档候选</h3>
      ${
        docMatches.length
          ? docMatches
              .map(
                ({ doc, hits }) => `
                  <p>
                    <a class="open-link" href="${encodeURI(doc.openPath)}" target="_blank" rel="noreferrer">${doc.title}</a>
                    <span class="mono"> T${doc.retrievalTier} · ${doc.path}</span>
                  </p>
                  <p class="mono">命中词: ${hits.slice(0, 8).join(", ") || "标题/摘要相关"}</p>
                `,
              )
              .join("<hr>")
          : `<p>当前没有直接命中的文档，建议先落到阶段级总纲再人工细分。</p>`
      }
    </div>
    <div class="suggestion-card">
      <h3>建议的 agent 落位字段</h3>
      <p class="mono">阶段候选 / 章节候选 / 共形维度 / 上游残差 / 下游出口</p>
    </div>
  `;
}

function bindEvents() {
  refs.searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim();
    rerender();
  });

  refs.layerFilter.addEventListener("change", (event) => {
    state.layer = event.target.value;
    state.chapter = "";
    rerender();
  });

  refs.roleFilter.addEventListener("change", (event) => {
    state.role = event.target.value;
    rerender();
  });

  refs.archiveToggle.addEventListener("change", (event) => {
    state.includeArchived = event.target.checked;
    rerender();
  });

  refs.locatorButton.addEventListener("click", locateInput);
}

function rerender() {
  renderStageTree();
  renderDocList();
}

function init() {
  applyUrlState();
  renderStats();
  renderFilters();
  refs.layerFilter.value = state.layer;
  refs.roleFilter.value = state.role;
  refs.archiveToggle.checked = state.includeArchived;
  bindEvents();
  rerender();
  if (refs.locatorInput.value.trim()) {
    locateInput();
  }
}

init();
