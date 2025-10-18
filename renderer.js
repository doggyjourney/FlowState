let currentSessionId = null;
let currentScore = 60;
let distractionCount = 0;
let sessionStartTime = null;
let scoreInterval = null;
let chartInterval = null;
let activities = [];
let lastDistractionTime = 0;
let scoreHistory = [];

// Switch tabs
function switchTab(tabName) {
  document.querySelectorAll('.tab').forEach((tab) => tab.classList.remove('active'));
  document.querySelectorAll('.content').forEach((content) => content.classList.remove('active'));

  event.target.classList.add('active');
  document.getElementById(tabName).classList.add('active');

  // Load corresponding data
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

    // Start score update and chart refresh
    startScoreUpdate();
    startChartRefresh();

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

    currentSessionId = null;
    stopScoreUpdate();
    stopChartRefresh();

    // Refresh stats
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
    // - Base score: 60
    // - +1 every 30 seconds (if not in cooldown)
    // - Max 100
    // - -30 on distraction, then 20s cooldown

    const timeSinceLastDistraction = elapsedSeconds - lastDistractionTime;

    if (timeSinceLastDistraction > 20) {
      // Not in cooldown, can increase
      const baseIncrease = Math.floor(elapsedSeconds / 30);
      currentScore = Math.min(60 + baseIncrease - (distractionCount * 30), 100);
      currentScore = Math.max(currentScore, 0);
    }

    document.getElementById('currentScore').textContent = currentScore;

    // Update session info
    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    const info = document.getElementById('sessionInfo');
    info.textContent = `Focusing... | Duration: ${minutes}m ${seconds}s | Score: ${currentScore} | Distractions: ${distractionCount}`;

    // Update score history every 10 seconds
    if (elapsedSeconds % 10 === 0) {
      const timeMinutes = elapsedSeconds / 60; // Use decimal minutes for accuracy
      scoreHistory.push({ time: timeMinutes, score: currentScore });

      // Update backend
      window.electronAPI.updateSessionScore({
        score: currentScore,
        distractionCount: distractionCount
      });
    }
  }, 1000);
}

// Stop score update
function stopScoreUpdate() {
  if (scoreInterval) {
    clearInterval(scoreInterval);
    scoreInterval = null;
  }
}

// Start chart refresh (every 10 seconds)
function startChartRefresh() {
  if (chartInterval) clearInterval(chartInterval);
  
  // Draw immediately
  drawScoreChart();
  
  // Then refresh every 10 seconds
  chartInterval = setInterval(() => {
    drawScoreChart();
  }, 10000);
}

// Stop chart refresh
function stopChartRefresh() {
  if (chartInterval) {
    clearInterval(chartInterval);
    chartInterval = null;
  }
}

// Draw score chart
function drawScoreChart() {
  const canvas = document.getElementById('scoreChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Set canvas size
  canvas.width = canvas.offsetWidth;
  canvas.height = 300;

  const width = canvas.width;
  const height = canvas.height;
  const padding = 50;

  // Clear canvas
  ctx.clearRect(0, 0, width, height);

  // Draw background
  ctx.fillStyle = '#f8f9fa';
  ctx.fillRect(0, 0, width, height);

  if (scoreHistory.length === 0) {
    ctx.fillStyle = '#999';
    ctx.font = '16px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Start a session to see score chart', width / 2, height / 2);
    return;
  }

  // Calculate max time (in minutes, with decimals)
  const maxTime = Math.max(...scoreHistory.map(p => p.time), 1);
  const maxTimeRounded = Math.ceil(maxTime);

  // Draw grid
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;

  // Horizontal lines (score)
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height - padding * 2) * i / 5;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(width - padding, y);
    ctx.stroke();

    // Y-axis labels
    ctx.fillStyle = '#666';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(100 - i * 20, padding - 10, y + 4);
  }

  // Vertical lines (time)
  const timeSteps = 6;
  for (let i = 0; i <= timeSteps; i++) {
    const x = padding + (width - padding * 2) * i / timeSteps;
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, height - padding);
    ctx.stroke();

    // X-axis labels (show actual minutes)
    ctx.fillStyle = '#666';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    const timeLabel = (maxTimeRounded * i / timeSteps).toFixed(1);
    ctx.fillText(timeLabel + 'm', x, height - padding + 20);
  }

  // Draw score line
  ctx.strokeStyle = '#4caf50';
  ctx.lineWidth = 3;
  ctx.beginPath();

  scoreHistory.forEach((point, index) => {
    const x = padding + (point.time / maxTime) * (width - padding * 2);
    const y = height - padding - (point.score / 100) * (height - padding * 2);

    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });

  ctx.stroke();

  // Draw points
  ctx.fillStyle = '#4caf50';
  scoreHistory.forEach((point) => {
    const x = padding + (point.time / maxTime) * (width - padding * 2);
    const y = height - padding - (point.score / 100) * (height - padding * 2);
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
  });

  // Draw axis labels
  ctx.fillStyle = '#333';
  ctx.font = '14px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Time (minutes)', width / 2, height - 5);
  
  ctx.save();
  ctx.translate(15, height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('Focus Score', 0, 0);
  ctx.restore();
}

