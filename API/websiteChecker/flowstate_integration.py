#!/usr/bin/env python3
"""
FlowState 集成脚本
实时监控 FlowState 任务和网站，使用 TaskFocusMonitor 进行专注度分析
"""

import os
import time
import json
import signal
import sys
from datetime import datetime
from pathlib import Path


os.environ["GROQ_API_KEY"] = "type in your own key"

# 导入我们的模块
from flowstate_bridge import FlowStateBridge
from task_focus_monitor import TaskFocusMonitor


class FlowStateIntegration:
    """FlowState 集成监控器"""
    
    def __init__(self, check_interval: int = 5):
        """
        初始化集成监控器
        
        参数:
            check_interval: 检查间隔（秒）
        """
        self.bridge = FlowStateBridge()
        self.monitor = TaskFocusMonitor()
        self.check_interval = check_interval
        self.running = False
        self.current_task_id = None
        self.last_website = None
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理退出信号"""
        print(f"\n收到信号 {signum}，正在停止监控...")
        self.stop()
        sys.exit(0)
    
    def start_monitoring(self):
        """开始监控"""
        print("=" * 70)
        print("FlowState 专注度监控器启动")
        print("=" * 70)
        print(f"检查间隔: {self.check_interval} 秒")
        print("按 Ctrl+C 停止监控\n")
        
        self.running = True
        
        while self.running:
            try:
                self._check_and_analyze()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"监控过程中出错: {e}")
                time.sleep(self.check_interval)
        
        print("\n监控已停止")
    
    def stop(self):
        """停止监控"""
        self.running = False
    
    def _check_and_analyze(self):
        """检查并分析当前状态"""
        # 获取当前任务
        current_task = self.bridge.get_current_task()
        
        # 检查任务是否发生变化
        if current_task and current_task.get('id') != self.current_task_id:
            self.current_task_id = current_task.get('id')
            print(f"\n📋 检测到新任务: {current_task.get('name', '未知任务')}")
            print(f"   任务ID: {self.current_task_id}")
            
            # 显示任务资源
            resources = current_task.get('resources', [])
            if resources:
                print(f"   相关资源: {len(resources)} 个")
                for i, resource in enumerate(resources[:3]):  # 只显示前3个
                    if resource.get('kind') == 'url':
                        print(f"     - {resource.get('title', '无标题')} ({resource.get('id', '')})")
                    elif resource.get('kind') == 'app':
                        print(f"     - {resource.get('title', '无标题')} ({resource.get('id', '')})")
        
        # 获取当前网站
        current_website = self.bridge.get_current_website()
        
        # 检查网站是否发生变化
        if current_website and current_website != self.last_website:
            self.last_website = current_website
            website_url = current_website.get('url', '')
            website_title = current_website.get('title', '')
            
            print(f"\n🌐 检测到网站访问: {website_title or website_url}")
            
            # 如果有当前任务，进行分析
            if current_task:
                self._analyze_website(current_task, current_website)
            else:
                print("   ⚠️  没有活跃任务，跳过分析")
        
        # 如果没有变化，显示状态点
        if not (current_task and current_task.get('id') != self.current_task_id) and \
           not (current_website and current_website != self.last_website):
            print(".", end="", flush=True)
    
    def _analyze_website(self, task_data, website_data):
        """分析网站与任务的相关性"""
        try:
            # 使用 TaskFocusMonitor 进行分析
            result = self.monitor.check_from_flowstate(task_data, website_data)
            
            # 显示分析结果
            website_url = website_data.get('url', '')
            website_title = website_data.get('title', '')
            
            print(f"   🔍 专注度分析结果:")
            print(f"      判断: {'✅ 相关' if result['is_relevant'] else '❌ 无关'}")
            print(f"      置信度: {result['confidence']}")
            print(f"      建议: {result['action']}")
            print(f"      理由: {result['reason']}")
            
            # 如果是不相关的网站，给出警告
            if not result['is_relevant'] and result['action'] == 'block':
                print(f"   ⚠️  警告: 当前网站可能分散注意力，建议关闭")
            
        except Exception as e:
            print(f"   ❌ 分析失败: {e}")
    
    def show_statistics(self):
        """显示统计信息"""
        if hasattr(self.monitor, 'print_statistics'):
            self.monitor.print_statistics()
    
    def save_history(self, filename: str = None):
        """保存历史记录"""
        if hasattr(self.monitor, 'save_history'):
            if filename:
                self.monitor.save_history(filename)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"flowstate_monitor_history_{timestamp}.json"
                self.monitor.save_history(filename)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FlowState 专注度监控器")
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        default=5, 
        help="检查间隔（秒，默认5秒）"
    )
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="显示统计信息"
    )
    parser.add_argument(
        "--save", 
        type=str, 
        help="保存历史记录到指定文件"
    )
    
    args = parser.parse_args()
    
    # 创建集成监控器
    integration = FlowStateIntegration(check_interval=args.interval)
    
    if args.stats:
        # 显示统计信息
        integration.show_statistics()
    elif args.save:
        # 保存历史记录
        integration.save_history(args.save)
    else:
        # 开始监控
        integration.start_monitoring()


if __name__ == "__main__":
    main()
