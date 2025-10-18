// FlowState Website Logger - background (MV3 service worker)
const DEFAULT_ENDPOINT = "http://localhost:5001/classify_website";
const DEFAULT_SETTINGS = {
  endpoint: DEFAULT_ENDPOINT,
  showBanner: true,   // 是否在页面顶部展示提示条
  autoClose: false    // 是否自动关闭/跳转无关页面
};

const state = {
  cache: new Map() // key: `${tabId}|${url}` -> result
};

function getSettings() {
  return new Promise(resolve => {
    chrome.storage.sync.get(DEFAULT_SETTINGS, resolve);
  });
}

function cacheKey(tabId, url) {
  return `${tabId}|${url}`;
}

async function classifyAndAct(tabId, url, title) {
  if (!/^https?:\/\//i.test(url)) return; // 排除非 http(s)

  const key = cacheKey(tabId, url);
  if (state.cache.has(key)) {
    const cached = state.cache.get(key);
    notifyContent(tabId, url, cached);
    await maybeActOnResult(tabId, url, title, cached);
    return;
  }

  const settings = await getSettings();
  const payload = {
    website: { url, title: title || "", app_id: "browser" },
    client_time: new Date().toISOString(),
    source: "chrome-extension"
  };

  try {
    const res = await fetch(settings.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || "API not ok");

    const result = {
      is_relevant: !!data.is_relevant,
      action: data.action || (data.is_relevant ? "allow" : "block"),
      confidence: data.confidence || "medium",
      reason: data.reason || ""
    };

    state.cache.set(key, result);
    notifyContent(tabId, url, result);
    await maybeActOnResult(tabId, url, title, result);
  } catch (e) {
    console.warn("[FlowState] classify failed:", e);
  }
}

function notifyContent(tabId, url, result) {
  chrome.tabs.sendMessage(tabId, {
    type: "FLOWSTATE_CLASSIFICATION",
    url,
    result
  }).catch(() => {
    // content script 可能尚未注入
  });
}

async function maybeActOnResult(tabId, url, title, result) {
  const settings = await getSettings();

  if (settings.showBanner) {
    notifyContent(tabId, url, result);
  }

  if (settings.autoClose && result.action === "block" && !result.is_relevant) {
    const focusUrl = chrome.runtime.getURL(
      `focus.html?u=${encodeURIComponent(url)}&t=${encodeURIComponent(title || "")}&r=${encodeURIComponent(result.reason || "")}`
    );
    try {
      await chrome.tabs.update(tabId, { url: focusUrl });
    } catch (e) {
      await chrome.tabs.remove(tabId);
    }
  }
}

chrome.webNavigation.onCommitted.addListener(async (details) => {
  if (details.frameId !== 0) return;
  try {
    const tab = await chrome.tabs.get(details.tabId);
    if (!tab || !tab.url) return;
    classifyAndAct(details.tabId, tab.url, tab.title);
  } catch (e) {
    console.warn("[FlowState] onCommitted failed", e);
  }
});

chrome.webNavigation.onHistoryStateUpdated.addListener(async (details) => {
  if (details.frameId !== 0) return;
  try {
    const tab = await chrome.tabs.get(details.tabId);
    if (!tab || !tab.url) return;
    classifyAndAct(details.tabId, tab.url, tab.title);
  } catch (e) {
    console.warn("[FlowState] onHistoryStateUpdated failed", e);
  }
});

chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    if (!tab || !tab.url) return;
    classifyAndAct(activeInfo.tabId, tab.url, tab.title);
  } catch (e) {
    console.warn("[FlowState] onActivated failed", e);
  }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === "FLOWSTATE_OVERRIDE_ALLOW" && sender.tab?.id) {
    const key = cacheKey(sender.tab.id, msg.url || sender.tab.url || "");
    state.cache.set(key, { is_relevant: true, action: "allow", confidence: "high", reason: "User override" });
    sendResponse({ ok: true });
    return true;
  }
});
