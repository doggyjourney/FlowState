# FlowState 使用示例

## 配置管理

### 查看当前配置
```bash
# 查看配置概览
flow config:show

# 查看详细配置（JSON格式）
flow config:show --json

# 查看用户偏好设置
flow config:preferences --list
```

### 设置API密钥
```bash
# 设置Groq API密钥（用于分心检测）
flow config:api-key groq your-groq-api-key-here

# 验证配置
flow config:validate
```

### 调整用户偏好
```bash
# 设置学习会话默认时长为60秒
flow config:set learningSession.defaultDuration 60

# 启用自动干预
flow config:set distractionDetection.autoIntervention true

# 调整检测敏感度为高
flow config:set distractionDetection.sensitivity high

# 设置警告阈值为0.8
flow config:set distractionDetection.warningThreshold 0.8

# 启用桌面通知
flow config:set notifications.desktop true
```

## 任务管理

### 创建和管理任务
```bash
# 创建新任务
flow task:create "写AI博客"
flow task:create "学习TypeScript"
flow task:create "准备演讲"

# 查看任务列表
flow task:list

# 查看特定任务详情
flow task:show task_1760775428341_7kp8hs
```

### 学习会话（记录使用的应用和网站）
```bash
# 基本学习会话（30秒，使用配置中的默认时长）
flow task:learn task_1760775428341_7kp8hs

# 自定义时长的学习会话
flow task:learn task_1760775428341_7kp8hs -d 60

# 带分心检测的学习会话
flow task:learn task_1760775428341_7kp8hs -d 30 --with-detection
```

### 启动任务资源
```bash
# 启动任务相关的应用和网站
flow task:start task_1760775428341_7kp8hs
```

## 分心检测监控

### 实时监控
```bash
# 开始实时监控（每5秒检查一次）
flow monitor:start task_1760775428341_7kp8hs

# 自定义检查间隔（每2秒检查一次）
flow monitor:start task_1760775428341_7kp8hs -i 2

# 按Ctrl+C停止监控
```

## 配置示例

### 完整的配置文件示例
```json
{
  "version": "1.0.0",
  "userPreferences": {
    "learningSession": {
      "defaultDuration": 30,
      "autoStart": false,
      "smartDeduplication": true
    },
    "distractionDetection": {
      "enabled": true,
      "sensitivity": "medium",
      "autoIntervention": false,
      "warningThreshold": 0.7
    },
    "notifications": {
      "enabled": true,
      "sound": true,
      "desktop": true
    },
    "ui": {
      "theme": "auto",
      "language": "en",
      "showAdvanced": false
    }
  },
  "apiConfig": {
    "groq": {
      "apiKey": "your-groq-api-key",
      "model": "llama-3.1-8b-instant",
      "baseUrl": "https://api.groq.com/openai/v1",
      "timeout": 30000
    }
  },
  "system": {
    "dataDir": "/home/user/.flowstate",
    "logLevel": "info",
    "maxLogFiles": 10
  },
  "tasks": {
    "autoSave": true,
    "maxHistoryDays": 30,
    "defaultTaskDuration": 25
  }
}
```

## 工作流程示例

### 1. 初始设置
```bash
# 1. 设置Groq API密钥
flow config:api-key groq your-api-key

# 2. 调整偏好设置
flow config:set distractionDetection.sensitivity high
flow config:set learningSession.defaultDuration 45

# 3. 验证配置
flow config:validate
```

### 2. 创建任务
```bash
# 创建工作任务
flow task:create "完成项目报告"
flow task:create "准备会议材料"
```

### 3. 学习阶段
```bash
# 开始学习会话，记录使用的应用和网站
flow task:learn task_xxx -d 60 --with-detection
```

### 4. 工作阶段
```bash
# 启动任务相关资源
flow task:start task_xxx

# 开始实时监控（可选）
flow monitor:start task_xxx -i 5
```

## 故障排除

### 常见问题

1. **API密钥未配置**
   ```
   Error: Groq API key not configured
   Solution: flow config:api-key groq your-key
   ```

2. **配置验证失败**
   ```
   Error: Configuration has errors
   Solution: flow config:validate 查看具体错误
   ```

3. **任务未找到**
   ```
   Error: Task not found
   Solution: flow task:list 查看可用任务
   ```

### 重置配置
```bash
# 重置为默认配置
flow config:reset --force
```