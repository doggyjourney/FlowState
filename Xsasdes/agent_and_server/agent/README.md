Agent - README (final modified)

Behavior:
- Polls /api/tasks/latest
- Reads active window and sends to /api/decide when window changes or >= MIN_SEND_INTERVAL_MS passed
- Executes direct OS close commands only if ALLOW_DIRECT_KILL=true and app is in CLOSABLE_APPS
- Safety: requires 2 consecutive DISTRACTION or confidence >=80 to close; otherwise popup

Enable direct kill (CAUTION):
export ALLOW_DIRECT_KILL=true
export CLOSABLE_APPS="chrome,google chrome,firefox,edge,safari"

Testing:
- Use MOCK_WINDOW_TITLE to simulate:
export MOCK_WINDOW_TITLE="Twitter - Home"
npm start
