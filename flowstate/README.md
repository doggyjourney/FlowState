# FlowState CLI

智能分心检测和任务管理工具 - 帮助用户保持专注，提高工作效率。

## 功能特性

### 第一阶段（已完成）
- ✅ **任务管理**：创建、查看、管理任务
- ✅ **学习会话**：记录用户使用的应用和网站
- ✅ **资源启动**：启动任务相关的应用和网站
- ✅ **配置管理**：完整的配置系统，支持API密钥和用户偏好

### 第二阶段（准备就绪）
- 🔄 **分心检测**：基于Groq AI的智能分心检测
- 🔄 **实时监控**：持续监控用户活动并给出建议
- 🔄 **智能干预**：根据用户偏好自动或手动干预

## 安装和构建

```bash
cd flowstate
pnpm install
pnpm run build
```

开发模式（无需构建）：
```bash
pnpm run flow -- --help
```

## 快速开始

### 1. 配置API密钥
```bash
# 设置Groq API密钥（用于分心检测）
flow config:api-key groq your-groq-api-key

# 查看配置
flow config:show
```

### 2. 创建任务
```bash
# 创建新任务
flow task:create "写AI博客"
flow task:create "学习TypeScript"
```

### 3. 学习阶段
```bash
# 开始学习会话，记录使用的应用和网站
flow task:learn <taskId> -d 30 --with-detection
```

### 4. 工作阶段
```bash
# 启动任务相关资源
flow task:start <taskId>

# 开始实时监控（可选）
flow monitor:start <taskId> -i 5
```

## 主要命令

### 任务管理
```bash
flow task:create <name>              # 创建任务
flow task:list                       # 列出任务
flow task:show <taskId>              # 查看任务详情
flow task:learn [options] <taskId>   # 学习会话
flow task:start <taskId>             # 启动任务资源
```

### 配置管理
```bash
flow config:show                     # 查看配置
flow config:set <key> <value>        # 设置配置值
flow config:api-key <service> <key>  # 设置API密钥
flow config:validate                 # 验证配置
flow config:preferences --list       # 查看用户偏好
```

### 分心检测
```bash
flow monitor:start <taskId>          # 开始实时监控
```

## 配置选项

### 学习会话设置
- `learningSession.defaultDuration`: 默认学习时长（秒）
- `learningSession.autoStart`: 是否自动开始学习会话
- `learningSession.smartDeduplication`: 是否启用智能去重

### 分心检测设置
- `distractionDetection.enabled`: 是否启用分心检测
- `distractionDetection.sensitivity`: 检测敏感度（low/medium/high）
- `distractionDetection.autoIntervention`: 是否自动干预
- `distractionDetection.warningThreshold`: 警告阈值（0-1）

### 通知设置
- `notifications.enabled`: 是否启用通知
- `notifications.sound`: 是否播放声音
- `notifications.desktop`: 是否显示桌面通知

## 数据存储

- 任务数据：`~/.flowstate/store.json`
- 配置文件：`~/.flowstate/config.json`
- 日志文件：`~/.flowstate/logs/`

## 架构设计

### 核心组件
- **TaskStore**: 任务数据管理
- **ConfigManager**: 配置管理
- **LearningSession**: 学习会话管理
- **GroqDistractionDetector**: AI分心检测
- **SystemController**: 系统控制接口

### 扩展性
- 支持多种AI服务提供商（Groq、OpenAI、Anthropic）
- 可插拔的检测算法
- 灵活的配置系统
- 模块化的架构设计

## 开发说明

### 为真实系统控制做准备
- 实现 `SystemController` 接口，使用 Smithery MCP：
  - `openApp(appId)` 和 `openUrl(url)`
  - `subscribeActiveWindow(cb)` 流式传输焦点事件
- 在CLI启动时替换 `DevSystemController`

### 技术特性
- URL规范化去除hash和query以减少重复
- 学习会话按 `kind:id` 去重
- 支持TypeScript类型安全
- 完整的错误处理和验证

## 使用示例

详细的使用示例请参考 [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md)

## 许可证

MIT License
