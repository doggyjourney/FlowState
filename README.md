# FlowState v4.0 - AI-Powered Focus Detector (Final)

## 🚀 What's New in v4.0

### 🎯 Differential Penalty System
- **AI Detection:** Warning popup (NOT force-closed), -5 points
- **Manual Blacklist:** Force close app, -10 points

### 📊 Real-Time Scrolling Chart
- Updates every 2 seconds
- Shows last 60 seconds (30 points)
- Scrolls left automatically
- X-axis in seconds

### 🧹 Clean First Run
- Removes all preset data
- Fresh start every time

### 📈 Improved Score Display
- Shows last session score when not focusing
- Clear status descriptions

### ✅ All Bugs Fixed
- Task deletion works
- Chart scrolls correctly
- Score display accurate

## 🔧 Installation

```bash
npm install
export GROQ_API_KEY="your_key"  # Optional
npm start
```

## 🎯 Penalty System

| Method | Action | Penalty | Popup |
|--------|--------|---------|-------|
| AI | Warning | -5 | Orange |
| Blacklist | Force close | -10 | Red |

## 📖 Quick Guide

**Setup Blacklist:**
1. App Categories → Enter app name
2. Category: "Distraction"
3. Check "Auto-close"
4. Save

**Use AI:**
1. Set GROQ_API_KEY
2. Start session with clear task
3. AI detects automatically

**Task Associations:**
1. Task Management → Add
2. Launch all when starting session

## 📊 Chart Features

- 2-second updates
- 30-point window (60s)
- Auto-scrolling
- Real-time visualization

## 🐛 Troubleshooting

**AI not working?** Check GROQ_API_KEY

**Apps not closing?** Verify exact app name

**Chart not scrolling?** Wait 60+ seconds

## 📄 License

MIT

---

**v4.0 Final** | **Full English** | **Built-in AI** 🚀

