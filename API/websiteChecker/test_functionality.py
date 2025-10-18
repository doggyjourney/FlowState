#!/usr/bin/env python3
"""
测试任务记录和网站检测功能
演示如何使用任务专注度监控工具
"""

import os
import sys
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from task_focus_monitor import TaskFocusMonitor
from simple_focus_monitor import SimpleFocusMonitor


def test_basic_functionality():
    """测试基本功能 - 任务记录和网站检测"""
    print("=" * 70)
    print("测试1: 基本功能 - 任务记录和网站检测")
    print("=" * 70)
    
    # 检查是否有API Key
    if not os.environ.get("GROQ_API_KEY"):
        print("❌ 错误: 需要设置 GROQ_API_KEY 环境变量")
        print("请访问 https://console.groq.com/keys 获取免费API Key")
        print("然后运行: export GROQ_API_KEY='your-api-key-here'")
        return False
    
    try:
        # 创建监控器
        monitor = TaskFocusMonitor()
        print("✅ 成功创建任务专注度监控器")
        
        # 设置任务
        task = "学习Python编程"
        monitor.set_task(task)
        print(f"✅ 成功设置任务: {task}")
        
        # 测试网站检测
        test_websites = [
            {
                "url": "https://docs.python.org",
                "description": "Python官方文档",
                "expected": "相关"
            },
            {
                "url": "https://www.youtube.com",
                "description": "YouTube视频平台",
                "expected": "无关"
            },
            {
                "url": "https://stackoverflow.com",
                "description": "编程问答网站",
                "expected": "相关"
            },
            {
                "url": "https://www.instagram.com",
                "description": "社交媒体",
                "expected": "无关"
            }
        ]
        
        print(f"\n开始测试 {len(test_websites)} 个网站...")
        print("-" * 70)
        
        for i, site in enumerate(test_websites, 1):
            print(f"\n[{i}/{len(test_websites)}] 测试网站: {site['url']}")
            print(f"描述: {site['description']}")
            print(f"预期结果: {site['expected']}")
            
            # 检查网站
            result = monitor.check_website(site['url'], site['description'])
            
            # 显示结果
            status = "✅ 相关" if result['is_relevant'] else "❌ 无关"
            print(f"实际结果: {status}")
            print(f"置信度: {result['confidence']}")
            print(f"理由: {result['reason']}")
            
            # 判断是否符合预期
            actual = "相关" if result['is_relevant'] else "无关"
            if actual == site['expected']:
                print("✅ 结果符合预期")
            else:
                print("⚠️  结果与预期不符")
            
            print("-" * 70)
        
        # 显示统计信息
        print("\n")
        monitor.print_statistics()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_simple_monitor():
    """测试简化版监控器"""
    print("\n" + "=" * 70)
    print("测试2: 简化版监控器")
    print("=" * 70)
    
    try:
        monitor = SimpleFocusMonitor()
        monitor.set_task("写数学作业")
        
        # 测试几个网站
        test_urls = [
            "https://www.khanacademy.org",
            "https://www.netflix.com",
            "https://www.wolframalpha.com"
        ]
        
        for url in test_urls:
            print(f"\n检查网站: {url}")
            is_relevant, reason = monitor.check(url)
            status = "✅ 相关" if is_relevant else "❌ 无关"
            print(f"结果: {status}")
            print(f"理由: {reason}")
        
        return True
        
    except Exception as e:
        print(f"❌ 简化版监控器测试失败: {e}")
        return False


def test_demo_scenarios():
    """测试演示场景"""
    print("\n" + "=" * 70)
    print("测试3: 演示场景")
    print("=" * 70)
    
    scenarios = [
        {
            "task": "写技术博客",
            "websites": [
                ("https://github.com", "GitHub代码托管"),
                ("https://www.reddit.com", "Reddit论坛"),
                ("https://stackoverflow.com", "Stack Overflow"),
                ("https://www.tiktok.com", "TikTok短视频")
            ]
        },
        {
            "task": "准备考试复习",
            "websites": [
                ("https://www.coursera.org", "Coursera在线课程"),
                ("https://www.youtube.com", "YouTube视频"),
                ("https://www.notion.so", "Notion笔记工具"),
                ("https://www.facebook.com", "Facebook社交")
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario['task']}")
        print("-" * 50)
        
        try:
            monitor = TaskFocusMonitor()
            monitor.set_task(scenario['task'])
            
            for url, desc in scenario['websites']:
                result = monitor.check_website(url, desc)
                status = "✅" if result['is_relevant'] else "❌"
                print(f"{status} {url} - {desc}")
            
            print()
            monitor.print_statistics()
            
        except Exception as e:
            print(f"❌ 场景 {i} 测试失败: {e}")


def main():
    """主测试函数"""
    print("🧪 任务记录和网站检测功能测试")
    print("=" * 70)
    print("这个测试将验证以下功能:")
    print("1. 任务记录 - 输入并保存当前任务")
    print("2. 网站检测 - 判断网站是否与任务相关")
    print("3. 专注提醒 - 对无关网站给出建议")
    print("=" * 70)
    
    # 运行测试
    tests = [
        ("基本功能测试", test_basic_functionality),
        ("简化版监控器测试", test_simple_monitor),
        ("演示场景测试", test_demo_scenarios)
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
        print("\n🎉 所有测试通过！功能正常工作。")
        print("\n📝 使用建议:")
        print("1. 运行 'python task_focus_monitor.py' 开始交互式使用")
        print("2. 运行 'python web_monitor.py' 启动Web界面")
        print("3. 运行 'python demo.py' 查看完整演示")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败")
        print("请检查 GROQ_API_KEY 环境变量是否正确设置")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)