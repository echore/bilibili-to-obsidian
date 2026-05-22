// extension/background.js

chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    chrome.tabs.create({ url: chrome.runtime.getURL("welcome.html") });
  }
});

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "OPEN_WELCOME") {
    chrome.tabs.create({ url: chrome.runtime.getURL("welcome.html") });
  }
});
