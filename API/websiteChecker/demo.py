"""
演示脚本 - 展示任务专注度监控工具的使用
"""

from task_focus_monitor import TaskFocusMonitor


def demo_basic_usage():
    """演示基本使用"""
    print("\n" + "="*70)
    print("演示1: 基本使用")
    print("="*70 + "\n")
    
    # 创建监控器
    monitor = TaskFocusMonitor()
    
    # 设置任务
    monitor.set_task("写数学作业")
    
    # 检查几个网站
    test_websites = [
        ("https://www.khanacademy.org", "可汗学院 - 数学学习平台"),
        ("https://www.youtube.com", "YouTube - 视频娱乐平台"),
        ("https://www.wolframalpha.com", "Wolfram Alpha - 数学计算工具"),
        ("https://www.instagram.com", "Instagram - 社交媒体"),
    ]
    
    for url, description in test_websites:
        print(f"\n检查网站: {url}")
        print(f"描述: {description}")
        result = monitor.check_website(url, description)
        
        if result['is_relevant']:
            print(f"✓ 与任务相关 - 可以打开")
        else:
            print(f"✗ 与任务无关 - 建议关闭")
        print(f"理由: {result['reason']}")
        print("-" * 70)
    
    # 显示统计
    print("\n")
    monitor.print_statistics()


def demo_multiple_tasks():
    """演示多任务场景"""
    print("\n" + "="*70)
    print("演示2: 不同任务的判断差异")
    print("="*70 + "\n")
    
    test_url = "https://github.com"
    
    tasks = [
        "学习Python编程",
        "写数学作业",
        "看电影放松",
    ]
    
    for task in tasks:
        monitor = TaskFocusMonitor()
        monitor.set_task(task)
        
        result = monitor.check_website(test_url)
        
        print(f"任务: {task}")
        print(f"网站: {test_url}")
        print(f"判断: {'✓ 相关' if result['is_relevant'] else '✗ 无关'}")
        print(f"理由: {result['reason']}")
        print("-" * 70)


def demo_focus_session():
    """演示专注时段"""
    print("\n" + "="*70)
    print("演示3: 专注时段模拟")
    print("="*70 + "\n")
    
    monitor = TaskFocusMonitor()
    monitor.set_task("准备项目报告")
    
    # 模拟用户在工作时段打开的网站
    browsing_history = [
        "https://docs.google.com",
        "https://www.canva.com",
        "https://twitter.com",
        "https://www.notion.so",
        "https://www.reddit.com",
        "https://www.figma.com",
    ]
    
    print("模拟用户在30分钟内打开的网站:\n")
    
    for i, url in enumerate(browsing_history, 1):
        result = monitor.check_website(url)
        status = "✓" if result['is_relevant'] else "✗"
        print(f"{i}. {status} {url}")
    
    print("\n")
    monitor.print_statistics()
    
    # 计算专注度得分
    history = monitor.get_history()
    relevant_count = sum(1 for h in history if h['result']['is_relevant'])
    focus_score = (relevant_count / len(history)) * 100
    
    print(f"\n专注度得分: {focus_score:.1f}%")
    
    if focus_score >= 80:
        print("评价: 优秀！保持专注 🎯")
    elif focus_score >= 60:
        print("评价: 良好，还有提升空间 👍")
    else:
        print("评价: 需要改善，减少无关网站访问 ⚠️")


def demo_save_and_load():
    """演示保存和加载历史"""
    print("\n" + "="*70)
    print("演示4: 保存历史记录")
    print("="*70 + "\n")
    
    monitor = TaskFocusMonitor()
    monitor.set_task("学习机器学习")
    
    # 检查一些网站
    websites = [
        "https://www.coursera.org",
        "https://arxiv.org",
        "https://www.tiktok.com",
    ]
    
    for url in websites:
        monitor.check_website(url)
    
    # 保存历史
    filename = "demo_history.json"
    monitor.save_history(filename)
    
    print(f"\n历史记录已保存到: {filename}")
    print("可以使用 JSON 查看器打开此文件查看详细记录")


def main():
    """运行所有演示"""
    print("\n" + "="*70)
    print("任务专注度监控工具 - 功能演示")
    print("="*70)
    
    try:
        # 运行各个演示
        demo_basic_usage()
        input("\n按 Enter 继续下一个演示...")
        
        demo_multiple_tasks()
        input("\n按 Enter 继续下一个演示...")
        
        demo_focus_session()
        input("\n按 Enter 继续下一个演示...")
        
        demo_save_and_load()
        
        print("\n" + "="*70)
        print("演示完成！")
        print("="*70)
        print("\n提示:")
        print("- 运行 'python task_focus_monitor.py' 开始交互式使用")
        print("- 运行 'python web_monitor.py' 启动Web界面")
        print("- 查看 README.md 了解更多功能")
        print()
        
    except KeyboardInterrupt:
        print("\n\n演示已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        print("请确保已设置 GROQ_API_KEY 环境变量")


if __name__ == "__main__":
    main()

