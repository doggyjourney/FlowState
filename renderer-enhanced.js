// FlowState v4 Enhanced Renderer
// Real-time 2-second chart, AI warnings, improved score display

let currentSessionId = null;
let currentScore = 60;
let distractionCount = 0;
let sessionStartTime = null;
let scoreInterval = null;
let activities = [];
let lastDistractionTime = 0;
let scoreHistory = [];
let lastScore = 60; // Score when not in session

// Initialize - load last score
async function initializeApp() {
  try {
    const result = await window.electronAPI.getLastScore();
    lastScore = result.lastScore;
    document.getElementById('currentScore').textContent = lastScore;
    
    // Update description
    const info = document.getElementById('sessionInfo');
    info.textContent = 'Not in session - Score shows last session result';
    info.className = 'alert';
  } catch (error) {
    console.error('Failed to load last score:', error);
  }
  
  loadStats();
  drawRealtimeChart();
}

// Switch tabs
function switchTab(tabName) {
  document.querySelectorAll('.tab').forEach((tab) => tab.classList.remove('active'));
  document.querySelectorAll('.content').forEach((content) => content.classList.remove('active'));

  event.target.classList.add('active');
  document.getElementById(tabName).classList.add('active');

  if (tabName === 'categories') {
    loadCategories();
  } else if (tabName === 'history') {
    loadSessions();
  } else if (tabName === 'tasks') {
    loadAllTaskApps();
  } else if (tabName === 'home') {
    loadStats();
  }
}

// Start focus session
async function startSession() {
  const taskDescription = document.getElementById('taskInput').value.trim();

  if (!taskDescription) {
    alert('Please enter a task description');
    return;
  }

  try {
    const result = await window.electronAPI.startSession(taskDescription);
    currentSessionId = result.sessionId;
    sessionStartTime = result.startTime;
    currentScore = 60;
    distractionCount = 0;
    lastDistractionTime = 0;
    activities = [];
    scoreHistory = [{ time: 0, score: 60 }];

    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('endBtn').style.display = 'block';
    document.getElementById('taskInput').disabled = true;

    const info = document.getElementById('sessionInfo');
    info.style.display = 'block';
    info.className = 'alert success';
    info.textContent = `Focus session started | Session ID: ${currentSessionId.slice(0, 8)}...`;

    document.getElementById('activityList').innerHTML = '<p class="empty-state">Waiting for app activities...</p>';

    // Start score update
    startScoreUpdate();

    // Ask to launch task apps
    const shouldLaunch = confirm(`Launch apps/URLs associated with "${taskDescription}"?`);
    if (shouldLaunch) {
      try {
        const launchResult = await window.electronAPI.launchTaskApps(taskDescription);
        if (launchResult.count > 0) {
          alert(`Launched ${launchResult.count} app(s)/URL(s)`);
        }
      } catch (error) {
        console.error('Failed to launch apps:', error);
      }
    }
  } catch (error) {
    alert('Failed to start session: ' + error.message);
  }
}

// End focus session
async function endSession() {
  if (!currentSessionId) return;

  try {
    await window.electronAPI.endSession({
      sessionId: currentSessionId,
      finalScore: currentScore,
      distractionCount: distractionCount,
    });

    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('endBtn').style.display = 'none';
    document.getElementById('taskInput').disabled = false;
    document.getElementById('taskInput').value = '';

    const info = document.getElementById('sessionInfo');
    info.className = 'alert';
    info.textContent = `Session ended | Final score: ${currentScore} | Distractions: ${distractionCount}`;

    lastScore = currentScore; // Save for display
    currentSessionId = null;
    stopScoreUpdate();

    loadStats();
  } catch (error) {
    alert('Failed to end session: ' + error.message);
  }
}

// Start score update
function startScoreUpdate() {
  if (scoreInterval) clearInterval(scoreInterval);

  let elapsedSeconds = 0;

  scoreInterval = setInterval(() => {
    elapsedSeconds++;

    // Focus score algorithm:
    // +1 every 30 seconds (if not in cooldown)
    // -5 on AI distraction
    // -10 on blacklist distraction
    // 20s cooldown after distraction

    const timeSinceLastDistraction = elapsedSeconds - lastDistractionTime;

    if (timeSinceLastDistraction > 20) {
      const baseIncrease = Math.floor(elapsedSeconds / 30);
      currentScore = Math.min(60 + baseIncrease - (distractionCount * 5), 100);
      currentScore = Math.max(currentScore, 0);
    }

    document.getElementById('currentScore').textContent = currentScore;

    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    const info = document.getElementById('sessionInfo');
    info.textContent = `Focusing... | Duration: ${minutes}m ${seconds}s | Score: ${currentScore} | Distractions: ${distractionCount}`;
  }, 1000);
}

