# FlowState CLI (dev scaffold)

Minimal CLI for FlowState phase-1 (Developer B scope):
- Create tasks, learn used apps/URLs, and start resources.

## Install & build

```bash
cd flowstate
pnpm install
pnpm run build
```

Optional: run without build during dev:
```bash
pnpm run flow -- --help
```

## Usage

```bash
# create a task
node dist/cli.js task:create "写 AI 博客"

# list tasks
node dist/cli.js task:list

# learn resources for 10s (dev controller generates mock focus events)
node dist/cli.js task:learn <taskId> -d 10

# show task JSON
node dist/cli.js task:show <taskId>

# start the task (dev controller prints actions)
node dist/cli.js task:start <taskId>
```

Data is stored in `~/.flowstate/store.json`.

## Adapting to real system control (handoff to A)

- Implement `SystemController` in `src/learning.ts` using Smithery MCP to:
  - `openApp(appId)` and `openUrl(url)`
  - `subscribeActiveWindow(cb)` to stream focus events
- Replace `DevSystemController` with the real implementation at CLI bootstrap.

## Notes

- URL canonicalization strips hash and query to reduce duplicates.
- Learning session deduplicates by `kind:id`.
