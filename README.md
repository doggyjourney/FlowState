Got it. Time is short. Here is your full, updated README with those sections integrated. Just copy and paste this.

-----

# FlowState v4.0 - AI-Powered Focus Detector

## Introduction

FlowState is your AI accountability partner for deep work. It intelligently detects and penalizes distracting context-switching, keeping you locked in the zone.

At its core, FlowState leverages the **blazing-fast Groq API** to analyze browsing activity in real-time. It's not just another website blocker; it's an intelligent system that understands your task and provides immediate feedback, ensuring your focus remains unbroken. This final version (4.0) introduces a nuanced penalty system and live data visualization.

## Why Groq? (Groq Track)

For a focus tool to be effective, its interventions must be **instantaneous**. A 5-second delay in detecting a distraction is too late—the user's focus is already broken.

This is where Groq is the game-changer:

  * **Real-Time Relevance Check:** We use the Groq API (running a model like Llama 3 8B) to analyze website content in real-time. When a user navigates to a new page, FlowState sends the content to Groq and gets a relevance decision in **milliseconds**.
  * **Low-Latency User Experience:** This incredible speed, powered by Groq's LPUs, means our AI warning appears *immediately*, acting as a gentle, real-time nudge rather than an annoying, delayed notification.
  * **Feasibility:** Without Groq's performance, the "AI-Based Detection" feature would feel sluggish and ineffective, defeating the purpose of the application. Groq makes real-time AI accountability possible.

## What's New in v4.0

### Differential Penalty System

FlowState now employs a two-tiered penalty system to offer more flexible focus enforcement:

  * **AI-Based Detection:** When the system's AI, powered by Groq, detects that a user has navigated to a website irrelevant to their current task, it issues a warning and deducts a minor penalty of 5 points. This serves as a gentle nudge to maintain focus.
  * **Manual Blacklist:** For applications and websites manually designated as distractions, FlowState will forcefully close the application and apply a more significant 10-point penalty, ensuring that high-priority distractions are effectively managed.

### Real-Time Scrolling Chart

To provide immediate feedback on focus levels, version 4.0 includes a dynamic scrolling chart with the following features:

  * **Live Updates:** The chart refreshes every two seconds to provide a real-time representation of the user's focus score.
  * **60-Second Window:** It displays the last 60 seconds of focus data, offering a continuous and current overview of performance.
  * **Automatic Scrolling:** The chart automatically scrolls to the left, ensuring the latest data is always in view.
  * **Clear Axes:** The x-axis is clearly labeled in seconds for easy interpretation of the timeline.

### Clean First Run

To ensure a consistent and clean starting point, FlowState now automatically removes all preset data on the first run of a new session, allowing for a fresh start each time.

### Improved Score Display

The user interface has been updated to provide clearer status information:

  * When a focus session is not active, the score from the last session is displayed for review.
  * Status descriptions are now more explicit, ensuring the user always understands their current state within the application.

### Bug Fixes

All known bugs from previous versions have been addressed, including:

  * Proper functionality of task deletion.
  * Correct and smooth scrolling of the real-time chart.
  * Accurate and timely updates to the score display.

## Tech Stack & Architecture

FlowState is built with:

  * **AI Inference:** **Groq API** (running Llama 3 8B) for real-time website relevance analysis.
  * **Frontend:** React (for the dashboard and chart).
  * **Core Logic:** Node.js (for monitoring active applications and browsing).

### How it Works (AI Detection)

1.  User starts a focus session with a task (e.g., "Writing my hackathon README").
2.  User navigates to a new website (e.g., reddit.com).
3.  The app sends the website's content/URL to the Groq API with a prompt like: `"Is this website content relevant to the task: 'Writing my hackathon README'? Respond with JSON: {relevant: true/false}"`.
4.  Groq returns a JSON response in milliseconds.
5.  If `relevant: false`, the app triggers the -5 point penalty and warning popup.

## Installation

To install and run FlowState, follow these steps:

```bash
npm install
export GROQ_API_KEY="your_groq_api_key"  # Required for AI features
npm start
```

## Penalty System Overview

| Detection Method | Action Taken | Point Penalty |
| :--- | :--- | :--- |
| AI (Irrelevant Website) | Warning Popup | -5 |
| Manual Blacklist | Force Close Application | -10 |

## Quick Guide

### Setting Up the Blacklist

1.  Navigate to **App Categories**.
2.  Enter the name of the application you wish to blacklist.
3.  Assign the category "Distraction".
4.  Enable the "Auto-close" option.
5.  Save your settings.

### Utilizing the AI Detection

1.  Ensure you have set your `GROQ_API_KEY` in your environment variables.
2.  Start a new focus session with a clearly defined task.
3.  The AI will automatically monitor your browsing activity for relevance to your stated task.

### Associating Tasks with Applications

1.  Go to **Task Management** and add a new task.
2.  You can associate specific applications with a task.
3.  When you begin the session for that task, the associated applications will be launched automatically.

## Chart Features

  * **Update Frequency:** 2 seconds
  * **Display Window:** 30 data points (representing the last 60 seconds)
  * **Behavior:** Auto-scrolling to the left
  * **Purpose:** Real-time visualization of focus score

## Troubleshooting

  * **AI Not Functioning:** Verify that your `GROQ_API_KEY` is correctly set in your environment variables.
  * **Applications Not Closing:** Double-check that the application name in your blacklist exactly matches the running application's name.
  * **Chart Not Scrolling:** Please allow at least 60 seconds of a focus session to pass for the scrolling feature to become apparent.

## Team

  * [doggyjourney](https://github.com/doggyjourney)
  * [Xsasdes](https://github.com/Xsasdes)
  * [XYavecasdf](https://github.com/XYavecasdf)
  * The list of contributors is sorted alphabetically by username and does not reflect the magnitude of contribution.

## License

This project is licensed under the MIT License.
