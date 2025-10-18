FlowState - 实现说明与注入指南 (最终版)

一、已实现
- 决策 server (/api/decide)：保留 Gemini 注入点（注释），默认回退至局部启发式判断（黑名单/白名单/token-overlap）。
- Agent：每 5s 循环读取前台窗口。仅在窗口变更或自上次发送 >=60s 时向决策服务发送一次请求。
- 安全策略：连续两次 DISTRACTION 或 confidence>=80 才会执行真正的 close；否则降级为 popup。
- 直接关闭：agent 内置跨平台系统命令模板（macOS: osascript; Win: taskkill; Linux: pkill）。默认仅模拟，需显式通过 ALLOW_DIRECT_KILL=true 启用。

二、待实现 / 可选
- 真正的 Gemini 集成（示例已注释）并使用 function-calling以获得稳定 JSON输出。
- Smithery 集成（生产推荐）以便获得权限控制和审计；当前实现用系统命令作为替代。
- 前端 UI 与持久化数据库，用于多用户/任务历史。

三、如何注入 Gemini（简要）
1) 在 Google Cloud 创建 Project，启用 Vertex AI，创建服务帐号并下载 JSON key（存放在服务器并设置 GOOGLE_APPLICATION_CREDENTIALS）。
2) 在 mock_decide_server/index.js 注释处写入调用 Vertex AI 的代码（使用 @google-cloud/aiplatform 或 REST）。
3) 使用严格系统提示词，要求模型**仅输出 JSON**，或使用 function-calling。
4) 验证模型输出并在 parse 成功时返回；parse 失败时回退到本地启发式。
5) 记录原始模型响应供审计和调试。

四、注意事项（演示）
- 在启用 ALLOW_DIRECT_KILL 前，请把 CLOSABLE_APPS 设置为仅包含可安全关闭的应用（例如 Chrome、Twitter 等），并不要包含系统进程（Finder、explorer 等）。
- 演示时建议默认使用模拟模式；若要展示真实关闭，请在演示前单机测试并确认权限。
