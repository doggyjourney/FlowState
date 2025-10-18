#!/usr/bin/env python3
"""
FlowState 集成功能模拟测试
演示如何将 FlowState 与 TaskFocusMonitor 集成
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from test_mock import MockTaskFocusMonitor


class MockFlowStateBridge:
    """模拟 FlowState 桥接器"""
    
    def __init__(self):
        self.mock_tasks = [
            {
                "id": "task_1234567890_abc123",
                "name": "学习Python编程",
                "resources": [
                    {
                        "kind": "url",
                        "id": "https://docs.python.org",
                        "title": "Python官方文档"
                    },
                    {
                        "kind": "url", 
                        "id": "https://stackoverflow.com",
                        "title": "Stack Overflow"
                    },
                    {
                        "kind": "app",
                        "id": "vscode",
                        "title": "Visual Studio Code"
                    }
                ]
            },
            {
                "id": "task_2345678901_def456",
                "name": "写技术博客",
                "resources": [
                    {
                        "kind": "url",
                        "id": "https://github.com",
                        "title": "GitHub"
                    },
                    {
                        "kind": "url",
                        "id": "https://www.notion.so",
                        "title": "Notion笔记"
                    }
                ]
            },
            {
                "id": "task_3456789012_ghi789",
                "name": "准备考试复习",
                "resources": [
                    {
                        "kind": "url",
                        "id": "https://www.coursera.org",
                        "title": "Coursera课程"
                    },
                    {
                        "kind": "url",
                        "id": "https://www.khanacademy.org",
                        "title": "可汗学院"
                    }
                ]
            }
        ]
        
        self.mock_websites = [
            {
                "url": "https://docs.python.org/tutorial/",
                "title": "Python Tutorial - 官方教程",
                "app_id": "browser"
            },
            {
                "url": "https://www.youtube.com/watch?v=123",
                "title": "YouTube - Python学习视频",
                "app_id": "browser"
            },
            {
                "url": "https://stackoverflow.com/questions/123456",
                "title": "Stack Overflow - Python问题",
                "app_id": "browser"
            },
            {
                "url": "https://www.instagram.com",
                "title": "Instagram - 社交媒体",
                "app_id": "browser"
            },
            {
                "url": "https://github.com/user/repo",
                "title": "GitHub - 项目仓库",
                "app_id": "browser"
            }
        ]
    
    def get_current_task(self):
        """获取当前任务（模拟）"""
        import random
        return random.choice(self.mock_tasks)
    
    def get_current_website(self):
        """获取当前网站（模拟）"""
        import random
        return random.choice(self.mock_websites)
    
    def format_task_for_monitor(self, task):
        """格式化任务信息"""
        if not task:
            return "未知任务"
            
        task_name = task.get("name", "未知任务")
        resources = task.get("resources", [])
        
        description = f"任务: {task_name}"
        
        if resources:
            resource_descriptions = []
            for resource in resources[:5]:  # 只取前5个资源
                if resource.get("kind") == "url":
                    url = resource.get("id", "")
                    title = resource.get("title", "")
                    if title:
                        resource_descriptions.append(f"{title} ({url})")
                    else:
                        resource_descriptions.append(url)
                elif resource.get("kind") == "app":
                    app_id = resource.get("id", "")
                    title = resource.get("title", "")
                    if title:
                        resource_descriptions.append(f"{title} ({app_id})")
                    else:
                        resource_descriptions.append(app_id)
            
            if resource_descriptions:
                description += f"\n相关资源: {', '.join(resource_descriptions)}"
        
        return description
    
    def format_website_for_monitor(self, website):
        """格式化网站信息"""
        if not website:
            return "", ""
            
        url = website.get("url", "")
        title = website.get("title", "")
        app_id = website.get("app_id", "")
        
        description = ""
        if title:
            description = title
        if app_id and app_id != "browser":
            description += f" (应用: {app_id})"
            
        return url, description


def test_flowstate_bridge():
    """测试 FlowState 桥接器功能"""
    print("=" * 70)
    print("测试1: FlowState 桥接器功能")
    print("=" * 70)
    
    bridge = MockFlowStateBridge()
    
    # 测试获取任务
    print("1. 测试获取任务...")
    task = bridge.get_current_task()
    if task:
        print(f"   ✅ 成功获取任务: {task.get('name', 'N/A')}")
        print(f"   📋 任务ID: {task.get('id', 'N/A')}")
        print(f"   📦 资源数量: {len(task.get('resources', []))}")
    else:
        print("   ❌ 无法获取任务")
        return False
    
    # 测试获取网站
    print("\n2. 测试获取网站...")
    website = bridge.get_current_website()
    if website:
        print(f"   ✅ 成功获取网站: {website.get('title', 'N/A')}")
        print(f"   🌐 URL: {website.get('url', 'N/A')}")
        print(f"   💻 应用: {website.get('app_id', 'N/A')}")
    else:
        print("   ❌ 无法获取网站")
        return False
    
    # 测试格式化
    print("\n3. 测试数据格式化...")
    task_desc = bridge.format_task_for_monitor(task)
    url, desc = bridge.format_website_for_monitor(website)
    
    print(f"   📝 任务描述: {task_desc}")
    print(f"   🔗 网站URL: {url}")
    print(f"   📄 网站描述: {desc}")
    
    return True


def test_monitor_integration():
    """测试监控器集成功能"""
    print("\n" + "=" * 70)
    print("测试2: 监控器集成功能")
    print("=" * 70)
    
    try:
        monitor = MockTaskFocusMonitor()
        print("   ✅ 成功创建监控器")
        
        # 测试设置任务
        monitor.set_task("测试任务：学习Python编程")
        print("   ✅ 成功设置任务")
        
        # 测试检查网站
        result = monitor.check_website("https://docs.python.org", "Python官方文档")
        print("   ✅ 成功检查网站")
        print(f"   📊 结果: {'相关' if result['is_relevant'] else '无关'}")
        
        return True
    except Exception as e:
        print(f"   ❌ 监控器测试失败: {e}")
        return False


def test_full_integration():
    """测试完整集成功能"""
    print("\n" + "=" * 70)
    print("测试3: 完整集成功能")
    print("=" * 70)
    
    try:
        bridge = MockFlowStateBridge()
        monitor = MockTaskFocusMonitor()
        
        # 获取测试数据
        task = bridge.get_current_task()
        website = bridge.get_current_website()
        
        if not task or not website:
            print("   ❌ 无法获取测试数据")
            return False
        
        # 格式化数据
        task_description = bridge.format_task_for_monitor(task)
        url, description = bridge.format_website_for_monitor(website)
        
        print(f"   📝 任务: {task_description}")
        print(f"   🌐 网站: {url} - {description}")
        
        # 设置任务
        monitor.set_task(task_description)
        
        # 检查网站
        result = monitor.check_website(url, description if description else None)
        
        print("   ✅ 成功执行集成分析")
        print(f"   📊 分析结果: {'相关' if result['is_relevant'] else '无关'}")
        print(f"   🎯 置信度: {result['confidence']}")
        print(f"   💡 建议: {result['action']}")
        print(f"   📝 理由: {result['reason']}")
        
        return True
    except Exception as e:
        print(f"   ❌ 集成测试失败: {e}")
        return False


def test_workflow_simulation():
    """测试工作流程模拟"""
    print("\n" + "=" * 70)
    print("测试4: 工作流程模拟")
    print("=" * 70)
    
    print("🔄 模拟完整的 FlowState 集成工作流程:")
    print("1. FlowState 检测到用户切换任务")
    print("2. FlowState 检测到用户打开新网站")
    print("3. 桥接器获取任务和网站信息")
    print("4. 传递给 TaskFocusMonitor 进行分析")
    print("5. 返回专注度建议")
    print()
    
    bridge = MockFlowStateBridge()
    monitor = MockTaskFocusMonitor()
    
    # 模拟多个工作场景
    scenarios = [
        {
            "description": "用户开始学习Python编程",
            "task": bridge.mock_tasks[0],  # 学习Python编程
            "websites": [
                bridge.mock_websites[0],  # Python文档
                bridge.mock_websites[2],  # Stack Overflow
                bridge.mock_websites[1],  # YouTube
                bridge.mock_websites[3],  # Instagram
            ]
        },
        {
            "description": "用户开始写技术博客",
            "task": bridge.mock_tasks[1],  # 写技术博客
            "websites": [
                bridge.mock_websites[4],  # GitHub
                bridge.mock_websites[2],  # Stack Overflow
                bridge.mock_websites[1],  # YouTube
                bridge.mock_websites[3],  # Instagram
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario['description']}")
        print("-" * 50)
        
        # 设置任务
        task_desc = bridge.format_task_for_monitor(scenario['task'])
        monitor.set_task(task_desc)
        print(f"✅ 任务已设置: {scenario['task']['name']}")
        
        # 检查网站
        for j, website in enumerate(scenario['websites'], 1):
            url, desc = bridge.format_website_for_monitor(website)
            result = monitor.check_website(url, desc if desc else None)
            
            status = "✅" if result['is_relevant'] else "❌"
            print(f"   [{j}] {status} {url}")
            print(f"       理由: {result['reason']}")
        
        # 显示统计
        print()
        monitor.print_statistics()
    
    return True


def test_api_integration():
    """测试API集成"""
    print("\n" + "=" * 70)
    print("测试5: API集成测试")
    print("=" * 70)
    
    print("🔌 模拟API集成场景:")
    print("1. FlowState 作为数据源")
    print("2. TaskFocusMonitor 作为分析引擎")
    print("3. Web界面作为用户交互")
    print("4. 实时数据流和反馈")
    print()
    
    # 模拟API调用序列
    api_calls = [
        {
            "endpoint": "GET /flowstate/task",
            "description": "获取当前任务",
            "response": {"task": "学习Python编程", "resources": 3}
        },
        {
            "endpoint": "GET /flowstate/website", 
            "description": "获取当前网站",
            "response": {"url": "https://docs.python.org", "title": "Python文档"}
        },
        {
            "endpoint": "POST /monitor/check",
            "description": "检查网站相关性",
            "response": {"is_relevant": True, "confidence": "high"}
        },
        {
            "endpoint": "GET /monitor/stats",
            "description": "获取统计信息",
            "response": {"total": 1, "relevant": 1, "irrelevant": 0}
        }
    ]
    
    print("📡 API调用序列:")
    for i, call in enumerate(api_calls, 1):
        print(f"\n[{i}] {call['endpoint']}")
        print(f"    描述: {call['description']}")
        print(f"    响应: {json.dumps(call['response'], ensure_ascii=False)}")
        print("    ✅ 调用成功")
    
    print("\n🔄 数据流:")
    print("FlowState → 桥接器 → TaskFocusMonitor → Web界面 → 用户")
    print("    ↓         ↓           ↓            ↓        ↓")
    print("  任务数据   格式化      分析结果      UI更新   专注建议")
    
    return True


def main():
    """主测试函数"""
    print("🔗 FlowState 集成功能测试")
    print("=" * 70)
    print("这个测试演示了以下集成功能:")
    print("1. 🌉 数据桥接 - FlowState 到 TaskFocusMonitor")
    print("2. 🔄 工作流程 - 完整的集成工作流程")
    print("3. 📊 实时分析 - 任务和网站相关性分析")
    print("4. 🔌 API集成 - 多组件协作")
    print("=" * 70)
    
    # 运行测试
    tests = [
        ("FlowState桥接器功能", test_flowstate_bridge),
        ("监控器集成功能", test_monitor_integration),
        ("完整集成功能", test_full_integration),
        ("工作流程模拟", test_workflow_simulation),
        ("API集成测试", test_api_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n开始 {test_name}...")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果汇总
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("\n🎉 FlowState 集成功能测试全部通过！")
        print("\n📝 集成使用说明:")
        print("1. 确保 FlowState 正常运行")
        print("2. 设置 GROQ_API_KEY 环境变量")
        print("3. 运行 'python3 flowstate_integration.py'")
        print("4. 集成到你的工作流程中")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)