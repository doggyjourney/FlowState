# 任务专注度监控工具

使用 Groq API 实现的智能任务专注度监控系统，帮助你保持专注，避免在工作学习时被无关网站分散注意力。

## 🎯 核心功能

**工作流程：**

1. **第一步**：输入当前要完成的任务（例如："写作业"）
2. **第二步**：每次打开网站前，系统使用 Groq API 判断该网站是否属于任务主题
3. **判断结果**：
   - ✅ **属于任务主题** → 允许打开，继续工作
   - ❌ **不属于任务主题** → 提示关闭，保持专注

## 📦 项目文件

### 核心文件

1. **task_focus_monitor.py** - 完整版任务专注度监控器
   - 面向对象设计，功能完整
   - 支持历史记录保存和统计
   - 提供详细的检查结果和置信度
   - 交互式命令行界面

2. **simple_focus_monitor.py** - 简化版监控器
   - 简洁的API接口
   - 快速集成到现有项目
   - 适合快速原型开发

3. **web_monitor.py** - Web界面版本
   - 美观的图形界面
   - 实时统计显示
   - 易于使用，无需命令行

4. **batch_check_example.py** - 批量检查示例
   - 一次性检查多个网站
   - 适合预先规划和分析

### 配置文件

- **requirements.txt** - Python依赖包
- **.env.example** - 环境变量配置示例

## 🚀 快速开始

### 安装依赖

```bash
pip install groq flask
```

### 设置 API Key

