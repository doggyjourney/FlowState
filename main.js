const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const AIRelevanceChecker = require('./ai-relevance');

let mainWindow;
let dataPath;
let monitoringInterval = null;
let currentSession = null;
let scoreHistory = []; // Track score changes
let aiChecker = null; // AI relevance checker
let lastScore = 60; // Last session's final score

// Data storage path
function getDataPath() {
  const userDataPath = app.getPath('userData');
  return path.join(userDataPath, 'data.json');
}

// Initialize data
function initData() {
  dataPath = getDataPath();
  
  // Always start with clean data (removes any preset records)
  const initialData = {
    sessions: [],
    activities: [],
    categories: [],
    taskApps: [],
    firstRun: false
  };
  
  // Only overwrite if first run or file doesn't exist
  if (!fs.existsSync(dataPath)) {
    fs.writeFileSync(dataPath, JSON.stringify(initialData, null, 2));
    console.log('[Data] First run - initialized with clean data');
  } else {
    // Check if it's first run
    try {
      const existingData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      if (existingData.firstRun === undefined) {
        // Old data format, clear it
        fs.writeFileSync(dataPath, JSON.stringify(initialData, null, 2));
        console.log('[Data] Cleared preset data on first run');
      }
    } catch (error) {
      fs.writeFileSync(dataPath, JSON.stringify(initialData, null, 2));
    }
  }
  
  console.log('[Data] Initialized at:', dataPath);
}

// Read data
function readData() {
  try {
    const data = fs.readFileSync(dataPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('[Data] Read error:', error);
    return { sessions: [], activities: [], categories: [], taskApps: [] };
  }
}

// Write data
function writeData(data) {
  try {
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
    return true;
  } catch (error) {
    console.error('[Data] Write error:', error);
    return false;
  }
}

// Get foreground app - macOS
function getForegroundAppMacOS() {
  return new Promise((resolve, reject) => {
    const script = `
      tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        set frontWindow to ""
        try
          set frontWindow to name of front window of application process frontApp
        end try
        return frontApp & "|" & frontWindow
      end tell
    `;

    exec(`osascript -e '${script}'`, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      const [appName, windowTitle] = stdout.trim().split('|');
      resolve({ appName: appName.trim(), windowTitle: windowTitle?.trim() || '' });
    });
  });
}

