#!/usr/bin/env python3
"""
模拟测试 - 不需要真实API Key的功能演示
展示任务记录和网站检测的工作流程
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))


class MockTaskFocusMonitor:
    """模拟任务专注度监控器 - 用于演示功能"""
    
    def __init__(self):
        self.current_task = None
        self.check_history = []
    
    def set_task(self, task_description):
        """设置当前任务"""
        self.current_task = task_description
        self.check_history = []
        print(f"\n✓ 已设置当前任务: {task_description}")
        print(f"现在会监控打开的网站是否与此任务相关\n")
    
    def check_website(self, website_url, website_description=None):
        """模拟检查网站是否属于当前任务主题"""
        if not self.current_task:
            return {
                "is_relevant": False,
                "action": "error",
                "reason": "错误：请先使用 set_task() 设置当前任务",
                "confidence": "none"
            }
        
        # 模拟AI判断逻辑
        result = self._mock_ai_judgment(website_url, website_description)
        
        # 记录检查历史
        self.check_history.append({
            "timestamp": datetime.now().isoformat(),
            "website_url": website_url,
            "task": self.current_task,
            "result": result
        })
        
        return result
    
    def _mock_ai_judgment(self, website_url, website_description):
        """模拟AI判断逻辑"""
        # 简单的规则判断（实际使用中会调用Groq API）
        url_lower = website_url.lower()
        task_lower = self.current_task.lower()
        
        # 定义相关关键词
        educational_sites = ['docs.', 'tutorial', 'course', 'learn', 'study', 'academy', 'khan', 'coursera', 'edx']
        programming_sites = ['github', 'stackoverflow', 'python', 'javascript', 'code', 'dev', 'programming']
        productivity_sites = ['notion', 'google', 'office', 'canva', 'figma', 'slack', 'trello']
        entertainment_sites = ['youtube', 'netflix', 'instagram', 'facebook', 'twitter', 'tiktok', 'reddit']
        
        # 判断网站类型
        is_educational = any(keyword in url_lower for keyword in educational_sites)
        is_programming = any(keyword in url_lower for keyword in programming_sites)
        is_productivity = any(keyword in url_lower for keyword in productivity_sites)
        is_entertainment = any(keyword in url_lower for keyword in entertainment_sites)
        
        # 根据任务类型判断相关性
        if '学习' in task_lower or '编程' in task_lower or 'python' in task_lower:
            if is_educational or is_programming:
                return {
                    "is_relevant": True,
                    "action": "allow",
                    "reason": "此网站有助于学习编程，与任务相关",
                    "confidence": "high"
                }
            elif is_entertainment:
                return {
                    "is_relevant": False,
                    "action": "block",
                    "reason": "娱乐网站可能分散学习注意力",
                    "confidence": "high"
                }
        
        elif '作业' in task_lower or '数学' in task_lower:
            if is_educational or 'wolfram' in url_lower or 'khan' in url_lower:
                return {
                    "is_relevant": True,
                    "action": "allow",
                    "reason": "教育网站有助于完成作业",
                    "confidence": "high"
                }
            elif is_entertainment:
                return {
                    "is_relevant": False,
                    "action": "block",
                    "reason": "娱乐网站会分散做作业的注意力",
                    "confidence": "high"
                }
        
        elif '工作' in task_lower or '报告' in task_lower or '博客' in task_lower:
            if is_productivity or is_programming:
                return {
                    "is_relevant": True,
                    "action": "allow",
                    "reason": "生产力工具有助于完成工作任务",
                    "confidence": "high"
                }
            elif is_entertainment:
                return {
                    "is_relevant": False,
                    "action": "block",
                    "reason": "娱乐网站会影响工作效率",
                    "confidence": "high"
                }
        
        # 默认判断
        if is_entertainment:
            return {
                "is_relevant": False,
                "action": "block",
                "reason": "娱乐网站可能分散注意力",
                "confidence": "medium"
            }
        else:
            return {
                "is_relevant": True,
                "action": "allow",
                "reason": "网站内容可能与任务相关",
                "confidence": "medium"
            }
    
    def print_check_result(self, website_url, result):
        """打印检查结果"""
        print("=" * 70)
        print(f"网站检查结果: {website_url}")
        print("=" * 70)
        print(f"当前任务: {self.current_task}")
        print(f"判断结果: {'✓ 与任务相关' if result['is_relevant'] else '✗ 与任务无关'}")
        print(f"建议操作: {'允许打开' if result['action'] == 'allow' else '建议关闭'}")
        print(f"置信度: {result['confidence']}")
        print(f"\n理由: {result['reason']}")
        print("=" * 70)
        
        if result['action'] == 'allow':
            print("✓ 可以打开此网站，继续完成任务")
        else:
            print("✗ 此网站与任务无关，建议关闭以保持专注")
        print()
    
    def get_history(self):
        """获取检查历史记录"""
        return self.check_history
    
    def print_statistics(self):
        """打印统计信息"""
        if not self.check_history:
            print("暂无检查记录")
            return
        
        total = len(self.check_history)
        relevant = sum(1 for h in self.check_history if h['result']['is_relevant'])
        irrelevant = total - relevant
        
        print("\n" + "=" * 70)
        print("任务专注度统计")
        print("=" * 70)
        print(f"当前任务: {self.current_task}")
        print(f"检查网站总数: {total}")
        print(f"相关网站: {relevant} ({relevant/total*100:.1f}%)")
        print(f"无关网站: {irrelevant} ({irrelevant/total*100:.1f}%)")
        print("=" * 70 + "\n")


def test_task_recording():
    """测试任务记录功能"""
    print("=" * 70)
    print("测试1: 任务记录功能")
    print("=" * 70)
    
    monitor = MockTaskFocusMonitor()
    
    # 测试设置任务
    tasks = [
        "学习Python编程",
        "写数学作业",
        "准备技术博客",
        "复习考试内容"
    ]
    
    for task in tasks:
        print(f"\n设置任务: {task}")
        monitor.set_task(task)
        print(f"✅ 任务记录成功: {monitor.current_task}")
    
    return True


def test_website_detection():
    """测试网站检测功能"""
    print("\n" + "=" * 70)
    print("测试2: 网站检测功能")
    print("=" * 70)
    
    monitor = MockTaskFocusMonitor()
    monitor.set_task("学习Python编程")
    
    # 测试网站检测
    test_websites = [
        ("https://docs.python.org", "Python官方文档"),
        ("https://www.youtube.com", "YouTube视频平台"),
        ("https://stackoverflow.com", "Stack Overflow编程问答"),
        ("https://www.instagram.com", "Instagram社交媒体"),
        ("https://github.com", "GitHub代码托管"),
        ("https://www.netflix.com", "Netflix视频流媒体")
    ]
    
    print(f"开始检测 {len(test_websites)} 个网站...")
    print("-" * 70)
    
    for url, description in test_websites:
        print(f"\n检测网站: {url}")
        print(f"描述: {description}")
        
        result = monitor.check_website(url, description)
        
        status = "✅ 相关" if result['is_relevant'] else "❌ 无关"
        print(f"检测结果: {status}")
        print(f"置信度: {result['confidence']}")
        print(f"理由: {result['reason']}")
        print("-" * 70)
    
    # 显示统计
    monitor.print_statistics()
    
    return True


def test_focus_scenarios():
    """测试专注场景"""
    print("\n" + "=" * 70)
    print("测试3: 专注场景演示")
    print("=" * 70)
    
    scenarios = [
        {
            "task": "写数学作业",
            "websites": [
                ("https://www.khanacademy.org", "可汗学院数学课程"),
                ("https://www.wolframalpha.com", "Wolfram Alpha计算工具"),
                ("https://www.youtube.com", "YouTube视频"),
                ("https://www.instagram.com", "Instagram社交")
            ]
        },
        {
            "task": "准备技术博客",
            "websites": [
                ("https://github.com", "GitHub代码仓库"),
                ("https://stackoverflow.com", "Stack Overflow问答"),
                ("https://www.reddit.com", "Reddit论坛"),
                ("https://www.notion.so", "Notion笔记工具")
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario['task']}")
        print("-" * 50)
        
        monitor = MockTaskFocusMonitor()
        monitor.set_task(scenario['task'])
        
        for url, desc in scenario['websites']:
            result = monitor.check_website(url, desc)
            status = "✅" if result['is_relevant'] else "❌"
            print(f"{status} {url} - {desc}")
        
        print()
        monitor.print_statistics()
    
    return True


def test_workflow_demo():
    """测试完整工作流程"""
    print("\n" + "=" * 70)
    print("测试4: 完整工作流程演示")
    print("=" * 70)
    
    print("🎯 模拟用户使用流程:")
    print("1. 用户输入任务")
    print("2. 用户打开网站")
    print("3. 系统检测网站相关性")
    print("4. 给出专注建议")
    print("5. 记录统计信息")
    print()
    
    monitor = MockTaskFocusMonitor()
    
    # 步骤1: 设置任务
    print("步骤1: 用户设置任务")
    task = "学习机器学习"
    monitor.set_task(task)
    
    # 步骤2-4: 模拟用户浏览网站
    print("步骤2-4: 模拟用户浏览网站并检测")
    browsing_session = [
        ("https://www.coursera.org", "Coursera机器学习课程"),
        ("https://arxiv.org", "ArXiv学术论文"),
        ("https://www.youtube.com", "YouTube视频"),
        ("https://www.tiktok.com", "TikTok短视频"),
        ("https://scikit-learn.org", "Scikit-learn机器学习库"),
        ("https://www.facebook.com", "Facebook社交")
    ]
    
    print(f"\n模拟用户在30分钟内访问了 {len(browsing_session)} 个网站:")
    print("-" * 70)
    
    for i, (url, desc) in enumerate(browsing_session, 1):
        print(f"\n[{i}] 用户访问: {url}")
        result = monitor.check_website(url, desc)
        
        if result['is_relevant']:
            print("✅ 系统判断: 与任务相关 - 允许继续")
        else:
            print("❌ 系统判断: 与任务无关 - 建议关闭")
            print("💡 专注提醒: 此网站可能分散学习注意力")
    
    # 步骤5: 显示统计
    print("\n步骤5: 专注度统计报告")
    monitor.print_statistics()
    
    # 计算专注度得分
    history = monitor.get_history()
    relevant_count = sum(1 for h in history if h['result']['is_relevant'])
    focus_score = (relevant_count / len(history)) * 100
    
    print(f"🎯 专注度得分: {focus_score:.1f}%")
    
    if focus_score >= 80:
        print("评价: 优秀！保持专注 🎯")
    elif focus_score >= 60:
        print("评价: 良好，还有提升空间 👍")
    else:
        print("评价: 需要改善，减少无关网站访问 ⚠️")
    
    return True


def main():
    """主测试函数"""
    print("🧪 任务记录和网站检测功能 - 模拟测试")
    print("=" * 70)
    print("这个测试演示了以下功能:")
    print("1. 📝 任务记录 - 输入并保存当前任务")
    print("2. 🔍 网站检测 - 智能判断网站是否与任务相关")
    print("3. 🎯 专注提醒 - 对无关网站给出关闭建议")
    print("4. 📊 统计分析 - 提供专注度统计和评分")
    print("=" * 70)
    
    # 运行测试
    tests = [
        ("任务记录功能", test_task_recording),
        ("网站检测功能", test_website_detection),
        ("专注场景演示", test_focus_scenarios),
        ("完整工作流程", test_workflow_demo)
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
        print("\n🎉 所有功能演示成功！")
        print("\n📝 实际使用说明:")
        print("1. 设置 GROQ_API_KEY 环境变量")
        print("2. 运行 'python3 task_focus_monitor.py' 开始交互式使用")
        print("3. 运行 'python3 web_monitor.py' 启动Web界面")
        print("4. 运行 'python3 demo.py' 查看完整演示")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)