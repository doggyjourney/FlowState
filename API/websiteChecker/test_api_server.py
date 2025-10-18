#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 后端测试（基于 pytest）
- 覆盖 /health, /classify_website（缺参/自动任务/显式任务）, /stats
- 使用 monkeypatch 拦截 FlowStateBridge 与 TaskFocusMonitor，避免真实外部依赖
运行：
    pip install pytest
    pytest -q API/websiteChecker/test_api_server.py
前置：
    需要存在 API/websiteChecker/api_server.py
"""

import importlib
import sys
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def api():
    # 确保可以 import 到 api_server.py 与同目录模块
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        mod = importlib.import_module("api_server")
        return mod
    except ImportError:
        pytest.skip("未找到 api_server.py，请先添加 API 后端实现后再运行测试。")


@pytest.fixture()
def client(api, monkeypatch, tmp_path):
    # 启用测试模式
    api.app.config["TESTING"] = True

    # 重定向日志目录到临时目录
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(api, "LOG_DIR", log_dir, raising=False)
    monkeypatch.setattr(api, "EVENT_LOG", log_dir / "website_events.jsonl", raising=False)
    monkeypatch.setattr(api, "RESULT_LOG", log_dir / "classification_results.jsonl", raising=False)

    # 打桩 FlowStateBridge.get_current_task
    fake_task = {
        "id": "task_1",
        "name": "学习Python编程",
        "resources": [{"kind": "url", "id": "https://docs.python.org", "title": "Python 文档"}],
    }
    monkeypatch.setattr(api.bridge, "get_current_task", lambda: fake_task, raising=True)

    # 打桩 TaskFocusMonitor.check_from_flowstate
    def fake_check_from_flowstate(task, website):
        url = (website or {}).get("url", "")
        if "youtube.com" in url:
            return {
                "is_relevant": False,
                "action": "block",
                "reason": "娱乐网站",
                "confidence": "high",
            }
        if "python" in url:
            return {
                "is_relevant": True,
                "action": "allow",
                "reason": "学习资源",
                "confidence": "high",
            }
        return {
            "is_relevant": False,
            "action": "block",
            "reason": "不相关",
            "confidence": "medium",
        }

    monkeypatch.setattr(api.monitor, "check_from_flowstate", fake_check_from_flowstate, raising=True)

    return api.app.test_client(), api


def test_health_ok(client):
    c, _ = client
    resp = c.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert "time" in data


def test_classify_missing_website_url(client):
    c, _ = client
    # 1) 完全没有 website
    resp1 = c.post("/classify_website", json={})
    assert resp1.status_code == 400
    # 2) website 无 url
    resp2 = c.post("/classify_website", json={"website": {"title": "no url"}})
    assert resp2.status_code == 400


def test_classify_uses_bridge_task_when_task_not_provided(client):
    c, api = client
    payload = {
        "website": {"url": "https://docs.python.org/tutorial/", "title": "Python Tutorial", "app_id": "browser"},
        "client_time": "2025-10-18T10:00:00Z",
        "source": "pytest",
    }
    resp = c.post("/classify_website", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["is_relevant"] is True
    assert data["action"] == "allow"
    assert data["confidence"] in {"high", "medium", "low"}
    # 验证日志文件写入
    assert api.EVENT_LOG.exists()
    assert api.RESULT_LOG.exists()
    assert api.EVENT_LOG.read_text(encoding="utf-8").strip() != ""
    assert api.RESULT_LOG.read_text(encoding="utf-8").strip() != ""


def test_classify_respects_explicit_task_over_bridge(client, monkeypatch):
    c, api = client

    captured = {}

    def capturing_check(task, website):
        captured["task"] = task
        captured["website"] = website
        return {
            "is_relevant": False,
            "action": "block",
            "reason": "自定义任务下不相关",
            "confidence": "high",
        }

    monkeypatch.setattr(api.monitor, "check_from_flowstate", capturing_check, raising=True)

    explicit_task = {
        "id": "task_explicit",
        "name": "准备技术博客",
        "resources": [{"kind": "url", "id": "https://github.com", "title": "GitHub"}],
    }
    payload = {
        "task": explicit_task,
        "website": {"url": "https://www.youtube.com/watch?v=123", "title": "YouTube 视频", "app_id": "browser"},
        "source": "pytest",
    }
    resp = c.post("/classify_website", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["is_relevant"] is False
    assert captured["task"]["id"] == "task_explicit"
    assert "youtube" in captured["website"]["url"]


def test_stats_reflects_history(client, monkeypatch):
    c, api = client

    fake_history = [
        {"result": {"is_relevant": True}},
        {"result": {"is_relevant": False}},
        {"result": {"is_relevant": True}},
    ]
    monkeypatch.setattr(api.monitor, "get_history", lambda: fake_history, raising=True)

    resp = c.get("/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["total_checks"] == 3
    assert data["relevant"] == 2
    assert data["irrelevant"] == 1