// Get foreground app - Windows
function getForegroundAppWindows() {
  return new Promise((resolve, reject) => {
    const script = `
      Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        using System.Text;
        
        public class WindowInfo {
          [DllImport("user32.dll")]
          public static extern IntPtr GetForegroundWindow();
          
          [DllImport("user32.dll")]
          public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
          
          [DllImport("user32.dll")]
          public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
        }
      "@
      
      $hWnd = [WindowInfo]::GetForegroundWindow()
      $sb = New-Object System.Text.StringBuilder 256
      [WindowInfo]::GetWindowText($hWnd, $sb, 256) | Out-Null
      
      $processId = 0
      [WindowInfo]::GetWindowThreadProcessId($hWnd, [ref]$processId) | Out-Null
      
      try {
        $process = Get-Process -Id $processId -ErrorAction Stop
        Write-Output "$($process.Name)|$($sb.ToString())"
      } catch {
        Write-Output "Unknown|$($sb.ToString())"
      }
    `;

    exec(`powershell -Command "${script.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      const [appName, windowTitle] = stdout.trim().split('|');
      resolve({ appName: appName?.trim() || 'Unknown', windowTitle: windowTitle?.trim() || '' });
    });
  });
}

// Get foreground app
async function getForegroundApp() {
  try {
    if (process.platform === 'darwin') {
      return await getForegroundAppMacOS();
    } else if (process.platform === 'win32') {
      return await getForegroundAppWindows();
    } else {
      throw new Error('Unsupported platform');
    }
  } catch (error) {
    console.error('[Monitor] Error getting foreground app:', error);
    return null;
  }
}

// Close app - macOS
function closeAppMacOS(appName) {
  return new Promise((resolve) => {
    exec(`osascript -e 'tell application "${appName}" to quit'`, (error) => {
      resolve(!error);
    });
  });
}

// Close app - Windows
function closeAppWindows(appName) {
  return new Promise((resolve) => {
    exec(`taskkill /IM "${appName}.exe" /F`, (error) => {
      resolve(!error);
    });
  });
}

// Close app
async function closeApp(appName) {
  if (process.platform === 'darwin') {
    return await closeAppMacOS(appName);
  } else if (process.platform === 'win32') {
    return await closeAppWindows(appName);
  }
  return false;
}

// Create main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadFile('index.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  initData();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers
ipcMain.handle('start-session', async (event, taskDescription) => {
  const sessionId = `session_${Date.now()}`;
  const startTime = Date.now();

  const data = readData();
  data.sessions.push({
    id: sessionId,
    taskDescription,
    startTime,
    endTime: null,
    finalScore: null,
    distractionCount: 0,
    scoreHistory: [] // Store score changes
  });
  writeData(data);

  currentSession = { id: sessionId, startTime, score: 60, distractionCount: 0 };
  scoreHistory = [{ time: 0, score: 60 }]; // Initialize score history
  
  // Initialize AI checker with task
  if (!aiChecker) {
    aiChecker = new AIRelevanceChecker(process.env.GROQ_API_KEY);
  }
  if (aiChecker.isEnabled()) {
    aiChecker.setTask(taskDescription);
    console.log('[AI] Task set for AI relevance checking');
  }
  
  startMonitoring(sessionId);

  return { sessionId, startTime };
});

ipcMain.handle('end-session', async (event, { sessionId, finalScore, distractionCount }) => {
  const endTime = Date.now();

  const data = readData();
  const session = data.sessions.find(s => s.id === sessionId);
  if (session) {
    session.endTime = endTime;
    session.finalScore = finalScore;
    session.distractionCount = distractionCount;
    session.scoreHistory = scoreHistory; // Save score history
    writeData(data);
  }

  stopMonitoring();
  lastScore = finalScore; // Save for display when not in session
  currentSession = null;
  scoreHistory = [];

  return { success: true };
});

ipcMain.handle('get-sessions', async () => {
  const data = readData();
  return data.sessions.sort((a, b) => b.startTime - a.startTime);
});

ipcMain.handle('get-last-score', async () => {
  return { lastScore };
});

ipcMain.handle('delete-session', async (event, sessionId) => {
  const data = readData();
  data.sessions = data.sessions.filter(s => s.id !== sessionId);
  // Also delete related activities
  data.activities = data.activities.filter(a => a.sessionId !== sessionId);
  writeData(data);
  return { success: true };
});

ipcMain.handle('get-score-history', async () => {
  return scoreHistory;
});

ipcMain.handle('get-categories', async () => {
  const data = readData();
  return data.categories;
});

ipcMain.handle('set-category', async (event, { appName, category, isBlocked }) => {
  const data = readData();
  const existingIndex = data.categories.findIndex(c => c.appName === appName);
  
  const categoryData = { appName, category, isBlocked };
  
  if (existingIndex >= 0) {
    data.categories[existingIndex] = categoryData;
  } else {
    data.categories.push(categoryData);
  }
  
  writeData(data);
  return { success: true };
});

ipcMain.handle('delete-category', async (event, appName) => {
  const data = readData();
  data.categories = data.categories.filter(c => c.appName !== appName);
  writeData(data);
  return { success: true };
});

ipcMain.handle('get-task-apps', async (event, taskName) => {
  const data = readData();
  if (!taskName) return data.taskApps;
  return data.taskApps.filter(t => t.taskName === taskName);
});

ipcMain.handle('save-task-app', async (event, { taskName, appName, appPath, url }) => {
  const data = readData();
  
  // Avoid duplicates
  const exists = data.taskApps.some(t => 
    t.taskName === taskName && 
    ((t.appName && t.appName === appName) || (t.url && t.url === url))
  );
  
  if (!exists) {
    data.taskApps.push({ 
      id: `task_${Date.now()}`,
      taskName, 
      appName, 
      appPath, 
      url 
    });
    writeData(data);
  }
  
  return { success: true };
});

ipcMain.handle('delete-task-app', async (event, id) => {
  const data = readData();
  data.taskApps = data.taskApps.filter(t => t.id !== id);
  writeData(data);
  return { success: true };
});

ipcMain.handle('launch-task-apps', async (event, taskName) => {
  const data = readData();
  const apps = data.taskApps.filter(t => t.taskName === taskName);

  let launched = 0;

  for (const app of apps) {
    try {
      if (app.url) {
        // Open URL
        await shell.openExternal(app.url);
        launched++;
      } else if (app.appName) {
        // Launch application
        if (process.platform === 'darwin') {
          // macOS: use open command
          await new Promise((resolve) => {
            exec(`open -a "${app.appName}"`, (error) => {
              if (error) {
                console.error(`Failed to launch ${app.appName}:`, error);
              }
              resolve();
            });
          });
        } else if (process.platform === 'win32') {
          // Windows: use start command
          await new Promise((resolve) => {
            exec(`start "" "${app.appName}"`, (error) => {
              if (error) {
                console.error(`Failed to launch ${app.appName}:`, error);
              }
              resolve();
            });
          });
        }
        launched++;
      }
    } catch (error) {
      console.error('Failed to launch app:', error);
    }
  }

  return { success: true, count: launched };
});

ipcMain.handle('open-url', async (event, url) => {
  shell.openExternal(url);
  return { success: true };
});

// Monitoring logic
function startMonitoring(sessionId) {
  if (monitoringInterval) {
    clearInterval(monitoringInterval);
  }

  let lastAppName = null;
  let elapsedSeconds = 0;

  monitoringInterval = setInterval(async () => {
    elapsedSeconds += 2;

    try {
      const appInfo = await getForegroundApp();

      if (!appInfo || appInfo.appName === 'FlowState' || appInfo.appName === 'Electron') {
        return;
      }

      if (appInfo.appName !== lastAppName) {
        lastAppName = appInfo.appName;

        const data = readData();
        const category = data.categories.find(c => c.appName === appInfo.appName);
        
        let isDistraction = category?.category === 'distraction';
        let isBlocked = category?.isBlocked === true;
        let aiResult = null;

        // Use AI to determine relevance if no manual category exists
        if (!category && aiChecker && aiChecker.isEnabled() && currentSession) {
          aiResult = await aiChecker.checkAppRelevance(appInfo.appName, appInfo.windowTitle);
          if (aiResult.isRelevant !== null) {
            isDistraction = !aiResult.isRelevant;
            console.log(`[AI] ${appInfo.appName}: ${aiResult.reason}`);
          }
        }

        // Record activity
        data.activities.push({
          sessionId,
          appName: appInfo.appName,
          windowTitle: appInfo.windowTitle,
          timestamp: Date.now(),
          isDistraction,
          aiClassified: aiResult !== null,
          aiReason: aiResult?.reason || null
        });
        writeData(data);

        // Send to renderer
        if (mainWindow) {
          mainWindow.webContents.send('activity-detected', {
            appName: appInfo.appName,
            windowTitle: appInfo.windowTitle,
            isDistraction,
            timestamp: Date.now(),
            aiClassified: aiResult !== null,
            aiReason: aiResult?.reason || null
          });
        }

        // Handle distractions with different penalties
        if (isDistraction) {
          if (category && isBlocked) {
            // Manual blacklist: Force close and deduct 10 points
            console.log('[Monitor] Blacklist app detected:', appInfo.appName);
            currentSession.score = Math.max(currentSession.score - 10, 0);
            currentSession.distractionCount++;
            
            await closeApp(appInfo.appName);

            if (mainWindow) {
              mainWindow.webContents.send('app-blocked', {
                appName: appInfo.appName,
                penalty: 10,
                type: 'blacklist'
              });
            }
          } else if (aiResult) {
            // AI detected: Show warning and deduct 5 points
            console.log('[Monitor] AI detected distraction:', appInfo.appName);
            currentSession.score = Math.max(currentSession.score - 5, 0);
            currentSession.distractionCount++;

            if (mainWindow) {
              mainWindow.webContents.send('ai-warning', {
                appName: appInfo.appName,
                reason: aiResult.reason,
                penalty: 5
              });
            }
          }
        }
      }

      // Update score history every 2 seconds (for real-time chart)
      if (currentSession) {
        scoreHistory.push({
          time: elapsedSeconds,
          score: currentSession.score
        });

        // Keep only last 30 data points (60 seconds)
        if (scoreHistory.length > 30) {
          scoreHistory.shift();
        }

        // Send score update
        if (mainWindow) {
          mainWindow.webContents.send('score-updated', {
            score: currentSession.score,
            time: elapsedSeconds,
            scoreHistory: scoreHistory
          });
        }
      }
    } catch (error) {
      console.error('[Monitor] Error:', error);
    }
  }, 2000);

  console.log('[Monitor] Started for session:', sessionId);
}

function stopMonitoring() {
  if (monitoringInterval) {
    clearInterval(monitoringInterval);
    monitoringInterval = null;
    console.log('[Monitor] Stopped');
  }
}

// Update current session score (called from renderer)
ipcMain.handle('update-session-score', async (event, { score, distractionCount }) => {
  if (currentSession) {
    currentSession.score = score;
    currentSession.distractionCount = distractionCount;
  }
  return { success: true };
});

