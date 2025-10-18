"""
任务专注度监控工具 - 使用 Groq API
功能：先输入任务，然后判断每次打开的网站是否属于任务主题
"""

import os
import json
import time
from datetime import datetime
from groq import Groq
from focus_score_calculator import FocusScoreCalculator


class TaskFocusMonitor:
    """任务专注度监控器 - 帮助用户保持专注于当前任务"""
    
    def __init__(self, api_key=None):
        """
        初始化任务专注度监控器
        
        参数:
            api_key: Groq API密钥，如果不提供则从环境变量GROQ_API_KEY读取
        """
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        self.current_task = None
        self.check_history = []
        self.focus_calculator = FocusScoreCalculator()
        self.session_start_time = None
    
    def set_task(self, task_description):
        """
        设置当前任务
        
        参数:
            task_description: 任务描述，例如"写作业"、"学习Python编程"
        """
        self.current_task = task_description
        self.check_history = []
        self.session_start_time = time.time()
        
        # 开始专注会话
        task_id = f"task_{int(time.time())}"
        self.focus_calculator.start_session(task_id, task_description)
        
        print(f"\n✓ 已设置当前任务: {task_description}")
        print(f"现在会监控打开的网站是否与此任务相关")
        print(f"专注会话已开始，将记录您的专注时长和网站访问情况\n")
    
    def check_website(self, website_url, website_description=None):
        """
        检查网站是否属于当前任务主题
        
        参数:
            website_url: 要检查的网站URL
            website_description: 网站描述（可选），如果不提供则只使用URL
        
        返回:
            dict: 包含以下键的字典
                - is_relevant: bool, 是否与任务相关
                - action: str, 建议的操作（"allow" 或 "block"）
                - reason: str, 判断理由
                - confidence: str, 置信度（high/medium/low）
        """
        if not self.current_task:
            return {
                "is_relevant": False,
                "action": "error",
                "reason": "错误：请先使用 set_task() 设置当前任务",
                "confidence": "none"
            }
        
        # 构建提示词
        website_info = f"URL: {website_url}"
        if website_description:
            website_info += f"\n网站描述: {website_description}"
        
        prompt = f"""我正在执行的任务是：{self.current_task}

现在我想打开以下网站：
{website_info}

请判断这个网站是否与我的任务主题相关。

判断标准：
1. 如果网站内容直接有助于完成任务，判定为"相关"
2. 如果网站是娱乐、社交、购物等与任务无关的内容，判定为"不相关"
3. 如果网站是搜索引擎、工具类网站，需要根据任务判断

请按以下格式回答：
判断：相关 / 不相关
置信度：高 / 中 / 低
理由：[简短说明为什么相关或不相关]

只回答以上内容，不要添加其他说明。"""

        try:
            # 调用 Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的任务专注度助手，帮助用户判断网站是否与当前任务相关，从而保持专注。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,  # 低温度以获得更一致的判断
                max_tokens=512
            )
            
            # 获取响应内容
            response_content = chat_completion.choices[0].message.content
            
            # 解析响应
            result = self._parse_check_response(response_content, website_url)
            
            # 记录检查历史
            self.check_history.append({
                "timestamp": datetime.now().isoformat(),
                "website_url": website_url,
                "task": self.current_task,
                "result": result
            })
            
            # 记录到专注度计算器
            self.focus_calculator.record_website_check(
                website_url=website_url,
                is_relevant=result["is_relevant"],
                confidence=result["confidence"],
                reason=result["reason"]
            )
            
            return result
            
        except Exception as e:
            return {
                "is_relevant": False,
                "action": "error",
                "reason": f"API调用出错: {str(e)}",
                "confidence": "none"
            }
    
    def _parse_check_response(self, response_content, website_url):
        """
        解析API响应内容
        
        参数:
            response_content: API返回的文本内容
            website_url: 网站URL
        
        返回:
            dict: 解析后的结果
        """
        # 判断是否相关
        is_relevant = "相关" in response_content and "不相关" not in response_content.split("\n")[0]
        
        # 提取置信度
        confidence = "medium"
        if "高" in response_content:
            confidence = "high"
        elif "低" in response_content:
            confidence = "low"
        
        # 提取理由
        reason = response_content
        lines = response_content.split("\n")
        for line in lines:
            if "理由" in line:
                reason = line.replace("理由：", "").replace("理由:", "").strip()
                break
        
        result = {
            "is_relevant": is_relevant,
            "action": "allow" if is_relevant else "block",
            "reason": reason,
            "confidence": confidence,
            "raw_response": response_content
        }
        
        return result
    
    def print_check_result(self, website_url, result):
        """
        打印检查结果
        
        参数:
            website_url: 网站URL
            result: check_website方法返回的结果字典
        """
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
        """
        获取检查历史记录
        
        返回:
            list: 历史记录列表
        """
        return self.check_history
    
    def save_history(self, filename="task_focus_history.json"):
        """
        保存检查历史到文件
        
        参数:
            filename: 保存的文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "task": self.current_task,
                "history": self.check_history
            }, f, ensure_ascii=False, indent=2)
        print(f"✓ 历史记录已保存到 {filename}")
    
    def end_task(self):
        """
        结束当前任务并计算专注度
        
        返回:
            dict: 任务结束后的专注度统计
        """
        if not self.current_task:
            print("❌ 没有活跃的任务")
            return None
        
        # 结束专注会话
        ended_session = self.focus_calculator.end_session()
        
        if ended_session:
            # 打印任务总结
            print("\n" + "=" * 70)
            print("🎯 任务完成总结")
            print("=" * 70)
            print(f"任务: {self.current_task}")
            print(f"专注时长: {ended_session.total_duration / 60.0:.1f} 分钟")
            print(f"相关网站: {ended_session.relevant_websites} 次")
            print(f"无关网站: {ended_session.irrelevant_websites} 次")
            print(f"专注度分数: {ended_session.focus_score:.1f}/100")
            
            # 分数评级
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
            
            print(f"评级: {grade}")
            print("=" * 70 + "\n")
            
            # 清除当前任务
            self.current_task = None
            self.session_start_time = None
            
            return {
                "task_name": ended_session.task_name,
                "duration_minutes": ended_session.total_duration / 60.0,
                "focus_score": ended_session.focus_score,
                "relevant_websites": ended_session.relevant_websites,
                "irrelevant_websites": ended_session.irrelevant_websites,
                "grade": grade
            }
        
        return None
    
    def get_current_focus_info(self):
        """获取当前专注信息"""
        if not self.current_task:
            return None
        
        session_info = self.focus_calculator.get_current_session_info()
        if session_info:
            return {
                "task_name": self.current_task,
                "duration_minutes": session_info["duration_minutes"],
                "current_focus_score": session_info["current_focus_score"],
                "relevant_websites": session_info["relevant_websites"],
                "irrelevant_websites": session_info["irrelevant_websites"]
            }
        return None
    
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
        
        # 显示当前专注信息
        focus_info = self.get_current_focus_info()
        if focus_info:
            print(f"当前专注时长: {focus_info['duration_minutes']:.1f} 分钟")
            print(f"当前专注度分数: {focus_info['current_focus_score']:.1f}/100")
        
        print("=" * 70 + "\n")
    
    def print_focus_history(self, days=30):
        """打印专注度历史记录"""
        self.focus_calculator.print_focus_metrics(days)
    
    def get_focus_history(self, limit=10):
        """获取专注度历史记录"""
        return self.focus_calculator.get_session_history(limit)
    
    def check_from_flowstate(self, task_data, website_data):
        """
        从 FlowState 数据检查网站相关性
        
        参数:
            task_data: FlowState 任务数据
            website_data: FlowState 网站数据
        
        返回:
            dict: 检查结果
        """
        if not task_data or not website_data:
            return {
                "is_relevant": False,
                "action": "error",
                "reason": "FlowState 数据不完整",
                "confidence": "none"
            }
        
        # 构建任务描述
        task_name = task_data.get('name', '未知任务')
        resources = task_data.get('resources', [])
        
        # 构建任务描述，包含相关资源信息
        task_description = f"任务: {task_name}"
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
                task_description += f"\n相关资源: {', '.join(resource_descriptions)}"
        
        # 设置任务
        self.set_task(task_description)
        
        # 获取网站信息
        website_url = website_data.get('url', '')
        website_title = website_data.get('title', '')
        app_id = website_data.get('app_id', '')
        
        # 构建网站描述
        website_description = website_title if website_title else ""
        if app_id and app_id != "browser":
            website_description += f" (应用: {app_id})"
        
        # 检查网站
        return self.check_website(website_url, website_description if website_description else None)


def main():
    """主函数 - 交互式使用示例"""
    
    print("=" * 70)
    print("任务专注度监控工具")
    print("=" * 70)
    print("功能：帮助你保持专注，判断打开的网站是否与当前任务相关")
    print()
    
    # 创建监控器实例
    monitor = TaskFocusMonitor()
    
    # 第一步：设置任务
    print("第一步：请输入你当前要完成的任务")
    task = input("任务描述: ").strip()
    
    if not task:
        print("错误：任务描述不能为空")
        return
    
    monitor.set_task(task)
    
    # 第二步：循环检查网站
    print("第二步：现在可以输入要打开的网站URL进行检查")
    print("提示：")
    print("  - 输入网站URL进行检查")
    print("  - 输入 'quit' 退出")
    print("  - 输入 'end' 结束当前任务并查看专注度")
    print("  - 输入 'stats' 查看当前统计")
    print("  - 输入 'history' 查看专注度历史")
    print("  - 输入 'new' 设置新任务\n")
    
    while True:
        website_url = input("请输入网站URL (或命令): ").strip()
        
        if not website_url:
            continue
        
        # 处理命令
        if website_url.lower() == 'quit':
            print("\n感谢使用！")
            # 如果有活跃任务，询问是否结束
            if monitor.current_task:
                end_task = input("是否结束当前任务并查看专注度？(y/n): ").strip().lower()
                if end_task == 'y':
                    monitor.end_task()
            # 保存历史记录
            if monitor.check_history:
                save = input("是否保存检查历史？(y/n): ").strip().lower()
                if save == 'y':
                    monitor.save_history()
            break
        
        elif website_url.lower() == 'end':
            if monitor.current_task:
                monitor.end_task()
            else:
                print("❌ 没有活跃的任务")
            continue
        
        elif website_url.lower() == 'stats':
            monitor.print_statistics()
            continue
        
        elif website_url.lower() == 'history':
            monitor.print_focus_history()
            continue
        
        elif website_url.lower() == 'new':
            new_task = input("请输入新任务: ").strip()
            if new_task:
                monitor.set_task(new_task)
            continue
        
        # 可选：输入网站描述
        print("  (可选) 网站描述: ", end="")
        description = input().strip()
        
        # 检查网站
        result = monitor.check_website(
            website_url, 
            description if description else None
        )
        
        # 打印结果
        monitor.print_check_result(website_url, result)


if __name__ == "__main__":
    main()

