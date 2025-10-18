"""
批量检查示例 - 一次性检查多个网站
"""

from task_focus_monitor import TaskFocusMonitor


def batch_check_websites(task, websites):
    """
    批量检查多个网站是否与任务相关
    
    参数:
        task: 任务描述
        websites: 网站URL列表
    """
    monitor = TaskFocusMonitor()
    monitor.set_task(task)
    
    results = []
    
    print(f"正在检查 {len(websites)} 个网站...\n")
    
    for i, website in enumerate(websites, 1):
        print(f"[{i}/{len(websites)}] 检查: {website}")
        result = monitor.check_website(website)
        results.append({
            "url": website,
            "relevant": result['is_relevant'],
            "reason": result['reason']
        })
        print(f"  结果: {'✓ 相关' if result['is_relevant'] else '✗ 无关'}\n")
    
    # 打印汇总
    print("\n" + "="*70)
    print("检查汇总")
    print("="*70)
    
    relevant_sites = [r for r in results if r['relevant']]
    irrelevant_sites = [r for r in results if not r['relevant']]
    
    print(f"\n✓ 相关网站 ({len(relevant_sites)}个):")
    for site in relevant_sites:
        print(f"  - {site['url']}")
    
    print(f"\n✗ 无关网站 ({len(irrelevant_sites)}个):")
    for site in irrelevant_sites:
        print(f"  - {site['url']}")
    
    print("\n" + "="*70)
    
    return results


# 使用示例
if __name__ == "__main__":
    # 示例1: 检查"写作业"相关网站
    print("示例1: 写作业任务")
    task1 = "写数学作业"
    websites1 = [
        "https://www.khanacademy.org",  # 可汗学院
        "https://www.youtube.com",       # YouTube
        "https://www.wolframalpha.com",  # Wolfram Alpha
        "https://www.instagram.com",     # Instagram
        "https://stackoverflow.com",     # Stack Overflow
    ]
    
    batch_check_websites(task1, websites1)
    
    print("\n\n" + "="*70 + "\n\n")
    
    # 示例2: 检查"学习Python"相关网站
    print("示例2: 学习Python任务")
    task2 = "学习Python编程"
    websites2 = [
        "https://docs.python.org",       # Python官方文档
        "https://www.reddit.com",        # Reddit
        "https://realpython.com",        # Real Python
        "https://www.netflix.com",       # Netflix
        "https://github.com",            # GitHub
    ]
    
    batch_check_websites(task2, websites2)

