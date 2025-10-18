# FlowState 集成使用指南

本指南介绍如何使用 FlowState 与 TaskFocusMonitor 的集成功能，实现基于 FlowState 任务数据的网站专注度监控。

## 功能概述

这个集成系统能够：
1. 从 FlowState 获取当前任务和资源信息
2. 监控当前访问的网站
3. 使用 AI 分析网站与任务的相关性
4. 提供专注度建议和警告

## 文件结构

```
API/websiteChecker/
├── task_focus_monitor.py          # 原有的专注度监控器
├── flowstate_bridge.py           # FlowState 数据桥接器
├── flowstate_integration.py      # 集成监控脚本
├── test_integration.py           # 测试脚本
└── FLOWSTATE_INTEGRATION.md      # 本文档
```

## 安装依赖

确保已安装必要的 Python 包：

```bash
pip install groq
```

## 配置

### 1. 设置 Groq API 密钥

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 2. 确保 FlowState 已构建

在 FlowState 目录中运行：

```bash
cd /workspace/flowstate
npm run build
```

## 使用方法

### 1. 基本使用

运行集成监控器：

```bash
cd /workspace/API/websiteChecker
python flowstate_integration.py
```

这将启动实时监控，每5秒检查一次当前任务和网站状态。

### 2. 自定义检查间隔

```bash
python flowstate_integration.py -i 10  # 每10秒检查一次
```

### 3. 查看统计信息

```bash
python flowstate_integration.py --stats
```

### 4. 保存历史记录

```bash
python flowstate_integration.py --save my_history.json
```

### 5. 测试集成功能

```bash
python test_integration.py
```

## 工作原理

### 数据流程

1. **FlowState 数据获取**：
   - 通过 `flowstate_bridge.py` 调用 FlowState CLI
   - 获取当前任务信息和资源列表
   - 获取当前活动窗口/网站信息

2. **数据格式化**：
   - 将 FlowState 任务数据转换为 TaskFocusMonitor 可理解的格式
   - 包含任务名称、相关资源等信息

3. **专注度分析**：
   - 使用 TaskFocusMonitor 的 AI 分析功能
   - 判断当前网站是否与任务相关
   - 提供置信度和建议

4. **实时监控**：
   - 定期检查任务和网站状态变化
   - 在状态变化时触发分析
   - 显示分析结果和警告

### 支持的数据类型

**任务数据**：
- 任务ID和名称
- 相关资源列表（URL和应用程序）
- 创建和更新时间

**网站数据**：
- 当前访问的URL
- 页面标题
- 应用程序ID

## 配置选项

### 环境变量

- `GROQ_API_KEY`: Groq API 密钥（必需）
- `FLOWSTATE_PATH`: FlowState 项目路径（可选，默认为 `../flowstate`）

### 命令行参数

- `-i, --interval`: 检查间隔（秒）
- `--stats`: 显示统计信息
- `--save`: 保存历史记录到文件

## 故障排除

### 常见问题

1. **"无法获取当前任务"**
   - 确保 FlowState 已正确构建
   - 检查 FlowState 项目路径是否正确
   - 确保有活跃的任务

2. **"Groq API 调用失败"**
   - 检查 GROQ_API_KEY 环境变量
   - 确保 API 密钥有效且有足够配额

3. **"无法导入 task_focus_monitor"**
   - 确保在正确的目录中运行脚本
   - 检查 Python 路径设置

### 调试模式

启用详细日志输出：

```bash
python -u flowstate_integration.py -i 1  # 更频繁的检查用于调试
```

## 扩展功能

### 自定义分析逻辑

可以修改 `flowstate_bridge.py` 中的 `format_task_for_monitor` 方法来自定义任务描述格式。

### 添加新的数据源

可以扩展 `FlowStateBridge` 类来支持其他数据源，如：
- 浏览器扩展数据
- 系统活动监控
- 其他任务管理工具

### 自定义警告机制

可以修改 `flowstate_integration.py` 中的 `_analyze_website` 方法来添加自定义的警告和通知机制。

## 示例输出

```
======================================================================
FlowState 专注度监控器启动
======================================================================
检查间隔: 5 秒
按 Ctrl+C 停止监控

📋 检测到新任务: 学习Python编程
   任务ID: task_1234567890_abc123
   相关资源: 3 个
     - Python官方文档 (https://docs.python.org)
     - Stack Overflow (https://stackoverflow.com)
     - VS Code (code)

🌐 检测到网站访问: YouTube - 视频标题
   🔍 专注度分析结果:
      判断: ❌ 无关
      置信度: high
      建议: block
      理由: 这是一个娱乐视频网站，与学习Python编程任务无关
   ⚠️  警告: 当前网站可能分散注意力，建议关闭
```

## 注意事项

1. 这是一个开发版本，某些功能可能不稳定
2. 确保 FlowState 项目已正确配置和构建
3. 监控功能会持续运行，记得在不需要时停止
4. 建议在测试环境中先验证功能正常

## 贡献

欢迎提交问题和改进建议！