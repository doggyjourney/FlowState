#!/usr/bin/env python3
"""
专注度监控CLI工具
"""

import sys
import time
import argparse
from enhanced_focus_monitor import EnhancedFocusMonitor


def main():
    parser = argparse.ArgumentParser(description="专注度监控CLI工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    start_parser = subparsers.add_parser('start', help='开始专注度监控')
    start_parser.add_argument('--task-id', help='任务ID')
    start_parser.add_argument('--task-name', help='任务名称')
    start_parser.add_argument('--auto', action='store_true', help='自动从FlowState获取任务')
    
    check_parser = subparsers.add_parser('check', help='检查当前网站')
    end_parser = subparsers.add_parser('end', help='结束专注度监控')
    status_parser = subparsers.add_parser('status', help='查看当前状态')
    
    history_parser = subparsers.add_parser('history', help='查看专注度历史')
    history_parser.add_argument('--days', type=int, default=30, help='查看天数')
    history_parser.add_argument('--limit', type=int, default=10, help='显示记录数量')
    
    stats_parser = subparsers.add_parser('stats', help='查看专注度统计')
    stats_parser.add_argument('--days', type=int, default=30, help='统计天数')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    monitor = EnhancedFocusMonitor()
    
    try:
        if args.command == 'start':
            if args.auto:
                success = monitor.start_task_monitoring()
                if success:
                    print("✅ 专注度监控已开始")
                else:
                    print("❌ 启动监控失败")
            else:
                if not args.task_name:
                    print("❌ 请提供任务名称 (--task-name)")
                    return
                
                success = monitor.start_task_monitoring(args.task_id, args.task_name)
                if success:
                    print("✅ 专注度监控已开始")
                else:
                    print("❌ 启动监控失败")
        
        elif args.command == 'check':
            result = monitor.check_current_website()
            if result["success"]:
                print(f"🌐 网站: {result['website_url']}")
                print(f"📝 标题: {result['website_title']}")
                print(f"🎯 相关: {'是' if result['is_relevant'] else '否'}")
                print(f"📊 置信度: {result['confidence']}")
                print(f"💭 理由: {result['reason']}")
                print(f"⭐ 当前专注度: {result['current_focus_score']:.1f}/100")
            else:
                print(f"❌ 检查失败: {result['error']}")
        
        elif args.command == 'end':
            result = monitor.end_task_monitoring()
            if result:
                print("✅ 专注度监控已结束")
            else:
                print("❌ 结束监控失败")
        
        elif args.command == 'status':
            status = monitor.get_current_status()
            if status["monitoring_active"]:
                print("🟢 监控状态: 活跃")
                print(f"📋 任务: {status['task_name']}")
                print(f"⏱️  时长: {status['duration_minutes']:.1f} 分钟")
                print(f"⭐ 专注度: {status['current_focus_score']:.1f}/100")
                print(f"✅ 相关网站: {status['relevant_websites']} 次")
                print(f"❌ 无关网站: {status['irrelevant_websites']} 次")
            else:
                print("🔴 监控状态: 未活跃")
                print(f"💬 {status['message']}")
        
        elif args.command == 'history':
            print(f"📈 专注度历史记录 (最近 {args.days} 天)")
            print("-" * 50)
            history = monitor.get_focus_history(args.limit)
            if history:
                for i, session in enumerate(history, 1):
                    print(f"{i:2d}. {session['start_time']} - {session['task_name']}")
                    print(f"    时长: {session['duration_minutes']:.1f}分钟 | 分数: {session['focus_score']:.1f}/100")
                    print(f"    相关: {session['relevant_websites']} | 无关: {session['irrelevant_websites']}")
                    print()
            else:
                print("暂无历史记录")
        
        elif args.command == 'stats':
            print(f"📊 专注度统计 (最近 {args.days} 天)")
            monitor.print_focus_history(args.days)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        if monitor.monitoring_active:
            print("正在结束监控...")
            monitor.end_task_monitoring()
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()