"""
简化版任务专注度监控 - 使用 Groq API
快速判断网站是否与任务相关
"""

import os
from groq import Groq


class SimpleFocusMonitor:
    """简化版任务专注度监控器"""
    
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.task = None
    
    def set_task(self, task):
        """设置当前任务"""
        self.task = task
        print(f"✓ 当前任务: {task}\n")
    
    def check(self, website_url):
        """
        检查网站是否与任务相关
        
        返回: (是否相关, 理由)
        """
        if not self.task:
            return False, "请先设置任务"
        
        prompt = f"""任务: {self.task}
网站: {website_url}

这个网站是否有助于完成任务？只回答"是"或"否"，并简短说明理由。"""
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=256
        )
        
        answer = response.choices[0].message.content
        is_relevant = answer.startswith("是")
        
        return is_relevant, answer


# 使用示例
if __name__ == "__main__":
    monitor = SimpleFocusMonitor()
    
    # 设置任务
    task = input("请输入当前任务: ")
    monitor.set_task(task)
    
    # 循环检查网站
    while True:
        url = input("\n输入网站URL (输入 quit 退出): ")
        
        if url.lower() == 'quit':
            break
        
        is_relevant, reason = monitor.check(url)
        
        print("\n" + "="*50)
        if is_relevant:
            print("✓ 与任务相关 - 可以打开")
        else:
            print("✗ 与任务无关 - 建议关闭")
        print(f"理由: {reason}")
        print("="*50)

