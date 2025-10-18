#!/usr/bin/env python3
"""
专注度系统演示脚本
展示专注度计算和监控功能的使用方法
"""

import time
import random
from focus_score_calculator import FocusScoreCalculator
from enhanced_focus_monitor import EnhancedFocusMonitor


def demo_basic_usage():
    """演示基础使用方法"""
    print("=" * 70)
    print("🎯 专注度系统基础使用演示")
    print("=" * 70)
    
    # 创建专注度计算器
    calculator = FocusScoreCalculator("demo_sessions.json")
    
    print("\n1. 开始专注会话...")
    session_id = calculator.start_session("demo_task_001", "学习Python编程")
    
    print("\n2. 模拟网站访问...")
    # 模拟一些网站访问
    websites = [
        ("https://docs.python.org", True, "high", "Python官方文档，学习相关"),
        ("https://stackoverflow.com", True, "high", "编程问答网站，有助于学习"),
        ("https://github.com", True, "medium", "代码仓库，学习相关"),
        ("https://realpython.com", True, "high", "Python学习网站"),
        ("https://www.youtube.com", False, "high", "视频网站，容易分心"),
        ("https://www.reddit.com", False, "high", "社交网站，与学习无关"),
        ("https://pypi.org", True, "medium", "Python包索引"),
        ("https://www.facebook.com", False, "high", "社交媒体，容易分心"),
    ]
    
    for i, (url, is_relevant, confidence, reason) in enumerate(websites, 1):
        print(f"   访问网站 {i}: {url}")
        calculator.record_website_check(url, is_relevant, confidence, reason)
        time.sleep(0.5)  # 模拟时间间隔
    
    print("\n3. 模拟专注时长...")
    print("   专注学习中...")
    time.sleep(3)  # 模拟3秒专注时间
    
    print("\n4. 结束专注会话...")
    ended_session = calculator.end_session()
    
    if ended_session:
        print(f"\n✅ 专注会话完成！")
        print(f"   专注度分数: {ended_session.focus_score:.1f}/100")
        
        # 显示评级
        if ended_session.focus_score >= 90:
            grade = "🌟 优秀"
        elif ended_session.focus_score >= 80:
            grade = "👍 良好"
        elif ended_session.focus_score >= 70:
            grade = "👌 一般"
        elif ended_session.focus_score >= 60:
            grade = "⚠️ 需要改进"
        else:
            grade = "❌ 需要大幅改进"
        
        print(f"   评级: {grade}")
    
    print("\n5. 查看专注度统计...")
    calculator.print_focus_metrics(1)
    
    print("\n6. 查看历史记录...")
    history = calculator.get_session_history(3)
    if history:
        print("   最近3次会话:")
        for i, session in enumerate(history, 1):
            print(f"   {i}. {session['start_time']} - {session['task_name']}")
            print(f"      时长: {session['duration_minutes']:.1f}分钟 | 分数: {session['focus_score']:.1f}/100")


def demo_enhanced_monitor():
    """演示增强版监控器"""
    print("\n" + "=" * 70)
    print("🚀 增强版监控器演示")
    print("=" * 70)
    
    monitor = EnhancedFocusMonitor()
    
    print("\n1. 启动任务监控...")
    success = monitor.start_task_monitoring("demo_task_002", "写技术文档")
    
    if success:
        print("   ✅ 监控启动成功")
        
        print("\n2. 模拟网站检查...")
        # 模拟几次网站检查
        for i in range(5):
            result = monitor.check_current_website()
            if result["success"]:
                print(f"   检查 {i+1}: {result['website_url']}")
                print(f"   标题: {result['website_title']}")
                print(f"   相关: {'是' if result['is_relevant'] else '否'}")
                print(f"   理由: {result['reason']}")
                print(f"   当前专注度: {result['current_focus_score']:.1f}/100")
                print()
            time.sleep(1)
        
        print("\n3. 查看当前状态...")
        status = monitor.get_current_status()
        if status["monitoring_active"]:
            print(f"   任务: {status['task_name']}")
            print(f"   时长: {status['duration_minutes']:.1f} 分钟")
            print(f"   专注度: {status['current_focus_score']:.1f}/100")
            print(f"   相关网站: {status['relevant_websites']} 次")
            print(f"   无关网站: {status['irrelevant_websites']} 次")
        
        print("\n4. 结束监控...")
        result = monitor.end_task_monitoring()
        if result:
            print(f"   ✅ 监控结束，专注度分数: {result['focus_score']:.1f}/100")
            print(f"   评级: {result['grade']}")
    
    else:
        print("   ❌ 监控启动失败")