// Stop score update
function stopScoreUpdate() {
  if (scoreInterval) {
    clearInterval(scoreInterval);
    scoreInterval = null;
  }
}

// Draw real-time chart (30 points, 2-second intervals, scrolling)
function drawRealtimeChart() {
  const canvas = document.getElementById('scoreChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = 300 * dpr;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = '300px';
  ctx.scale(dpr, dpr);

  const width = rect.width;
  const height = 300;
  const padding = 60;

  ctx.clearRect(0, 0, width, height);

  // Background gradient
  const bgGradient = ctx.createLinearGradient(0, 0, 0, height);
  bgGradient.addColorStop(0, '#f8f9fa');
  bgGradient.addColorStop(1, '#e9ecef');
  ctx.fillStyle = bgGradient;
  ctx.fillRect(0, 0, width, height);

  if (scoreHistory.length === 0) {
    ctx.fillStyle = '#6c757d';
    ctx.font = '16px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Start a session to see real-time score chart', width / 2, height / 2);
    ctx.fillText('Updates every 2 seconds', width / 2, height / 2 + 25);
    return;
  }

  // Draw grid
  ctx.strokeStyle = '#dee2e6';
  ctx.lineWidth = 1;

  // Horizontal lines (score: 0-100)
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height - padding * 2) * i / 5;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(width - padding, y);
    ctx.stroke();

    ctx.fillStyle = '#495057';
    ctx.font = 'bold 12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(100 - i * 20, padding - 10, y + 4);
  }

  // Vertical lines (time: 30 points = 60 seconds)
  const timeSteps = 6;
  for (let i = 0; i <= timeSteps; i++) {
    const x = padding + (width - padding * 2) * i / timeSteps;
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, height - padding);
    ctx.stroke();

    ctx.fillStyle = '#495057';
    ctx.font = 'bold 12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    const timeLabel = (60 * i / timeSteps).toFixed(0);
    ctx.fillText(timeLabel + 's', x, height - padding + 20);
  }

  // Draw area fill
  const areaGradient = ctx.createLinearGradient(0, padding, 0, height - padding);
  areaGradient.addColorStop(0, 'rgba(76, 175, 80, 0.3)');
  areaGradient.addColorStop(1, 'rgba(76, 175, 80, 0.05)');
  
  ctx.fillStyle = areaGradient;
  ctx.beginPath();
  
  const firstX = padding;
  const firstY = height - padding - (scoreHistory[0].score / 100) * (height - padding * 2);
  ctx.moveTo(firstX, height - padding);
  ctx.lineTo(firstX, firstY);
  
  scoreHistory.forEach((point, index) => {
    const x = padding + (index / 29) * (width - padding * 2);
    const y = height - padding - (point.score / 100) * (height - padding * 2);
    ctx.lineTo(x, y);
  });
  
  const lastX = padding + ((scoreHistory.length - 1) / 29) * (width - padding * 2);
  ctx.lineTo(lastX, height - padding);
  ctx.closePath();
  ctx.fill();

  // Draw line
  const lineGradient = ctx.createLinearGradient(padding, 0, width - padding, 0);
  lineGradient.addColorStop(0, '#4caf50');
  lineGradient.addColorStop(0.5, '#66bb6a');
  lineGradient.addColorStop(1, '#81c784');
  
  ctx.strokeStyle = lineGradient;
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.beginPath();

  scoreHistory.forEach((point, index) => {
    const x = padding + (index / 29) * (width - padding * 2);
    const y = height - padding - (point.score / 100) * (height - padding * 2);

    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });

  ctx.stroke();

  // Draw points
  ctx.shadowColor = 'rgba(76, 175, 80, 0.5)';
  ctx.shadowBlur = 8;
  
  scoreHistory.forEach((point, index) => {
    const x = padding + (index / 29) * (width - padding * 2);
    const y = height - padding - (point.score / 100) * (height - padding * 2);
    
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.fillStyle = '#4caf50';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
    
    if (index === scoreHistory.length - 1) {
      ctx.strokeStyle = '#2e7d32';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.stroke();
    }
  });
  
  ctx.shadowColor = 'transparent';
  ctx.shadowBlur = 0;

  // Axis labels
  ctx.fillStyle = '#212529';
  ctx.font = 'bold 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Time (seconds, last 60s)', width / 2, height - 5);
  
  ctx.save();
  ctx.translate(15, height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('Focus Score', 0, 0);
  ctx.restore();
  
  // Score badge
  if (scoreHistory.length > 0) {
    const lastScoreValue = scoreHistory[scoreHistory.length - 1].score;
    const badgeX = width - padding - 80;
    const badgeY = padding + 20;
    
    ctx.fillStyle = '#4caf50';
    ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.roundRect(badgeX, badgeY - 15, 70, 30, 15);
    ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 16px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${lastScoreValue}`, badgeX + 35, badgeY + 5);
  }
}

// Listen for score updates (every 2 seconds)
window.electronAPI.onScoreUpdated((data) => {
  scoreHistory = data.scoreHistory || [];
  drawRealtimeChart();
});

// Listen for activity detection
window.electronAPI.onActivityDetected((data) => {
  const { appName, windowTitle, isDistraction, timestamp, aiClassified, aiReason } = data;

  activities.unshift({
    appName,
    windowTitle,
    isDistraction,
    timestamp,
    aiClassified,
    aiReason
  });

  if (activities.length > 20) {
    activities = activities.slice(0, 20);
  }

  renderActivities();
});

// Listen for blacklist app blocked
window.electronAPI.onAppBlocked((data) => {
  const { appName, penalty } = data;
  
  const alertDiv = document.createElement('div');
  alertDiv.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #e74c3c;
    color: white;
    padding: 30px 50px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
    z-index: 10000;
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
  `;
  alertDiv.textContent = `🚫 Blacklist app "${appName}" was force-closed! -${penalty} points`;
  document.body.appendChild(alertDiv);
  
  setTimeout(() => {
    alertDiv.remove();
  }, 3000);
});

