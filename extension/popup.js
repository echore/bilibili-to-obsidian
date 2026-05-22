// extension/popup.js

// ─── Load + render saved settings ────────────────────────────────────────────
chrome.storage.local.get(
  { vault_name: "", folder: "Raw", output: "obsidian", model: "large-v3-turbo" },
  (s) => {
    document.getElementById("vault_name").value = s.vault_name;
    document.getElementById("folder").value = s.folder;
    document.getElementById("model").value = s.model;
    document.querySelectorAll("#output-seg button").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.value === s.output);
    });
  }
);

// ─── Save on any change ───────────────────────────────────────────────────────
function save() {
  const output =
    document.querySelector("#output-seg button.active")?.dataset.value ?? "obsidian";
  chrome.storage.local.set({
    vault_name: document.getElementById("vault_name").value.trim(),
    folder: document.getElementById("folder").value.trim(),
    output,
    model: document.getElementById("model").value,
  });
}

["vault_name", "folder", "model"].forEach((id) =>
  document.getElementById(id).addEventListener("change", save)
);

document.querySelectorAll("#output-seg button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("#output-seg button").forEach((b) =>
      b.classList.remove("active")
    );
    btn.classList.add("active");
    save();
  });
});

// ─── Auto-detect vault name from local server ─────────────────────────────────
document.getElementById("btn-detect").addEventListener("click", async () => {
  const btn = document.getElementById("btn-detect");
  btn.textContent = "检测中…";
  btn.disabled = true;
  try {
    const res = await fetch("http://localhost:27182/vaults", {
      signal: AbortSignal.timeout(2000),
    });
    if (!res.ok) throw new Error();
    const data = await res.json();
    if (data.vaults.length === 0) {
      btn.textContent = "未找到";
    } else {
      // Pick first vault; if multiple, user can manually adjust
      document.getElementById("vault_name").value = data.vaults[0].name;
      save();
      btn.textContent = "已检测 ✓";
    }
  } catch {
    btn.textContent = "需启动服务";
  } finally {
    btn.disabled = false;
    setTimeout(() => { btn.textContent = "自动检测"; }, 2000);
  }
});

// ─── Server health check ──────────────────────────────────────────────────────
(async () => {
  const dot = document.getElementById("dot");
  const label = document.getElementById("srv-label");
  try {
    const res = await fetch("http://localhost:27182/health", {
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) {
      dot.classList.add("ok");
      label.textContent = "本地服务运行中 · :27182";
    } else throw new Error();
  } catch {
    dot.classList.add("err");
    label.textContent = "本地服务未运行（CC 字幕仍可用）";
  }
})();
