// agent/index.js
// Behavior:
// - Polls /api/tasks/latest to get task
// - Reads active window every loop
// - Sends to /api/decide only when window changed OR >= MIN_SEND_INTERVAL_MS passed (default 60s)
// - Performs close via OS command if ALLOW_DIRECT_KILL=true and safety checks pass

const fetch = require('node-fetch');
const { exec } = require('child_process');
require('dotenv').config();
let activeWin;
try { activeWin = require('active-win'); } catch (e) { activeWin = null; }

const DECIDE_URL = process.env.DECIDE_URL || 'http://localhost:4000/api/decide';
const TASKS_URL = process.env.TASKS_URL || 'http://localhost:4000/api/tasks/latest';
const POLL_INTERVAL = parseInt(process.env.POLL_INTERVAL || '5000', 10);
const MIN_SEND_INTERVAL_MS = parseInt(process.env.MIN_SEND_INTERVAL_MS || '60000', 10);
const ALLOW_DIRECT_KILL = (process.env.ALLOW_DIRECT_KILL === 'true');
const CLOSABLE_APPS = (process.env.CLOSABLE_APPS || 'chrome,google chrome,firefox,edge,safari').split(',');

let lastWindow = null;
let lastSentTime = 0;
let consecutiveDistract = {};

async function getActiveWindowTitle() {
  if (process.env.MOCK_WINDOW_TITLE) return process.env.MOCK_WINDOW_TITLE;
  if (!activeWin) return "Unknown (active-win not installed)";
  try {
    const info = await activeWin();
    return (info && info.title) ? info.title : (info && info.owner && info.owner.name) ? info.owner.name : "Unknown";
  } catch (e) {
    console.error('active-win error:', e.message || e);
    return "Unknown";
  }
}

async function getLatestTask() {
  try {
    const r = await fetch(TASKS_URL);
    if (r.status === 200) return await r.json();
    return null;
  } catch (e) {
    console.error('Error fetching latest task:', e.message);
    return null;
  }
}

async function postDecisionLog(taskId, decision, performed) {
  try {
    await fetch(`http://localhost:4000/api/tasks/${taskId}/decisions`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ timestamp: new Date().toISOString(), decision, performed })
    });
  } catch (e) {
    console.error('Error posting decision log:', e.message);
  }
}

function buildCloseCmd(ownerName) {
  const os = process.platform;
  const name = (ownerName || '').toLowerCase();
  if (os === 'darwin') {
    // macOS: tell application to quit
    return `osascript -e 'tell application "${ownerName.replace(/"/g,"'")}" to quit'`;
  } else if (os === 'win32') {
    if (name.includes('chrome')) return 'taskkill /IM chrome.exe /F';
    if (name.includes('firefox')) return 'taskkill /IM firefox.exe /F';
    if (name.includes('edge')) return 'taskkill /IM msedge.exe /F';
    // fallback: try to kill by window title (may require admin)
    return `taskkill /FI "WINDOWTITLE eq ${ownerName}" /F`;
  } else {
    if (name.includes('chrome')) return 'pkill -f chrome || true';
    if (name.includes('firefox')) return 'pkill -f firefox || true';
    return `pkill -f "${ownerName}" || true`;
  }
}

async function performAction(decision, task, ownerName) {
  if (!decision) return { status: 'no-op' };
  if (decision.action === 'close_window') {
    // safety checks
    const allowed = ALLOW_DIRECT_KILL && ownerName && CLOSABLE_APPS.some(p => ownerName.toLowerCase().includes(p.toLowerCase()));
    if (!allowed) {
      console.log('[SIMULATE] Close requested for', ownerName, '- simulation only (ALLOW_DIRECT_KILL not enabled or app not allowed).');
      return { status: 'simulated', action_result: 'popup_shown_instead' };
    }
    const cmd = buildCloseCmd(ownerName);
    console.log('[EXEC] Running:', cmd);
    return new Promise(resolve => {
      exec(cmd, (error, stdout, stderr) => {
        if (error) {
          console.error('Close failed:', stderr || error.message);
          resolve({ status: 'error', action_result: 'close_failed', details: stderr || error.message });
        } else {
          console.log('Close succeeded:', stdout || '');
          resolve({ status: 'ok', action_result: 'closed' });
        }
      });
    });
  } else if (decision.action === 'popup') {
    console.log('[SIMULATE] Popup:', decision.reason);
    return { status: 'simulated', action_result: 'popup_shown' };
  } else {
    console.log('[SIMULATE] OK - no action.');
    return { status: 'simulated', action_result: 'none' };
  }
}

async function mainLoop() {
  console.log('Agent start. Poll interval:', POLL_INTERVAL, 'ms. Min send:', MIN_SEND_INTERVAL_MS, 'ms');
  while (true) {
    const task = await getLatestTask();
    if (!task) { await new Promise(r => setTimeout(r, POLL_INTERVAL)); continue; }
    const window_title = await getActiveWindowTitle();
    const now = Date.now();
    const shouldSend = (window_title !== lastWindow) || ((now - lastSentTime) >= MIN_SEND_INTERVAL_MS);
    if (!shouldSend) { await new Promise(r => setTimeout(r, POLL_INTERVAL)); continue; }
    console.log('Sending to decide:', window_title);
    try {
      const resp = await fetch(DECIDE_URL, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ task_id: task.task_id, main_goal: task.main_goal, window_title }) });
      const decision = await resp.json();
      console.log('Decision:', decision);
      const key = task.task_id || 'task_demo';
      if (decision.decision === 'DISTRACTION') consecutiveDistract[key] = (consecutiveDistract[key] || 0) + 1;
      else consecutiveDistract[key] = 0;
      const shouldForceClose = (consecutiveDistract[key] >= 2) || (decision.confidence && decision.confidence >= 80);
      if (decision.action === 'close_window' && !shouldForceClose) {
        console.log('Downgrading to popup due to safety.');
        decision.action = 'popup';
        decision.reason = '(downgraded to popup) ' + decision.reason;
      }
      // attempt to derive ownerName
      let ownerName = window_title;
      try {
        if (activeWin) {
          const info = await activeWin();
          ownerName = (info && info.owner && info.owner.name) ? info.owner.name : window_title;
        }
      } catch (e) {}
      const performed = await performAction(decision, task, ownerName);
      await postDecisionLog(task.task_id, decision, performed);
    } catch (e) {
      console.error('Error calling decide:', e.message || e);
    }
    lastWindow = window_title;
    lastSentTime = Date.now();
    await new Promise(r => setTimeout(r, POLL_INTERVAL));
  }
}

mainLoop();
