"""
Web界面版任务专注度监控 - 使用 Flask
提供简单的Web界面进行任务设置和网站检查
"""

import os
from flask import Flask, render_template_string, request, jsonify

# 硬编码 GROQ API Key（按你的要求）
os.environ["GROQ_API_KEY"] = "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"

from task_focus_monitor import TaskFocusMonitor

app = Flask(__name__)
monitor = TaskFocusMonitor()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务专注度监控</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: #444;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: "";
            width: 4px;
            height: 20px;
            background: #667eea;
            margin-right: 10px;
            border-radius: 2px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .current-task {
            background: #f8f9ff;
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin-bottom: 20px;
        }
        
        .current-task strong {
            color: #667eea;
        }
        
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result.relevant {
            background: #d4edda;
            border-left: 4px solid #28a745;
        }
        
        .result.irrelevant {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }
        
        .result-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .result.relevant .result-title {
            color: #155724;
        }
        
        .result.irrelevant .result-title {
            color: #721c24;
        }
        
        .result-reason {
            color: #333;
            line-height: 1.6;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 10px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 10px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 任务专注度监控</h1>
        <p class="subtitle">帮助你保持专注，判断网站是否与当前任务相关</p>
        
        <div class="section">
            <div class="section-title">第一步：设置任务</div>
            <div class="input-group">
                <input type="text" id="taskInput" placeholder="例如：写数学作业、学习Python编程">
                <button onclick="setTask()">设置任务</button>
            </div>
            <div id="currentTask" style="display:none;" class="current-task">
                <strong>当前任务：</strong><span id="taskName"></span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">第二步：检查网站</div>
            <div class="input-group">
                <input type="text" id="websiteInput" placeholder="输入网站URL，例如：https://www.youtube.com">
                <button onclick="checkWebsite()">检查</button>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在分析...</p>
            </div>
            <div id="result"></div>
        </div>
        
        <div class="section">
            <div class="section-title">统计信息</div>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="totalChecks">0</div>
                    <div class="stat-label">总检查次数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="relevantCount">0</div>
                    <div class="stat-label">相关网站</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="irrelevantCount">0</div>
                    <div class="stat-label">无关网站</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let stats = {
            total: 0,
            relevant: 0,
            irrelevant: 0
        };
        
        function setTask() {
            const task = document.getElementById('taskInput').value.trim();
            if (!task) {
                alert('请输入任务描述');
                return;
            }
            
            fetch('/set_task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task: task})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('currentTask').style.display = 'block';
                document.getElementById('taskName').textContent = task;
                document.getElementById('result').innerHTML = '';
                stats = {total: 0, relevant: 0, irrelevant: 0};
                updateStats();
            });
        }
        
        function checkWebsite() {
            const website = document.getElementById('websiteInput').value.trim();
            if (!website) {
                alert('请输入网站URL');
                return;
            }
            
            const currentTask = document.getElementById('taskName').textContent;
            if (!currentTask) {
                alert('请先设置任务');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
            
            fetch('/check_website', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({website: website})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                const resultDiv = document.getElementById('result');
                const isRelevant = data.is_relevant;
                
                stats.total++;
                if (isRelevant) {
                    stats.relevant++;
                } else {
                    stats.irrelevant++;
                }
                updateStats();
                
                resultDiv.className = 'result ' + (isRelevant ? 'relevant' : 'irrelevant');
                resultDiv.innerHTML = `
                    <div class="result-title">
                        ${isRelevant ? '✓ 与任务相关 - 可以打开' : '✗ 与任务无关 - 建议关闭'}
                    </div>
                    <div class="result-reason">${data.reason}</div>
                `;
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('检查失败: ' + error);
            });
        }
        
        function updateStats() {
            document.getElementById('totalChecks').textContent = stats.total;
            document.getElementById('relevantCount').textContent = stats.relevant;
            document.getElementById('irrelevantCount').textContent = stats.irrelevant;
        }
        
        // 回车键支持
        document.getElementById('taskInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') setTask();
        });
        
        document.getElementById('websiteInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') checkWebsite();
        });
    </script>
</body>
</html>
"""
 

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/set_task', methods=['POST'])
def set_task():
    """设置任务API"""
    data = request.json
    task = data.get('task', '')
    monitor.set_task(task)
    return jsonify({"success": True, "task": task})


@app.route('/check_website', methods=['POST'])
def check_website():
    """检查网站API"""
    data = request.json
    website = data.get('website', '')
    
    result = monitor.check_website(website)
    
    return jsonify({
        "is_relevant": result['is_relevant'],
        "reason": result['reason'],
        "confidence": result['confidence']
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("任务专注度监控 Web 服务")
    print("="*70)
    print("\n启动服务器...")
    print("请在浏览器中访问: http://localhost:5000")
    print("\n按 Ctrl+C 停止服务器\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
