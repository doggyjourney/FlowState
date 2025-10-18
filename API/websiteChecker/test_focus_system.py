#!/usr/bin/env python3
"""
专注度系统测试脚本
测试专注度计算和监控功能
"""

import time
import random
from focus_score_calculator import FocusScoreCalculator
from enhanced_focus_monitor import EnhancedFocusMonitor


def test_focus_calculator():
    """测试专注度计算器"""
    print("=" * 70)
    print("测试专注度计算器")
    print("=" * 70)
    
    calculator = FocusScoreCalculator("test_focus_sessions.json")
    
    # 测试1：基础功能
    print("\n1. 测试基础功能...")
    session_id = calculator.start_session("test_task_001", "测试专注度计算")
    
    # 模拟一些网站访问
    test_websites = [
        ("https://docs.python.org", True, "high", "Python官方文档"),
        ("https://stackoverflow.com", True, "high", "编程问答网站"),
        ("https://github.com", True, "medium", "代码仓库"),
        ("https://www.youtube.com", False, "high", "视频网站，容易分心"),
        ("https://www.reddit.com", False, "high", "社交网站"),
        ("https://realpython.com", True, "high", "Python学习网站"),
        ("https://www.facebook.com", False, "high", "社交媒体"),
        ("https://pypi.org", True, "medium", "Python包索引"),
    ]
    
    for url, is_relevant, confidence, reason in test_websites:
        calculator.record_website_check(url, is_relevant, confidence, reason)
        time.sleep(0.1)  # 模拟时间间隔
    
    # 模拟专注时长
    print("   模拟专注时长...")
    time.sleep(2)
    
    # 结束会话
    ended_session = calculator.end_session()
    
    if ended_session:
        print(f"   ✅ 会话结束，专注度分数: {ended_session.focus_score:.1f}")
    else:
        print("   ❌ 会话结束失败")
    
    # 测试2：统计功能
    print("\n2. 测试统计功能...")
    calculator.print_focus_metrics(1)  # 查看最近1天的统计
    
    # 测试3：历史记录
    print("\n3. 测试历史记录...")
    history = calculator.get_session_history(5)
    print(f"   历史记录数量: {len(history)}")
    
    print("\n✅ 专注度计算器测试完成")


def test_enhanced_monitor():
    """测试增强版监控器"""
    print("\n" + "=" * 70)
    print("测试增强版监控器")
    print("=" * 70)
    
    monitor = EnhancedFocusMonitor()
    
    # 测试1：手动任务监控
    print("\n1. 测试手动任务监控...")
    success = monitor.start_task_monitoring("test_task_002", "测试增强监控")
    
    if success:
        print("   ✅ 监控启动成功")
        
        # 模拟几次网站检查
        for i in range(3):
            result = monitor.check_current_website()
            if result["success"]:
                print(f"   检查 {i+1}: {result['website_url']}")
                print(f"   相关: {'是' if result['is_relevant'] else '否'}")
                print(f"   专注度: {result['current_focus_score']:.1f}")
            time.sleep(0.5)
        
        # 结束监控
        result = monitor.end_task_monitoring()
        if result:
            print(f"   ✅ 监控结束，专注度分数: {result['focus_score']:.1f}")
        else:
            print("   ❌ 监控结束失败")
    else:
        print("   ❌ 监控启动失败")
    
    # 测试2：状态查询
    print("\n2. 测试状态查询...")
    status = monitor.get_current_status()
    print(f"   监控状态: {'活跃' if status['monitoring_active'] else '未活跃'}")
    
    # 测试3：历史记录
    print("\n3. 测试历史记录...")
    history = monitor.get_focus_history(3)
    print(f"   历史记录数量: {len(history)}")
    
    print("\n✅ 增强版监控器测试完成")


def test_scoring_algorithm():
    """测试评分算法"""
    print("\n" + "=" * 70)
    print("测试评分算法")
    print("=" * 70)
    
    calculator = FocusScoreCalculator("test_scoring.json")
    
    # 测试不同场景的评分
    test_scenarios = [
        {
            "name": "完美专注",
            "duration": 1800,  # 30分钟
            "relevant": 10,
            "irrelevant": 0
        },
        {
            "name": "良好专注",
            "duration": 1200,  # 20分钟
            "relevant": 8,
            "irrelevant": 2
        },
        {
            "name": "一般专注",
            "duration": 900,   # 15分钟
            "relevant": 5,
            "irrelevant": 5
        },
        {
            "name": "分心严重",
            "duration": 600,   # 10分钟
            "relevant": 2,
            "irrelevant": 8
        },
        {
            "name": "极短时间",
            "duration": 60,    # 1分钟
            "relevant": 1,
            "irrelevant": 0
        }
    ]
    
    for scenario in test_scenarios:
        # 创建测试会话
        session_id = calculator.start_session(
            f"test_{scenario['name']}", 
            scenario['name']
        )
        
        # 模拟网站访问
        for i in range(scenario['relevant']):
            calculator.record_website_check(
                f"https://relevant-site-{i}.com", 
                True, "high", "相关网站"
            )
        
        for i in range(scenario['irrelevant']):
            calculator.record_website_check(
                f"https://distraction-{i}.com", 
                False, "high", "无关网站"
            )
        
        # 模拟时长
        time.sleep(0.1)
        
        # 结束会话
        ended_session = calculator.end_session()
        
        if ended_session:
            print(f"   {scenario['name']}: {ended_session.focus_score:.1f}/100")
        else:
            print(f"   {scenario['name']}: 测试失败")
    
    print("\n✅ 评分算法测试完成")


def main():
    """主测试函数"""
    print("🧪 专注度系统测试开始")
    print("=" * 70)
    
    try:
        # 测试专注度计算器
        test_focus_calculator()
        
        # 测试增强版监控器
        test_enhanced_monitor()
        
        # 测试评分算法
        test_scoring_algorithm()
        
        print("\n" + "=" * 70)
        print("🎉 所有测试完成！")
        print("=" * 70)
        
        # 清理测试文件
        import os
        test_files = [
            "test_focus_sessions.json",
            "test_scoring.json"
        ]
        
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  已清理测试文件: {file}")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()