// Listen for activity detection
window.electronAPI.onActivityDetected((data) => {
  const { appName, windowTitle, isDistraction, timestamp } = data;

  // Update activity list
  activities.unshift({
    appName,
    windowTitle,
    isDistraction,
    timestamp,
  });

  // Keep only last 20
  if (activities.length > 20) {
    activities = activities.slice(0, 20);
  }

  renderActivities();

  // Deduct score if distraction
  if (isDistraction) {
    distractionCount++;
    const elapsedSeconds = Math.floor((Date.now() - sessionStartTime) / 1000);
    lastDistractionTime = elapsedSeconds;
    currentScore = Math.max(currentScore - 30, 0);
    document.getElementById('currentScore').textContent = currentScore;
  }
});

// Listen for app blocked
window.electronAPI.onAppBlocked((data) => {
  const { appName } = data;
  
  // Create prominent alert
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
  alertDiv.textContent = `⚠️ Distraction app "${appName}" was auto-closed!`;
  document.body.appendChild(alertDiv);
  
  setTimeout(() => {
    alertDiv.remove();
  }, 3000);
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

      return `
        <div class="${className}">
          <div>
            <strong>${icon} ${activity.appName}</strong>
            <div style="font-size:12px; color:#666;">${activity.windowTitle || 'No title'}</div>
          </div>
          <div style="font-size:12px; color:#999;">${time}</div>
        </div>
      `;
    })
    .join('');
}

// Add app category
async function addCategory() {
  const appName = document.getElementById('appNameInput').value.trim();
  const category = document.getElementById('categorySelect').value;
  const isBlocked = document.getElementById('blockCheckbox').checked;

  if (!appName) {
    alert('Please enter an app name');
    return;
  }

  try {
    await window.electronAPI.setCategory({ appName, category, isBlocked });
    document.getElementById('appNameInput').value = '';
    document.getElementById('blockCheckbox').checked = false;
    alert(`App "${appName}" added to category`);
    loadCategories();
  } catch (error) {
    alert('Failed to add category: ' + error.message);
  }
}

// Load app categories
async function loadCategories() {
  try {
    const categories = await window.electronAPI.getCategories();
    const list = document.getElementById('categoryList');

    if (categories.length === 0) {
      list.innerHTML = '<p class="empty-state">No apps categorized yet</p>';
      return;
    }

    list.innerHTML = categories
      .map((cat) => {
        const badgeClass = `badge ${cat.category}`;
        const categoryLabel =
          cat.category === 'work' ? 'Work' : cat.category === 'distraction' ? 'Distraction' : 'Break';
        const blockText = cat.isBlocked ? '🚫 Auto-close' : '';

        return `
          <div class="category-item">
            <div>
              <strong>${cat.appName}</strong>
              <div style="font-size:12px; color:#666;">${blockText}</div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <span class="${badgeClass}">${categoryLabel}</span>
              <button class="danger" style="padding:6px 12px; font-size:12px;" onclick="deleteCategory('${cat.appName}')">Delete</button>
            </div>
          </div>
        `;
      })
      .join('');
  } catch (error) {
    console.error('Failed to load categories:', error);
  }
}

// Delete app category
async function deleteCategory(appName) {
  if (!confirm(`Delete category for ${appName}?`)) return;

  try {
    await window.electronAPI.deleteCategory(appName);
    loadCategories();
  } catch (error) {
    alert('Failed to delete: ' + error.message);
  }
}

// Save task app association
async function saveTaskApp() {
  const taskName = document.getElementById('taskNameInput').value.trim();
  const appName = document.getElementById('taskAppInput').value.trim();
  const url = document.getElementById('taskUrlInput').value.trim();

  if (!taskName) {
    alert('Please enter a task name');
    return;
  }

  if (!appName && !url) {
    alert('Please enter at least an app name or URL');
    return;
  }

  try {
    await window.electronAPI.saveTaskApp({
      taskName,
      appName: appName || null,
      appPath: null,
      url: url || null,
    });

    document.getElementById('taskAppInput').value = '';
    document.getElementById('taskUrlInput').value = '';

    alert('Association saved');
    loadAllTaskApps();
  } catch (error) {
    alert('Failed to save: ' + error.message);
  }
}

// Launch task apps
async function launchTaskApps() {
  const taskName = document.getElementById('launchTaskInput').value.trim();

  if (!taskName) {
    alert('Please enter a task name');
    return;
  }

  try {
    const result = await window.electronAPI.launchTaskApps(taskName);
    if (result.count > 0) {
      alert(`Launched ${result.count} app(s)/URL(s)`);
    } else {
      alert(`No apps/URLs associated with "${taskName}"`);
    }
  } catch (error) {
    alert('Failed to launch: ' + error.message);
  }
}

