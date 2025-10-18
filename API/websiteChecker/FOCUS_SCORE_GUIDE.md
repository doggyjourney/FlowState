# 专注度计算系统使用指南

## 概述

专注度计算系统是一个基于用户专注时长和网站访问行为的智能分析工具，能够帮助用户了解自己的专注情况并提供改进建议。

## 核心功能

### 1. 专注度计算
- **专注时长记录**: 自动记录用户的任务专注时间
- **网站访问分析**: 通过AI判断访问的网站是否与任务相关
- **专注度评分**: 基于时长和网站访问质量计算0-100分的专注度分数

### 2. 任务管理
- **任务开始**: 用户可以开始新的专注任务
- **任务结束**: 用户可以手动结束任务并查看专注度报告
- **实时监控**: 实时显示当前专注状态和分数

### 3. 历史记录和统计
- **会话历史**: 查看所有专注会话的历史记录
- **统计分析**: 提供详细的专注度统计和分析
- **趋势分析**: 帮助用户了解专注度的变化趋势

## 专注度评分算法

专注度分数由以下三个部分组成：

### 1. 时长分数 (最高40分)
- 每分钟专注时间获得2分
- 最多可获得40分

### 2. 效率分数 (最高60分)
- 基于相关网站访问比例计算
- 相关网站比例越高，分数越高
- 没有访问网站时给予满分

### 3. 分心惩罚 (最多扣20分)
- 每个无关网站访问扣除2分
- 最多扣除20分

### 最终分数 = 时长分数 + 效率分数 - 分心惩罚

## 使用方法

### 1. 基础使用

```python
from focus_score_calculator import FocusScoreCalculator

# 创建计算器实例
calculator = FocusScoreCalculator()

# 开始专注会话
session_id = calculator.start_session("task_001", "学习Python编程")

# 记录网站访问
calculator.record_website_check("https://docs.python.org", True, "high", "官方文档")
calculator.record_website_check("https://www.youtube.com", False, "high", "视频网站")

# 结束会话
ended_session = calculator.end_session()
```

### 2. 集成任务监控

```python
from enhanced_focus_monitor import EnhancedFocusMonitor

# 创建监控器
monitor = EnhancedFocusMonitor()

# 开始监控（自动从FlowState获取任务）
monitor.start_task_monitoring()

# 检查当前网站
result = monitor.check_current_website()

# 结束监控
monitor.end_task_monitoring()
```

### 3. 命令行使用

```bash
# 开始监控
python focus_cli.py start --auto

# 检查当前网站
python focus_cli.py check

# 查看状态
python focus_cli.py status

# 结束监控
python focus_cli.py end

# 查看历史记录
python focus_cli.py history --days 7 --limit 5

# 查看统计
python focus_cli.py stats --days 30
```

## 专注度等级

| 分数范围 | 等级 | 说明 |
|---------|------|------|
| 90-100  | 🌟 优秀 | 专注度很高，继续保持 |
| 80-89   | 👍 良好 | 专注度良好，有提升空间 |
| 70-79   | 👌 一般 | 专注度一般，需要改进 |
| 60-69   | ⚠️ 需要改进 | 专注度较低，建议减少分心 |
| 0-59    | ❌ 需要大幅改进 | 专注度很低，需要重新规划 |

## 数据存储

专注度数据存储在 `focus_sessions.json` 文件中，包含：
- 会话基本信息（ID、任务、时间）
- 网站访问记录
- 专注度分数和评级
- 统计信息

## 配置要求

### 环境变量
```bash
export GROQ_API_KEY="your_groq_api_key"
```

### 依赖包
```bash
pip install groq
```

## 示例场景

### 场景1：学习编程
- 任务：学习Python编程
- 相关网站：Python官方文档、Stack Overflow、GitHub
- 无关网站：YouTube、社交媒体、购物网站
- 目标：保持高专注度，减少无关网站访问

### 场景2：写论文
- 任务：撰写学术论文
- 相关网站：学术数据库、参考文献、写作工具
- 无关网站：娱乐网站、社交媒体
- 目标：长时间专注，提高效率

### 场景3：工作项目
- 任务：完成项目开发
- 相关网站：技术文档、项目管理工具、代码仓库
- 无关网站：新闻网站、娱乐内容
- 目标：保持工作状态，提高生产力

## 最佳实践

1. **定期查看统计**: 每周查看专注度统计，了解自己的专注模式
2. **设置合理目标**: 根据任务类型设置合理的专注度目标
3. **减少分心**: 识别并减少无关网站访问
4. **保持记录**: 定期记录和分析专注度变化
5. **持续改进**: 根据统计结果调整工作习惯

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查GROQ_API_KEY是否正确设置
   - 确认网络连接正常

2. **无法获取任务信息**
   - 确认FlowState项目路径正确
   - 检查任务是否已创建

3. **专注度分数异常**
   - 检查网站访问记录是否正确
   - 确认时长计算是否准确

### 调试模式

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看当前状态
monitor = EnhancedFocusMonitor()
status = monitor.get_current_status()
print(status)
```

## 扩展功能

### 自定义评分算法
可以修改 `_calculate_focus_score` 方法来实现自定义的评分逻辑。

### 集成其他AI服务
可以扩展支持OpenAI、Anthropic等其他AI服务。

### 数据导出
支持将专注度数据导出为CSV、JSON等格式。

## 更新日志

- v1.0.0: 基础专注度计算功能
- v1.1.0: 集成FlowState任务管理
- v1.2.0: 添加命令行工具
- v1.3.0: 增强统计和历史记录功能