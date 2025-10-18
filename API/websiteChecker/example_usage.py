#!/usr/bin/env python3
"""
FlowState 集成使用示例
演示如何使用 FlowState 和 TaskFocusMonitor 的集成功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from flowstate_bridge import FlowStateBridge
from task_focus_monitor import TaskFocusMonitor


def example_basic_usage():
    """基本使用示例"""
    print("=" * 70)
    print("基本使用示例")
    print("=" * 70)
    
    # 1. 创建桥接器
    bridge = FlowStateBridge()
    
    # 2. 获取当前任务（模拟数据）
    print("1. 获取当前任务...")
    mock_task = {
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
            }
        ]
    }
    print(f"   任务: {mock_task['name']}")
    print(f"   资源数量: {len(mock_task['resources'])}")
    
    # 3. 获取当前网站（模拟数据）
    print("\n2. 获取当前网站...")
    mock_website = {
        "url": "https://docs.python.org/tutorial/",
        "title": "Python Tutorial - 官方教程",
        "app_id": "browser"
    }
    print(f"   网站: {mock_website['title']}")
    print(f"   URL: {mock_website['url']}")
    
    # 4. 创建监控器
    print("\n3. 创建专注度监控器...")
    try:
        monitor = TaskFocusMonitor()
        print("   ✅ 监控器创建成功")
    except Exception as e:
        print(f"   ❌ 监控器创建失败: {e}")
        print("   💡 提示: 需要设置 GROQ_API_KEY 环境变量")
        return
    
    # 5. 格式化数据
    print("\n4. 格式化数据...")
    task_description = bridge.format_task_for_monitor(mock_task)
    url, description = bridge.format_website_for_monitor(mock_website)
    print(f"   任务描述: {task_description}")
    print(f"   网站信息: {url} | {description}")
    
    # 6. 进行分析
    print("\n5. 进行专注度分析...")
    try:
        result = monitor.check_from_flowstate(mock_task, mock_website)
        print("   ✅ 分析完成")
        print(f"   判断: {'相关' if result['is_relevant'] else '无关'}")
        print(f"   置信度: {result['confidence']}")
        print(f"   建议: {result['action']}")
        print(f"   理由: {result['reason']}")
    except Exception as e:
        print(f"   ❌ 分析失败: {e}")
        print("   💡 提示: 需要有效的 GROQ_API_KEY 和网络连接")


def example_monitoring_loop():
    """监控循环示例"""
    print("\n" + "=" * 70)
    print("监控循环示例")
    print("=" * 70)
    
    print("模拟监控循环（每5秒检查一次）:")
    print("按 Ctrl+C 停止")
    
    import time
    
    # 模拟数据
    mock_tasks = [
        {
            "id": "task_1",
            "name": "学习Python编程",
            "resources": [{"kind": "url", "id": "https://docs.python.org", "title": "Python文档"}]
        },
        {
            "id": "task_2", 
            "name": "写技术博客",
            "resources": [{"kind": "url", "id": "https://github.com", "title": "GitHub"}]
        }
    ]
    
    mock_websites = [
        {"url": "https://docs.python.org/tutorial/", "title": "Python教程", "app_id": "browser"},
        {"url": "https://www.youtube.com/watch?v=123", "title": "YouTube视频", "app_id": "browser"},
        {"url": "https://github.com/user/repo", "title": "GitHub仓库", "app_id": "browser"},
        {"url": "https://stackoverflow.com/questions/123", "title": "Stack Overflow问题", "app_id": "browser"}
    ]
    
    try:
        for i in range(10):  # 模拟10次检查
            print(f"\n--- 检查 {i+1} ---")
            
            # 模拟任务变化
            current_task = mock_tasks[i % len(mock_tasks)]
            print(f"当前任务: {current_task['name']}")
            
            # 模拟网站变化
            current_website = mock_websites[i % len(mock_websites)]
            print(f"当前网站: {current_website['title']}")
            
            # 模拟分析结果
            if "python" in current_website['url'].lower() and "python" in current_task['name'].lower():
                print("分析结果: ✅ 相关 - 网站与任务匹配")
            elif "youtube" in current_website['url'].lower():
                print("分析结果: ❌ 无关 - 娱乐网站，可能分散注意力")
            else:
                print("分析结果: ⚠️  部分相关 - 需要进一步判断")
            
            time.sleep(1)  # 模拟1秒间隔
            
    except KeyboardInterrupt:
        print("\n\n监控已停止")


def example_configuration():
    """配置示例"""
    print("\n" + "=" * 70)
    print("配置示例")
    print("=" * 70)
    
    print("1. 环境变量配置:")
    print("   export GROQ_API_KEY='your_groq_api_key_here'")
    print("   export FLOWSTATE_PATH='/path/to/flowstate'  # 可选")
    
    print("\n2. FlowState 配置:")
    print("   cd /workspace/flowstate")
    print("   npm run build")
    print("   flow config:api-key groq your_groq_api_key")
    
    print("\n3. 创建任务:")
    print("   flow task:create '学习Python编程'")
    print("   flow task:list")
    
    print("\n4. 启动监控:")
    print("   cd /workspace/API/websiteChecker")
    print("   python3 flowstate_integration.py")


def main():
    """主函数"""
    print("FlowState 集成使用示例")
    print("=" * 70)
    
    # 运行示例
    example_basic_usage()
    example_monitoring_loop()
    example_configuration()
    
    print("\n" + "=" * 70)
    print("示例完成")
    print("=" * 70)
    print("要开始实际使用，请按照配置示例设置环境变量和FlowState。")
    print("然后运行: python3 flowstate_integration.py")


if __name__ == "__main__":
    main()