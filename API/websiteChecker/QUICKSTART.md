# 快速开始指南 - 任务专注度监控工具

## 🎯 核心概念

**工作原理：**
1. 先输入任务（如"写作业"）
2. 每次打开网站时，AI判断是否与任务相关
3. 相关→允许打开，不相关→建议关闭

## ⚡ 3分钟上手

### 第一步：安装

```bash
pip install groq flask
```

### 第二步：设置API Key

1. 访问 https://console.groq.com/keys 获取免费API Key
2. 设置环境变量：

```bash
export GROQ_API_KEY='你的API密钥'
```

### 第三步：运行

**选项A：命令行版本**
```bash
python task_focus_monitor.py
```

**选项B：Web界面版本（推荐）**
```bash
python web_monitor.py
# 然后打开浏览器访问 http://localhost:5000
```

**选项C：简化版本**
```bash
python simple_focus_monitor.py
```

## 📝 使用示例

### 命令行交互

```
$ python task_focus_monitor.py

任务专注度监控工具
======================================================================
请输入你当前要完成的任务
任务描述: 写数学作业

✓ 已设置当前任务: 写数学作业

请输入网站URL: https://www.youtube.com

======================================================================
网站检查结果: https://www.youtube.com
======================================================================
当前任务: 写数学作业
判断结果: ✗ 与任务无关
建议操作: 建议关闭
置信度: high

理由: YouTube是视频娱乐平台，与写数学作业无直接关系
======================================================================
✗ 此网站与任务无关，建议关闭以保持专注
```

### Python代码集成

```python
from task_focus_monitor import TaskFocusMonitor

# 创建监控器
monitor = TaskFocusMonitor()

# 设置任务
monitor.set_task("学习Python编程")

# 检查网站
result = monitor.check_website("https://docs.python.org")

if result['is_relevant']:
    print("✓ 可以打开")
else:
    print("✗ 建议关闭")
```

## 🎨 Web界面使用

1. 运行 `python web_monitor.py`
2. 打开浏览器访问 `http://localhost:5000`
3. 在"设置任务"框中输入任务，点击"设置任务"
4. 在"检查网站"框中输入URL，点击"检查"
5. 查看结果和统计信息

## 💡 实用技巧

### 技巧1：任务描述要具体

❌ 不好："学习"
✅ 好："学习Python的面向对象编程"

### 技巧2：使用命令

在命令行版本中：
- 输入 `stats` 查看统计
- 输入 `new` 设置新任务
- 输入 `quit` 退出并保存

### 技巧3：批量检查

```python
from batch_check_example import batch_check_websites

websites = [
    "https://www.youtube.com",
    "https://www.khanacademy.org",
    "https://www.netflix.com"
]

batch_check_websites("写数学作业", websites)
```

## 🔧 常见问题

**Q: 没有API Key怎么办？**
A: 访问 https://console.groq.com/keys 免费注册获取

**Q: 判断不准确怎么办？**
A: 
1. 让任务描述更具体
2. 添加网站描述
3. 使用更强大的模型

**Q: 如何保存历史记录？**
A: 在命令行版本中输入 `quit` 时会提示保存

## 📚 更多信息

查看完整文档：`README_v2.md`

## 🎯 应用场景

- ✅ 学生写作业时避免分心
- ✅ 程序员编程时保持专注
- ✅ 办公室工作时提高效率
- ✅ 内容创作时避免干扰

---

开始使用，保持专注！🚀

