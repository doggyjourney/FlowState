# 🧪 任务记录和网站检测功能测试指南

## 📋 功能概述

这个仓库实现了智能任务专注度监控系统，核心功能包括：

1. **📝 任务记录** - 输入并保存当前要完成的任务
2. **🔍 网站检测** - 智能判断打开的网站是否与任务相关
3. **🎯 专注提醒** - 对无关网站给出关闭建议，帮助保持专注
4. **📊 统计分析** - 提供专注度统计和评分

## 🚀 快速开始测试

### 1. 环境准备

```bash
# 进入项目目录
cd /workspace/API/websiteChecker

# 安装依赖
pip3 install -r requirements.txt

# 设置API Key（可选，用于真实测试）
export GROQ_API_KEY='your-groq-api-key-here'
```

### 2. 运行模拟测试（推荐）

```bash
# 运行完整功能演示（不需要API Key）
python3 test_mock.py
```

这个测试会演示所有功能，包括：
- ✅ 任务记录功能
- ✅ 网站检测功能  
- ✅ 专注场景演示
- ✅ 完整工作流程

### 3. 运行真实测试（需要API Key）

```bash
# 运行真实功能测试（需要GROQ_API_KEY）
python3 test_functionality.py
```

## 🎯 测试场景详解

### 场景1: 学习编程任务

**任务**: "学习Python编程"

**测试网站**:
- ✅ `https://docs.python.org` - Python官方文档（相关）
- ✅ `https://stackoverflow.com` - 编程问答（相关）
- ✅ `https://github.com` - 代码托管（相关）
- ❌ `https://www.youtube.com` - 视频娱乐（无关）
- ❌ `https://www.instagram.com` - 社交媒体（无关）

**预期结果**: 教育和技术网站被标记为相关，娱乐网站被标记为无关

### 场景2: 写作业任务

**任务**: "写数学作业"

**测试网站**:
- ✅ `https://www.khanacademy.org` - 可汗学院（相关）
- ✅ `https://www.wolframalpha.com` - 数学计算工具（相关）
- ❌ `https://www.youtube.com` - 视频娱乐（无关）
- ❌ `https://www.tiktok.com` - 短视频（无关）

**预期结果**: 教育工具被标记为相关，娱乐平台被标记为无关

### 场景3: 工作场景

**任务**: "准备技术博客"

**测试网站**:
- ✅ `https://github.com` - 代码仓库（相关）
- ✅ `https://stackoverflow.com` - 技术问答（相关）
- ✅ `https://www.notion.so` - 笔记工具（相关）
- ❌ `https://www.reddit.com` - 论坛（无关）

**预期结果**: 生产力工具被标记为相关，娱乐论坛被标记为无关

## 🌐 Web界面测试

### 启动Web界面

```bash
# 启动Web服务器
python3 web_monitor.py

# 在浏览器中访问
# http://localhost:5000
```

### Web界面功能测试

1. **任务设置测试**
   - 在任务输入框中输入任务描述
   - 点击"设置任务"按钮
   - 验证任务显示在界面上

2. **网站检测测试**
   - 在网站输入框中输入URL
   - 点击"检查"按钮
   - 查看检测结果和理由

3. **统计功能测试**
   - 检查多个网站
   - 观察统计面板的实时更新
   - 验证相关/无关网站计数

4. **界面特性测试**
   - 测试响应式设计（调整浏览器窗口大小）
   - 测试键盘支持（回车键操作）
   - 测试加载动画和结果展示

## 📊 测试结果验证

### 成功标准

1. **任务记录功能**
   - ✅ 能够成功设置和保存任务
   - ✅ 任务描述正确显示
   - ✅ 支持任务切换

2. **网站检测功能**
   - ✅ 能够正确判断网站相关性
   - ✅ 提供合理的判断理由
   - ✅ 置信度评估准确

3. **专注提醒功能**
   - ✅ 对无关网站给出关闭建议
   - ✅ 对相关网站允许继续访问
   - ✅ 提醒信息清晰明确

4. **统计分析功能**
   - ✅ 正确统计检查次数
   - ✅ 准确计算相关/无关比例
   - ✅ 提供专注度评分

### 测试数据

运行测试后，你应该看到类似以下的输出：

```
🎯 专注度得分: 75.0%
评价: 良好，还有提升空间 👍

======================================================================
任务专注度统计
======================================================================
当前任务: 学习Python编程
检查网站总数: 6
相关网站: 4 (66.7%)
无关网站: 2 (33.3%)
======================================================================
```

## 🔧 故障排除

### 常见问题

1. **API Key错误**
   ```
   ❌ 错误: 需要设置 GROQ_API_KEY 环境变量
   ```
   **解决方案**: 设置正确的API Key或使用模拟测试

2. **依赖包缺失**
   ```
   ModuleNotFoundError: No module named 'groq'
   ```
   **解决方案**: 运行 `pip3 install -r requirements.txt`

3. **端口占用**
   ```
   Address already in use
   ```
   **解决方案**: 更改端口或停止占用端口的进程

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH=/workspace/API/websiteChecker
python3 -v test_mock.py

# 检查依赖
python3 -c "import groq, flask; print('Dependencies OK')"
```

## 📈 性能测试

### 批量测试

```bash
# 运行批量检查示例
python3 batch_check_example.py
```

### 压力测试

```python
# 创建压力测试脚本
import time
from test_mock import MockTaskFocusMonitor

monitor = MockTaskFocusMonitor()
monitor.set_task("压力测试")

start_time = time.time()
for i in range(100):
    monitor.check_website(f"https://example{i}.com")
end_time = time.time()

print(f"处理100个网站耗时: {end_time - start_time:.2f}秒")
```

## 🎯 集成测试

### FlowState集成测试

```bash
# 运行FlowState集成测试
python3 test_integration.py
```

### 自定义集成测试

```python
# 创建自定义测试
from task_focus_monitor import TaskFocusMonitor

def custom_test():
    monitor = TaskFocusMonitor()
    monitor.set_task("自定义任务")
    
    # 测试你的特定场景
    result = monitor.check_website("https://your-website.com")
    print(f"结果: {result}")

custom_test()
```

## 📝 测试报告模板

### 测试环境
- 操作系统: Linux 6.1.147
- Python版本: 3.x
- 依赖版本: groq>=0.4.0, flask>=2.3.0

### 测试结果
- [ ] 任务记录功能
- [ ] 网站检测功能
- [ ] 专注提醒功能
- [ ] 统计分析功能
- [ ] Web界面功能
- [ ] 集成测试

### 发现问题
- 问题描述:
- 重现步骤:
- 预期结果:
- 实际结果:

### 建议改进
- 功能改进:
- 性能优化:
- 用户体验:

## 🎉 测试完成

恭喜！你已经完成了任务记录和网站检测功能的全面测试。

### 下一步
1. 根据测试结果调整配置
2. 集成到你的工作流程中
3. 定期运行测试确保功能正常
4. 根据使用反馈持续改进

---

**📞 需要帮助？**
- 查看 `README.md` 了解详细文档
- 运行 `python3 demo.py` 查看完整演示
- 检查 `QUICKSTART.md` 快速上手指南