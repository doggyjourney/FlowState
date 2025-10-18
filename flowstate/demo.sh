#!/bin/bash

echo "🚀 FlowState CLI 演示脚本"
echo "=========================="

# 检查是否已构建
if [ ! -f "dist/cli.js" ]; then
    echo "📦 构建项目..."
    pnpm run build
fi

echo ""
echo "1️⃣ 查看当前配置"
echo "----------------"
node dist/cli.js config:show

echo ""
echo "2️⃣ 设置一些配置"
echo "----------------"
node dist/cli.js config:set learningSession.defaultDuration 45
node dist/cli.js config:set distractionDetection.sensitivity high
node dist/cli.js config:set notifications.desktop true

echo ""
echo "3️⃣ 验证配置"
echo "------------"
node dist/cli.js config:validate

echo ""
echo "4️⃣ 创建测试任务"
echo "----------------"
TASK_ID=$(node dist/cli.js task:create "演示任务" | grep -o 'task_[^[:space:]]*')
echo "创建的任务ID: $TASK_ID"

echo ""
echo "5️⃣ 查看任务列表"
echo "----------------"
node dist/cli.js task:list

echo ""
echo "6️⃣ 开始学习会话（5秒）"
echo "----------------------"
node dist/cli.js task:learn $TASK_ID -d 5 --with-detection

echo ""
echo "7️⃣ 查看任务详情"
echo "----------------"
node dist/cli.js task:show $TASK_ID

echo ""
echo "8️⃣ 启动任务资源"
echo "----------------"
node dist/cli.js task:start $TASK_ID

echo ""
echo "9️⃣ 查看用户偏好设置"
echo "-------------------"
node dist/cli.js config:preferences --list

echo ""
echo "✅ 演示完成！"
echo ""
echo "💡 提示："
echo "   - 设置真实的Groq API密钥以启用分心检测"
echo "   - 使用 'flow monitor:start $TASK_ID' 开始实时监控"
echo "   - 查看 USAGE_EXAMPLES.md 获取更多使用示例"