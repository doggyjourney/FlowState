#!/usr/bin/env python3
"""
测试 FlowState 集成功能
"""

import sys
import json
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from flowstate_bridge import FlowStateBridge
from task_focus_monitor import TaskFocusMonitor


def test_bridge():
    """测试桥接器功能"""
    print("=" * 70)
    print("测试 FlowState 桥接器")
    print("=" * 70)
    
    bridge = FlowStateBridge()
    
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


def test_monitor():
    """测试监控器功能"""
    print("\n" + "=" * 70)
    print("测试 TaskFocusMonitor")
    print("=" * 70)
    
    try:
        monitor = TaskFocusMonitor()
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


def test_integration():
    """测试集成功能"""
    print("\n" + "=" * 70)
    print("测试集成功能")
    print("=" * 70)
    
    try:
        bridge = FlowStateBridge()
        monitor = TaskFocusMonitor()
        
        # 获取测试数据
        task = bridge.get_current_task()
        website = bridge.get_current_website()
        
        if not task or not website:
            print("   ❌ 无法获取测试数据")
            return False
        
        # 测试集成分析
        result = monitor.check_from_flowstate(task, website)
        print("   ✅ 成功执行集成分析")
        print(f"   📊 分析结果: {'相关' if result['is_relevant'] else '无关'}")
        print(f"   🎯 置信度: {result['confidence']}")
        print(f"   💡 建议: {result['action']}")
        print(f"   📝 理由: {result['reason']}")
        
        return True
    except Exception as e:
        print(f"   ❌ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("FlowState 集成功能测试")
    print("=" * 70)
    
    # 运行测试
    tests = [
        ("桥接器功能", test_bridge),
        ("监控器功能", test_monitor),
        ("集成功能", test_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
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
        print("\n🎉 所有测试通过！集成功能正常工作。")
        return 0
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())