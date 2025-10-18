const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  startSession: (taskDescription) => ipcRenderer.invoke('start-session', taskDescription),
  endSession: (data) => ipcRenderer.invoke('end-session', data),
  getSessions: () => ipcRenderer.invoke('get-sessions'),
  deleteSession: (sessionId) => ipcRenderer.invoke('delete-session', sessionId),
  getScoreHistory: () => ipcRenderer.invoke('get-score-history'),
  updateSessionScore: (data) => ipcRenderer.invoke('update-session-score', data),
  getLastScore: () => ipcRenderer.invoke('get-last-score'),
  
  getCategories: () => ipcRenderer.invoke('get-categories'),
  setCategory: (data) => ipcRenderer.invoke('set-category', data),
  deleteCategory: (appName) => ipcRenderer.invoke('delete-category', appName),
  
  getTaskApps: (taskName) => ipcRenderer.invoke('get-task-apps', taskName),
  saveTaskApp: (data) => ipcRenderer.invoke('save-task-app', data),
  deleteTaskApp: (id) => ipcRenderer.invoke('delete-task-app', id),
  launchTaskApps: (taskName) => ipcRenderer.invoke('launch-task-apps', taskName),
  
  openUrl: (url) => ipcRenderer.invoke('open-url', url),
  
  onActivityDetected: (callback) => ipcRenderer.on('activity-detected', (event, data) => callback(data)),
  onAppBlocked: (callback) => ipcRenderer.on('app-blocked', (event, data) => callback(data)),
  onAiWarning: (callback) => ipcRenderer.on('ai-warning', (event, data) => callback(data)),
  onScoreUpdated: (callback) => ipcRenderer.on('score-updated', (event, data) => callback(data)),
});

