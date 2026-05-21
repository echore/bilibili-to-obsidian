// extension/background.js
chrome.runtime.onInstalled.addListener(() => {
  console.log("[Bili Clipper] Installed");
});

// All localhost:27182 communication goes through here.
// Content scripts on https:// pages can reach http://localhost directly,
// but centralising here keeps server I/O in one place for easier maintenance.
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "HEALTH_CHECK") {
    fetch("http://localhost:27182/health", { signal: AbortSignal.timeout(2000) })
      .then((res) => sendResponse({ ok: res.ok }))
      .catch(() => sendResponse({ ok: false }));
    return true;
  }

  if (message.type === "CLIP") {
    fetch("http://localhost:27182/clip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(message.payload),
    })
      .then(async (res) => {
        const data = await res.json();
        sendResponse({ ok: res.ok, data });
      })
      .catch((err) => sendResponse({ ok: false, error: err.message }));
    return true;
  }
});