1. 访问 [Groq Console](https://console.groq.com/keys) 获取免费 API Key
2. 设置环境变量：

```bash
# Linux/Mac
export GROQ_API_KEY='your-api-key-here'

# Windows PowerShell
$env:GROQ_API_KEY='your-api-key-here'

# Windows CMD
set GROQ_API_KEY=your-api-key-here
```

### 使用方法

#### 方法一：命令行版本（推荐）

```bash
python task_focus_monitor.py
```

**使用流程：**
```
1. 输入任务：写数学作业
2. 输入网站：https://www.youtube.com
3. 查看结果：✗ 与任务无关 - 建议关闭
```

**支持的命令：**
- 输入网站URL：检查网站
- `stats`：查看统计信息
- `new`：设置新任务
- `quit`：退出并保存历史

#### 方法二：Web界面版本（最易用）

```bash
python web_monitor.py
```

然后在浏览器中访问：`http://localhost:5000`

**特点：**
- 🎨 美观的图形界面
- 📊 实时统计显示
- ⚡ 快速响应
- 📱 支持移动端

#### 方法三：简化版本（快速集成）

```python
from simple_focus_monitor import SimpleFocusMonitor

monitor = SimpleFocusMonitor()
monitor.set_task("写作业")

is_relevant, reason = monitor.check("https://www.youtube.com")
print(f"结果: {'相关' if is_relevant else '无关'}")
print(f"理由: {reason}")
```

## 💡 使用示例

### 示例1：学习场景

```python
from task_focus_monitor import TaskFocusMonitor

monitor = TaskFocusMonitor()
monitor.set_task("学习Python编程")

# 检查相关网站
result1 = monitor.check_website("https://docs.python.org")
# 结果: ✓ 与任务相关 - Python官方文档

result2 = monitor.check_website("https://www.instagram.com")
# 结果: ✗ 与任务无关 - 社交媒体

monitor.print_check_result("https://docs.python.org", result1)
monitor.print_statistics()
```

### 示例2：工作场景

```python
monitor = TaskFocusMonitor()
monitor.set_task("准备项目报告")

websites = [
    "https://docs.google.com",      # ✓ 相关
    "https://www.netflix.com",      # ✗ 无关
    "https://www.canva.com",        # ✓ 相关（设计工具）
    "https://twitter.com",          # ✗ 无关
]

for site in websites:
    result = monitor.check_website(site)
    print(f"{site}: {'✓' if result['is_relevant'] else '✗'}")
```

### 示例3：集成到浏览器扩展

```python
# 在浏览器扩展的后端服务中使用
from task_focus_monitor import TaskFocusMonitor

monitor = TaskFocusMonitor()

def on_tab_opened(url):
    """当用户打开新标签页时调用"""
    result = monitor.check_website(url)
    
    if not result['is_relevant']:
        # 显示警告提示
        show_warning(f"此网站与任务无关：{result['reason']}")
        # 可选：自动关闭标签页
        # close_tab()
    
    return result
```

## 📊 功能详解

### TaskFocusMonitor 类

**主要方法：**

```python
monitor = TaskFocusMonitor(api_key=None)

# 设置任务
monitor.set_task("任务描述")

# 检查网站
result = monitor.check_website(
    website_url="https://example.com",
    website_description="可选的网站描述"
)

# 打印结果
monitor.print_check_result(website_url, result)

# 查看统计
monitor.print_statistics()

# 保存历史
monitor.save_history("history.json")

# 获取历史记录
history = monitor.get_history()
```

**返回结果格式：**

```python
{
    "is_relevant": bool,        # 是否与任务相关
    "action": str,              # "allow" 或 "block"
    "reason": str,              # 判断理由
    "confidence": str,          # "high", "medium", "low"
    "raw_response": str         # API原始响应
}
```

### 历史记录格式

```json
{
  "task": "写数学作业",
  "history": [
    {
      "timestamp": "2025-10-18T15:30:00",
      "website_url": "https://www.khanacademy.org",
      "task": "写数学作业",
      "result": {
        "is_relevant": true,
        "action": "allow",
        "reason": "可汗学院提供数学学习资源",
        "confidence": "high"
      }
    }
  ]
}
```

## 🎨 Web界面预览

Web界面包含以下功能：

- **任务设置区域**：输入当前任务
- **网站检查区域**：输入要检查的网站URL
- **结果显示**：清晰显示是否相关及理由
- **统计面板**：实时显示检查次数、相关/无关网站数量

界面采用现代化设计，支持响应式布局，可在手机、平板、电脑上使用。

## ⚙️ 配置说明

### 模型选择

默认使用 `llama-3.3-70b-versatile` 模型，可以修改为其他模型：

```python
# 在 task_focus_monitor.py 中修改
chat_completion = self.client.chat.completions.create(
    model="llama-3.1-8b-instant",  # 更快的模型
    # 或
    model="openai/gpt-oss-120b",   # 更强大的模型
    ...
)
```

### 判断严格度

通过调整 `temperature` 参数控制判断的严格度：

```python
temperature=0.2  # 更严格、更一致（推荐）
temperature=0.5  # 中等
temperature=0.8  # 更宽松、更灵活
```

### 自定义判断标准

修改 `check_website` 方法中的 `prompt` 变量：

```python
prompt = f"""我正在执行的任务是：{self.current_task}

现在我想打开以下网站：{website_url}

判断标准：
1. 如果网站内容直接有助于完成任务，判定为"相关"
2. 如果网站是娱乐、社交、购物等与任务无关的内容，判定为"不相关"
3. [添加你的自定义标准]

请判断这个网站是否与我的任务主题相关。"""
```

## 🔧 高级用法

### 1. 添加白名单/黑名单

```python
class TaskFocusMonitor:
    def __init__(self):
        # ...
        self.whitelist = ["docs.python.org", "stackoverflow.com"]
        self.blacklist = ["facebook.com", "twitter.com"]
    
    def check_website(self, website_url):
        # 检查白名单
        if any(domain in website_url for domain in self.whitelist):
            return {"is_relevant": True, "action": "allow", ...}
        
        # 检查黑名单
        if any(domain in website_url for domain in self.blacklist):
            return {"is_relevant": False, "action": "block", ...}
        
        # 使用AI判断
        return self._ai_check(website_url)
```

### 2. 定时提醒

```python
import time
from datetime import datetime

def focus_session(task, duration_minutes=25):
    """番茄工作法：专注时段"""
    monitor = TaskFocusMonitor()
    monitor.set_task(task)
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    print(f"开始专注时段: {duration_minutes}分钟")
    
    while time.time() < end_time:
        # 检查网站...
        time.sleep(1)
    
    print("专注时段结束！")
    monitor.print_statistics()
```

### 3. 与浏览器集成

可以开发浏览器扩展，实时监控打开的网站：

**架构：**
- 浏览器扩展（前端）→ 本地服务器（Flask）→ TaskFocusMonitor

**实现步骤：**
1. 运行 `web_monitor.py` 作为后端服务
2. 开发浏览器扩展调用 `/check_website` API
3. 在扩展中显示检查结果

### 4. 数据分析

```python
import json
import matplotlib.pyplot as plt

# 加载历史记录
with open('task_focus_history.json', 'r') as f:
    data = json.load(f)

# 分析专注度
history = data['history']
relevant_count = sum(1 for h in history if h['result']['is_relevant'])
total_count = len(history)

focus_rate = relevant_count / total_count * 100

print(f"专注度: {focus_rate:.1f}%")

# 可视化
# ... 绘制图表
```

## 📈 应用场景

### 1. 学生学习

- **场景**：写作业、准备考试
- **效果**：避免被社交媒体、视频网站分散注意力
- **任务示例**：
  - "写数学作业"
  - "准备英语考试"
  - "学习物理第三章"

### 2. 程序员工作

- **场景**：编程、调试、学习新技术
- **效果**：保持专注于技术文档和开发工具
- **任务示例**：
  - "开发用户登录功能"
  - "学习React框架"
  - "修复Bug #123"

### 3. 内容创作

- **场景**：写作、设计、视频制作
- **效果**：专注于创作工具和参考资料
- **任务示例**：
  - "写博客文章"
  - "设计产品海报"
  - "剪辑视频"

### 4. 企业办公

- **场景**：准备报告、数据分析
- **效果**：避免工作时间浏览无关网站
- **任务示例**：
  - "准备季度报告"
  - "分析销售数据"
  - "制作演示文稿"

## 🔒 隐私与安全

- **本地运行**：所有代码在本地运行，不上传数据到第三方
- **API调用**：仅向 Groq API 发送任务描述和网站URL
- **数据存储**：历史记录保存在本地JSON文件中
- **开源透明**：代码完全开源，可自行审查

## ❓ 常见问题

### Q1: 如何获取 Groq API Key？

访问 [Groq Console](https://console.groq.com/keys) 注册账号（免费），创建 API Key。

### Q2: API 有使用限制吗？

免费版有速率限制（每分钟请求数），但对个人使用足够。详见 [Groq Rate Limits](https://console.groq.com/docs/rate-limits)。

### Q3: 判断准确吗？

准确率取决于：
- 任务描述的清晰度
- 网站URL的明确性
- 使用的AI模型

建议：
- 任务描述要具体（"写数学作业" 比 "学习" 更好）
- 可以添加网站描述提高准确性
- 使用更强大的模型（如 gpt-oss-120b）

### Q4: 可以离线使用吗？

不可以，需要网络连接调用 Groq API。但可以添加缓存机制减少API调用。

### Q5: 如何集成到现有项目？

```python
# 简单集成
from simple_focus_monitor import SimpleFocusMonitor

monitor = SimpleFocusMonitor()
monitor.set_task("你的任务")

# 在需要检查的地方调用
is_relevant, reason = monitor.check(website_url)
if not is_relevant:
    # 执行阻止操作
    pass
```

### Q6: 支持多任务吗？

当前版本一次只支持一个任务。如需多任务，可以创建多个 `TaskFocusMonitor` 实例。

### Q7: 如何提高响应速度？

1. 使用更快的模型（如 `llama-3.1-8b-instant`）
2. 添加缓存机制
3. 使用白名单/黑名单减少API调用

## 🛠️ 技术栈

- **AI模型**：Groq API (Llama 3.3 70B)
- **后端**：Python 3.7+
- **Web框架**：Flask
- **前端**：HTML5 + CSS3 + JavaScript
- **数据存储**：JSON文件

## 📝 更新日志

### v2.0 (2025-10-18)

- ✨ 重新设计：改为"先设置任务，再检查网站"的工作流程
- 🎨 新增Web界面版本
- 📊 添加统计功能和历史记录
- 🚀 提供批量检查功能
- 📚 完善文档和示例

### v1.0 (2025-10-18)

- 🎉 初始版本：基本的序列任务判断功能

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 可自由使用和修改

## 🔗 相关资源

- [Groq 官方文档](https://console.groq.com/docs)
- [Groq API 参考](https://console.groq.com/docs/api-reference)
- [Groq Python 库](https://github.com/groq/groq-python)
- [Flask 文档](https://flask.palletsprojects.com/)

## 💬 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件
- 在讨论区留言

---

**让我们一起保持专注，高效完成任务！🎯**

