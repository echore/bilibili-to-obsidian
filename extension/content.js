// extension/content.js

// ─── Bilibili API helpers ────────────────────────────────────────────────────

/** Extract BV ID from current URL, e.g. /video/BV1xx411c7mD → "BV1xx411c7mD" */
function getBvId() {
  const match = window.location.pathname.match(/\/video\/(BV[a-zA-Z0-9]+)/);
  return match ? match[1] : null;
}

/** Fetch video metadata: { aid, cid, title } */
async function getVideoInfo(bvid) {
  const res = await fetch(
    `https://api.bilibili.com/x/web-interface/view?bvid=${bvid}`,
    { credentials: "include" }
  );
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Bilibili API error: ${data.message}`);
  return {
    aid: data.data.aid,
    cid: data.data.cid,
    title: data.data.title,
  };
}

/** Returns array of subtitle objects from player wbi/v2 API.
 *  Uses aid (numeric) + cid — NOT bvid.
 *  Filters out entries with empty subtitle_url.
 */
async function getSubtitleList(aid, cid) {
  const res = await fetch(
    `https://api.bilibili.com/x/player/wbi/v2?aid=${aid}&cid=${cid}`,
    { credentials: "include" }
  );
  const data = await res.json();
  const subtitles = data.data?.subtitle?.subtitles ?? [];
  return subtitles.filter((s) => s.subtitle_url);
}

/** Fetch subtitle JSON and return full transcript as plain text.
 *  Handles http:// → https:// conversion.
 */
async function fetchSubtitleText(subtitleUrl) {
  const url = subtitleUrl.startsWith("http://")
    ? subtitleUrl.replace("http://", "https://")
    : subtitleUrl.startsWith("//")
    ? "https:" + subtitleUrl
    : subtitleUrl;
  const res = await fetch(url, { credentials: "include" });
  const data = await res.json();
  return data.body.map((item) => item.content).join("\n");
}

/** Ping the local server. Returns true if running. */
async function isServerRunning() {
  try {
    const res = await fetch("http://localhost:27182/health", {
      signal: AbortSignal.timeout(2000),
    });
    return res.ok;
  } catch {
    return false;
  }
}

/** Get settings from chrome.storage.local with defaults. */
async function getSettings() {
  return new Promise((resolve) => {
    chrome.storage.local.get(
      {
        vault_path: "~/Documents/Obsidian Vault",
        folder: "Raw",
        output: "obsidian",
        model: "large-v3-turbo",
      },
      resolve
    );
  });
}
