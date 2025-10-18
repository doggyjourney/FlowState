## for cursor hackathon
### divide into three part
1. local (Smithery to control pc)
2. brain (gemini to make judgement)
3. frontend


## stage 1
//yongxi
TaskStore	✅ 实现了	任务的创建、保存到 ~/.flowstate/store.json、列表展示等。
LearningSession	✅ 模拟实现	可以运行，会打印“学习会话开始/结束”，但不连接真实网站或模型。
Launcher	🟡 模拟实现	只打印“正在启动任务…”的文字，还不会真正打开网站或应用。
DevSystemController	🟡 模拟实现	用于开发调试阶段，可能通过 console.log 模拟“打开 VSCode / 浏览器”。
CLI 命令	✅ 全部可运行	解析参数、调用对应逻辑、更新 store。

当前版本的 CLI 使用的是 DevSystemController（开发用控制器）。
它只是打印日志，不会真的操作系统或记录应用。
未来需要你手动替换为真正的 SystemController 实现，才能让它：

监控你访问的网站；

启动浏览器或应用；

记录时间/活动。

### 任务管理
- 创建，记录任务
- 查看任务
- 打开任务所需资源

~/.flowstate/web_log.txt 记录网站信息（验证日志功能是否正常）