// Load all task apps (with filter support)
async function loadAllTaskApps() {
  try {
    const taskName = document.getElementById('taskNameInput').value.trim();
    const allApps = await window.electronAPI.getTaskApps(null);
    const list = document.getElementById('taskAppList');
    
    if (allApps.length === 0) {
      list.innerHTML = '<p class="empty-state">No associations yet</p>';
      return;
    }

    // Filter by task name if provided
    const filteredApps = taskName 
      ? allApps.filter(app => app.taskName.toLowerCase().includes(taskName.toLowerCase()))
      : allApps;

    if (filteredApps.length === 0) {
      list.innerHTML = '<p class="empty-state">No associations match this filter</p>';
      return;
    }

    // Group by task name
    const grouped = {};
    filteredApps.forEach(app => {
      if (!grouped[app.taskName]) {
        grouped[app.taskName] = [];
      }
      grouped[app.taskName].push(app);
    });

    list.innerHTML = Object.entries(grouped)
      .map(([task, apps]) => {
        const appsList = apps.map(app => {
          const display = app.url ? `🌐 ${app.url}` : `📱 ${app.appName}`;
          return `
            <div class="task-app-item">
              <div>${display}</div>
              <button class="danger" style="padding:4px 8px; font-size:12px;" onclick="deleteTaskApp('${app.id}')">Delete</button>
            </div>
          `;
        }).join('');

        return `
          <div style="margin-bottom:16px;">
            <h3>${task}</h3>
            ${appsList}
          </div>
        `;
      })
      .join('');
  } catch (error) {
    console.error('Failed to load task apps:', error);
  }
}

// Delete task app (FIXED)
async function deleteTaskApp(id) {
  if (!confirm('Delete this association?')) return;

  try {
    await window.electronAPI.deleteTaskApp(id);
    loadAllTaskApps(); // Refresh the list
  } catch (error) {
    alert('Failed to delete: ' + error.message);
  }
}

// Load session history
async function loadSessions() {
  try {
    const sessions = await window.electronAPI.getSessions();
    const list = document.getElementById('sessionList');

    if (sessions.length === 0) {
      list.innerHTML = '<p class="empty-state">No sessions yet</p>';
      return;
    }

    list.innerHTML = sessions
      .map((session) => {
        const startTime = new Date(session.startTime).toLocaleString();
        const duration = session.endTime
          ? Math.round((session.endTime - session.startTime) / 60000)
          : 'In progress';

        return `
          <div class="session-item">
            <div class="session-header">
              <div>
                <strong>${session.taskDescription || 'Untitled'}</strong>
                <div style="font-size:12px; color:#666;">${startTime} | Duration: ${duration} min</div>
              </div>
              <div style="display:flex; gap:12px; align-items:center;">
                <div class="session-score">${session.finalScore !== null ? session.finalScore : '-'}</div>
                <button class="danger" style="padding:6px 12px; font-size:12px;" onclick="deleteSession('${session.id}')">Delete</button>
              </div>
            </div>
            <div style="font-size:13px; color:#666;">
              Distractions: ${session.distractionCount || 0}
            </div>
          </div>
        `;
      })
      .join('');
  } catch (error) {
    console.error('Failed to load sessions:', error);
  }
}

// Delete session
async function deleteSession(sessionId) {
  if (!confirm('Delete this session? This cannot be undone.')) return;

  try {
    await window.electronAPI.deleteSession(sessionId);
    loadSessions();
    loadStats();
  } catch (error) {
    alert('Failed to delete: ' + error.message);
  }
}

// Load stats
async function loadStats() {
  try {
    const sessions = await window.electronAPI.getSessions();

    // Calculate last 7 days stats
    const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const recentSessions = sessions.filter((s) => s.startTime > weekAgo && s.endTime);

    const totalSessions = recentSessions.length;
    const avgScore =
      totalSessions > 0
        ? Math.round(recentSessions.reduce((sum, s) => sum + (s.finalScore || 0), 0) / totalSessions)
        : 0;
    const totalDistractions = recentSessions.reduce((sum, s) => sum + (s.distractionCount || 0), 0);

    document.getElementById('totalSessions').textContent = totalSessions;
    document.getElementById('avgScore').textContent = avgScore;
    document.getElementById('totalDistractions').textContent = totalDistractions;
  } catch (error) {
    console.error('Failed to load stats:', error);
  }
}

// Listen for task name input changes (for filtering)
document.addEventListener('DOMContentLoaded', () => {
  const taskNameInput = document.getElementById('taskNameInput');
  if (taskNameInput) {
    taskNameInput.addEventListener('input', loadAllTaskApps);
  }
});

// Initialize
loadStats();
drawScoreChart();

