# 专注度计算系统

## 功能概述

专注度计算系统通过分析用户的专注时长和网站访问行为，计算0-100分的专注度分数，帮助用户了解并改善自己的专注情况。

## 核心功能

### 1. 专注度计算
- **时长记录**: 自动记录任务专注时间
- **网站分析**: AI判断访问网站是否与任务相关
- **分数计算**: 基于时长和网站访问质量计算专注度分数

### 2. 任务管理
- **任务开始/结束**: 用户可以开始和结束专注任务
- **实时监控**: 实时显示当前专注状态和分数
- **FlowState集成**: 与FlowState任务管理系统集成

### 3. 历史记录和统计
- **会话历史**: 查看所有专注会话记录
- **统计分析**: 提供详细的专注度统计
- **趋势分析**: 帮助了解专注度变化趋势

## 专注度评分算法

专注度分数由三个部分组成：

1. **时长分数** (最高40分): 每分钟专注时间获得2分
2. **效率分数** (最高60分): 基于相关网站访问比例计算
3. **分心惩罚** (最多扣20分): 每个无关网站访问扣除2分

**最终分数 = 时长分数 + 效率分数 - 分心惩罚**

## 文件结构

```
API/websiteChecker/
├── focus_score_calculator.py    # 专注度计算核心模块
├── enhanced_focus_monitor.py    # 增强版监控器
├── focus_cli.py                 # 命令行工具
├── task_focus_monitor.py        # 基础任务监控器
├── flowstate_bridge.py          # FlowState桥接器
├── test_focus_system.py         # 测试脚本
├── demo_focus_system.py         # 演示脚本
└── FOCUS_SCORE_GUIDE.md         # 详细使用指南
```

## 快速开始

### 1. 安装依赖
```bash
pip install groq
```

### 2. 设置API密钥
```bash
export GROQ_API_KEY="your_groq_api_key"
```

### 3. 基础使用
```python
from focus_score_calculator import FocusScoreCalculator

calculator = FocusScoreCalculator()
session_id = calculator.start_session("task_001", "学习Python编程")
calculator.record_website_check("https://docs.python.org", True, "high", "官方文档")
ended_session = calculator.end_session()
```

### 4. 命令行使用
```bash
# 开始监控
python focus_cli.py start --task-name "学习Python"

# 检查当前网站
python focus_cli.py check

# 查看状态
python focus_cli.py status

# 结束监控
python focus_cli.py end

# 查看历史
python focus_cli.py history --days 7
```

## 专注度等级

| 分数范围 | 等级 | 说明 |
|---------|------|------|
| 90-100  | 🌟 优秀 | 专注度很高，继续保持 |
| 80-89   | 👍 良好 | 专注度良好，有提升空间 |
| 70-79   | 👌 一般 | 专注度一般，需要改进 |
| 60-69   | ⚠️ 需要改进 | 专注度较低，建议减少分心 |
| 0-59    | ❌ 需要大幅改进 | 专注度很低，需要重新规划 |

## 测试和演示

### 运行测试
```bash
python test_focus_system.py
```

### 运行演示
```bash
python demo_focus_system.py
```

## 数据存储

专注度数据存储在 `focus_sessions.json` 文件中，包含：
- 会话基本信息（ID、任务、时间）
- 网站访问记录
- 专注度分数和评级
- 统计信息

## 扩展功能

- 支持自定义评分算法
- 可集成其他AI服务
- 支持数据导出
- 可扩展更多监控功能

## 注意事项

1. 需要有效的Groq API密钥
2. 确保网络连接正常
3. 数据文件会自动创建和更新
4. 建议定期备份数据文件