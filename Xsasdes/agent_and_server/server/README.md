Mock Decide Server (final modified) - README

Summary:
- Decision endpoint has a clear injection point for Gemini (commented in index.js).
- If Gemini is not configured, server falls back to a simple heuristic.
- Server does NOT execute system commands itself; the local agent executes OS commands when allowed.

Decision JSON schema:
{
  decision: "OK" | "DISTRACTION",
  action: "none" | "close_window" | "popup" | "hide",
  target: "<window title>",
  reason: "<explanation>",
  confidence: <0-100>,
  helpful_links: [ {title, url}, ... ]
}

See comments in index.js for Gemini injection pseudocode.