// Listen for AI warning (not force-closed)
window.electronAPI.onAiWarning((data) => {
  const { appName, reason, penalty } = data;
  
  const alertDiv = document.createElement('div');
  alertDiv.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #ff9800;
    color: white;
    padding: 30px 50px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    z-index: 10000;
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    max-width: 500px;
    text-align: center;
  `;
  alertDiv.innerHTML = `
    <div>⚠️ AI Detected Distraction</div>
    <div style="font-size: 16px; margin-top: 10px;">"${appName}"</div>
    <div style="font-size: 14px; margin-top: 10px; font-weight: normal;">${reason}</div>
    <div style="font-size: 16px; margin-top: 10px;">-${penalty} points</div>
  `;
  document.body.appendChild(alertDiv);
  
  setTimeout(() => {
    alertDiv.remove();
  }, 4000);
});

// Render activities
function renderActivities() {
  const list = document.getElementById('activityList');

  if (activities.length === 0) {
    list.innerHTML = '<p class="empty-state">No activities yet</p>';
    return;
  }

  list.innerHTML = activities
    .map((activity) => {
      const time = new Date(activity.timestamp).toLocaleTimeString();
      const className = activity.isDistraction ? 'activity-item distraction' : 'activity-item';
      const icon = activity.isDistraction ? '⚠️' : '✓';
      const aiIndicator = activity.aiClassified ? '🤖 AI' : '';

      return `
        <div class="${className}">
          <div>
            <strong>${icon} ${activity.appName}</strong> ${aiIndicator}
            <div style="font-size:12px; color:#666;">
              ${activity.windowTitle || 'No title'}
              ${activity.aiReason ? `<br><em style="color:#6c757d;">AI: ${activity.aiReason}</em>` : ''}
            </div>
          </div>
          <div style="font-size:12px; color:#999;">${time}</div>
        </div>
      `;
    })
    .join('');
}

// Polyfill for roundRect
if (typeof CanvasRenderingContext2D.prototype.roundRect === 'undefined') {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, width, height, radius) {
    this.moveTo(x + radius, y);
    this.lineTo(x + width - radius, y);
    this.quadraticCurveTo(x + width, y, x + width, y + radius);
    this.lineTo(x + width, y + height - radius);
    this.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    this.lineTo(x + radius, y + height);
    this.quadraticCurveTo(x, y + height, x, y + height - radius);
    this.lineTo(x, y + radius);
    this.quadraticCurveTo(x, y, x + radius, y);
    this.closePath();
  };
}

// Initialize on load
initializeApp();

console.log('[v4] Real-time chart and AI warnings loaded');