def demo_scoring_scenarios():
    """演示不同专注度场景"""
    print("\n" + "=" * 70)
    print("📊 专注度评分场景演示")
    print("=" * 70)
    
    calculator = FocusScoreCalculator("demo_scenarios.json")
    
    scenarios = [
        {
            "name": "完美专注 - 长时间专注，只访问相关网站",
            "duration": 30,  # 30分钟
            "relevant": 15,
            "irrelevant": 0
        },
        {
            "name": "良好专注 - 适度专注，偶尔分心",
            "duration": 20,  # 20分钟
            "relevant": 10,
            "irrelevant": 2
        },
        {
            "name": "一般专注 - 专注时间短，分心较多",
            "duration": 10,  # 10分钟
            "relevant": 5,
            "irrelevant": 5
        },
        {
            "name": "分心严重 - 专注时间短，大量分心",
            "duration": 5,   # 5分钟
            "relevant": 2,
            "irrelevant": 8
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   时长: {scenario['duration']}分钟, 相关: {scenario['relevant']}次, 无关: {scenario['irrelevant']}次")
        
        # 创建测试会话
        session_id = calculator.start_session(f"scenario_{i}", scenario['name'])
        
        # 模拟网站访问
        for j in range(scenario['relevant']):
            calculator.record_website_check(
                f"https://relevant-{j}.com", 
                True, "high", "相关网站"
            )
        
        for j in range(scenario['irrelevant']):
            calculator.record_website_check(
                f"https://distraction-{j}.com", 
                False, "high", "无关网站"
            )
        
        # 模拟时长
        time.sleep(0.1)
        
        # 结束会话
        ended_session = calculator.end_session()
        
        if ended_session:
            print(f"   专注度分数: {ended_session.focus_score:.1f}/100")
            
            # 评级
            if ended_session.focus_score >= 90:
                grade = "🌟 优秀"
            elif ended_session.focus_score >= 80:
                grade = "👍 良好"
            elif ended_session.focus_score >= 70:
                grade = "👌 一般"
            elif ended_session.focus_score >= 60:
                grade = "⚠️ 需要改进"
            else:
                grade = "❌ 需要大幅改进"
            
            print(f"   评级: {grade}")


def main():
    """主演示函数"""
    print("🎯 专注度系统完整演示")
    print("=" * 70)
    print("本演示将展示专注度计算和监控系统的各种功能")
    print()
    
    try:
        # 演示基础使用
        demo_basic_usage()
        
        # 演示增强版监控器
        demo_enhanced_monitor()
        
        # 演示评分场景
        demo_scoring_scenarios()
        
        print("\n" + "=" * 70)
        print("🎉 演示完成！")
        print("=" * 70)
        print("专注度系统功能总结:")
        print("✅ 专注时长记录")
        print("✅ 网站访问分析")
        print("✅ 专注度分数计算")
        print("✅ 任务管理集成")
        print("✅ 历史记录和统计")
        print("✅ 实时监控功能")
        print()
        print("现在您可以:")
        print("1. 使用 focus_cli.py 进行命令行操作")
        print("2. 集成到您的应用程序中")
        print("3. 自定义评分算法")
        print("4. 扩展更多功能")
        
        # 清理演示文件
        import os
        demo_files = ["demo_sessions.json", "demo_scenarios.json"]
        for file in demo_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  已清理演示文件: {file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()