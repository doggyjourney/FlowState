#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FlowState Website Checker - API Backend
- 接收浏览器或 FlowState 上报的网站日志
- 自动获取当前任务（或接受外部传入的任务）
- 使用 TaskFocusMonitor 判断网站是否与当前任务有关
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from flask import Flask, request, jsonify
try:
    from flask_cors import CORS
    _has_cors = True
except Exception:
    _has_cors = False

from task_focus_monitor import TaskFocusMonitor
from flowstate_bridge import FlowStateBridge

app = Flask(__name__)
if _has_cors:
    CORS(app)

monitor = TaskFocusMonitor()         # 依赖环境变量 GROQ_API_KEY
bridge = FlowStateBridge()           # 依赖 ../flowstate/dist/cli.js 可用（npm run build）
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

EVENT_LOG = LOG_DIR / "website_events.jsonl"
RESULT_LOG = LOG_DIR / "classification_results.jsonl"


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[WARN] 写入日志失败 {path}: {e}")


@app.get("/health")
def health():
    return jsonify({"ok": True, "time": _now_iso()}), 200


@app.post("/classify_website")
def classify_website():
    """
    请求体示例（两种都支持）：
    1) 仅传网站，由后端自动从 FlowState 获取当前任务
    {
      "website": { "url": "https://example.com", "title": "Example", "app_id": "browser" },
      "client_time": "2025-10-18T10:00:00Z" // 可选
    }

    2) 同时传任务与网站（任务来自 FlowState 侧）
    {
      "task": {
        "id": "task_123",
        "name": "学习Python编程",
        "resources": [
          { "kind": "url", "id": "https://docs.python.org", "title": "Python 文档" }
        ]
      },
      "website": { "url": "https://stackoverflow.com", "title": "Stack Overflow", "app_id": "browser" }
    }
    """
    data = request.get_json(silent=True) or {}

    # 容错解析 website
    website = data.get("website")
    if website is None:
        # 兼容简化传参：直接传 url/title/app_id 在根级
        url = data.get("url")
        title = data.get("title")
        app_id = data.get("app_id", "browser")
        if url:
            website = {"url": url, "title": title or "", "app_id": app_id}
    if not website or not website.get("url"):
        return jsonify({"ok": False, "error": "missing website.url"}), 400

    # 任务：优先用外部传入，否则从 FlowState 拉取当前任务
    task = data.get("task")
    if task is None:
        task = bridge.get_current_task()

    if not task:
        return jsonify({"ok": False, "error": "no active task found from FlowState, and no task provided"}), 400

    # 记录原始事件
    event_record = {
        "received_at": _now_iso(),
        "client_time": data.get("client_time"),
        "task_brief": {"id": task.get("id"), "name": task.get("name")},
        "website": website,
        "source": data.get("source", "unknown")  # 比如 "chrome-extension", "flowstate-cli"
    }
    _append_jsonl(EVENT_LOG, event_record)

    # 判定
    try:
        result = monitor.check_from_flowstate(task, website)
    except Exception as e:
        return jsonify({"ok": False, "error": f"classify failed: {e}"}), 500

    # 记录判定结果
    result_record = {
        "timestamp": _now_iso(),
        "task": {"id": task.get("id"), "name": task.get("name")},
        "website": website,
        "result": result,
    }
    _append_jsonl(RESULT_LOG, result_record)

    return jsonify({
        "ok": True,
        "is_relevant": result["is_relevant"],
        "action": result["action"],
        "confidence": result["confidence"],
        "reason": result["reason"]
    }), 200


@app.get("/stats")
def stats():
    """
    简单会话内统计（基于 monitor.check_history）
    """
    hist = monitor.get_history() if hasattr(monitor, "get_history") else []
    total = len(hist)
    relevant = sum(1 for h in hist if h.get("result", {}).get("is_relevant"))
    return jsonify({
        "ok": True,
        "total_checks": total,
        "relevant": relevant,
        "irrelevant": total - relevant
    }), 200


if __name__ == "__main__":
    print("=" * 70)
    print("FlowState Website Checker - API Backend")
    print("=" * 70)
    port = int(os.environ.get("WEBCHECKER_PORT", "5001"))
    host = os.environ.get("WEBCHECKER_HOST", "127.0.0.1")
    print(f"Listening on http://{host}:{port}")
    print("CTRL+C to stop")
    app.run(debug=True, host=host, port=port)
