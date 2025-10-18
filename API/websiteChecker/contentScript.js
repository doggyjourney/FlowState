// 在页面顶部渲染提示条（仅当 showBanner 为 true 时，背景会发消息过来）
let bannerEl = null;

function ensureBanner() {
  if (bannerEl) return bannerEl;
  bannerEl = document.createElement("div");
  bannerEl.id = "__flowstate_banner__";
  bannerEl.style.cssText = `
    position: fixed;
    top: 0; left: 0; right: 0; z-index: 2147483647;
    display: none;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    padding: 10px 16px;
    color: #111;
    box-shadow: 0 2px 8px rgba(0,0,0,.15);
  `;
  const text = document.createElement("span");
  text.id = "__flowstate_banner_text__";
  text.style.marginRight = "12px";

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "关闭";
  closeBtn.style.cssText = `
    background: transparent; border: 1px solid rgba(0,0,0,.2);
    padding: 4px 10px; border-radius: 6px; cursor: pointer;
  `;
  closeBtn.addEventListener("click", () => {
    bannerEl.style.display = "none";
  });

  const allowBtn = document.createElement("button");
  allowBtn.textContent = "本次忽略";
  allowBtn.style.cssText = `
    margin-left: 8px;
    background: #e0f3e6; border: 1px solid #3aa76d; color: #0d6832;
    padding: 4px 10px; border-radius: 6px; cursor: pointer;
  `;
  allowBtn.addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "FLOWSTATE_OVERRIDE_ALLOW", url: location.href });
    bannerEl.style.display = "none";
  });

  bannerEl.appendChild(text);
  bannerEl.appendChild(allowBtn);
  bannerEl.appendChild(closeBtn);
  document.documentElement.appendChild(bannerEl);
  return bannerEl;
}

function showBanner(result) {
  const el = ensureBanner();
  const textEl = el.querySelector("#__flowstate_banner_text__");

  if (result.is_relevant) {
    el.style.background = "#d4edda";
    el.style.borderBottom = "3px solid #28a745";
    textEl.textContent = `✓ 与当前任务相关（置信度：${result.confidence}）。理由：${result.reason || "N/A"}`;
  } else {
    el.style.background = "#f8d7da";
    el.style.borderBottom = "3px solid #dc3545";
    textEl.textContent = `✗ 与当前任务无关（置信度：${result.confidence}）。理由：${result.reason || "N/A"}`;
  }
  el.style.display = "block";
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg?.type === "FLOWSTATE_CLASSIFICATION") {
    showBanner(msg.result);
  }
});
