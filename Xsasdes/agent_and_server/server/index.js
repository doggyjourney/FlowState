/*
mock_decide_server/index.js
Final modified version:
 - Keeps Gemini injection comments (server will call Gemini if configured)
 - Fallback heuristic: blacklist/whitelist + token-overlap
 - Does NOT execute system commands itself (agent handles execution)
*/
const express = require('express');
const app = express();
app.use(express.json());
const port = process.env.PORT || 4000;

const BLACKLIST = ['twitter','youtube','facebook','instagram','tiktok','reddit','netflix'];
const WHITELIST = ['vscode','code','visual studio','pycharm','sublime','terminal','iterm','xcode','idea','stack overflow','stackexchange','docs.google','notion','stackoverflow'];
const OVERLAP_THRESHOLD = 0.25; // 25%

function normalize(s) {
  if(!s) return '';
  return s.toLowerCase().replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
}
function tokens(s) {
  return normalize(s).split(' ').filter(Boolean);
}
function overlapScore(goal, title) {
  const g = new Set(tokens(goal));
  const t = tokens(title);
  if (!g.size || !t.length) return 0;
  let common = 0;
  for (const tok of t) if (g.has(tok)) common++;
  return common / Math.max(g.size, t.length);
}

app.post('/api/tasks', (req, res) => {
  const body = req.body || {};
  const task = {
    task_id: "task_final_001",
    main_goal: body.main_goal || "demo goal",
    status: "running",
    created_at: new Date().toISOString(),
    helpful_links: []
  };
  res.status(201).json(task);
});

app.get('/api/tasks/latest', (req, res) => {
  res.json({
    task_id: "task_final_001",
    main_goal: "Fix Bug #105",
    status: "running",
    helpful_links: [],
    last_decision: null
  });
});

/* Gemini injection point (commented)
   ---------------------------------
   If GEMINI is configured, replace the heuristic by calling Gemini here.
   Pseudocode:
   if (process.env.GEMINI_API_KEY) {
     // call Gemini with system prompt that requires STRICT JSON output matching schema
     // parse response into resultJson
     // if parse OK -> return res.json(resultJson)
     // else fall through to heuristic
   }
   See project docs for full integration steps.
   ---------------------------------
*/

app.post('/api/decide', async (req, res) => {
  const body = req.body || {};
  const main_goal = body.main_goal || '';
  const window_title = body.window_title || '';
  const normTitle = normalize(window_title);

  // Fallback heuristic:
  for (const bad of BLACKLIST) {
    if (normTitle.includes(bad)) {
      return res.json({
        decision: 'DISTRACTION',
        action: 'close_window',
        target: window_title,
        reason: `Detected blacklisted app/domain: ${bad}`,
        confidence: 95,
        helpful_links: []
      });
    }
  }

  for (const good of WHITELIST) {
    if (normTitle.includes(good)) {
      return res.json({
        decision: 'OK',
        action: 'none',
        target: window_title,
        reason: `Whitelist matched: ${good}`,
        confidence: 90,
        helpful_links: []
      });
    }
  }

  const score = overlapScore(main_goal, window_title);
  if (score >= OVERLAP_THRESHOLD) {
    return res.json({
      decision: 'OK',
      action: 'none',
      target: window_title,
      reason: `Token overlap between goal and window (${(score*100).toFixed(0)}%)`,
      confidence: Math.min(85, 60 + Math.floor(score*40)),
      helpful_links: main_goal ? [{ title: 'Sample Help', url: 'https://example.com' }] : []
    });
  }

  return res.json({
    decision: 'DISTRACTION',
    action: 'close_window',
    target: window_title,
    reason: `Low token overlap (${(score*100).toFixed(0)}%) with goal`,
    confidence: Math.max(55, 70 - Math.floor(score*40)),
    helpful_links: main_goal ? [{ title: 'Documentation', url: 'https://example.com/docs' }] : []
  });
});

app.post('/api/tasks/:taskId/decisions', (req, res) => {
  console.log('Decision log received for', req.params.taskId, JSON.stringify(req.body));
  res.json({ ok: true });
});

app.listen(port, () => {
  console.log(`Mock Decide Server listening at http://localhost:${port}`);
});
