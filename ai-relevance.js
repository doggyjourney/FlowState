/**
 * AI-Powered App Relevance Checker using Groq API
 * Based on the FlowState repository's task_focus_monitor.py
 */

const Groq = require('groq-sdk');

class AIRelevanceChecker {
  constructor(apiKey) {
    this.apiKey = apiKey || process.env.GROQ_API_KEY;
    this.client = null;
    this.currentTask = null;
    this.checkHistory = [];
    
    if (this.apiKey) {
      try {
        this.client = new Groq({ apiKey: this.apiKey });
        console.log('[AI] Groq client initialized');
      } catch (error) {
        console.error('[AI] Failed to initialize Groq client:', error);
      }
    } else {
      console.warn('[AI] No Groq API key provided. AI features disabled.');
    }
  }

  setTask(taskDescription) {
    this.currentTask = taskDescription;
    this.checkHistory = [];
    console.log(`[AI] Task set: ${taskDescription}`);
  }

  async checkAppRelevance(appName, windowTitle = '') {
    if (!this.client) {
      return {
        isRelevant: null,
        confidence: 'none',
        reason: 'AI features disabled (no API key)',
        action: 'manual'
      };
    }

    if (!this.currentTask) {
      return {
        isRelevant: null,
        confidence: 'none',
        reason: 'No task set',
        action: 'manual'
      };
    }

    const appInfo = `App: ${appName}${windowTitle ? `\nWindow Title: ${windowTitle}` : ''}`;

    const prompt = `I am working on this task: ${this.currentTask}

I just switched to this application:
${appInfo}

Please determine if this application is relevant to my task.

Criteria:
1. If the app directly helps complete the task, it's "relevant"
2. If the app is for entertainment, social media, shopping, or unrelated to the task, it's "irrelevant"
3. For tools like browsers, editors, terminals, judge based on the task context

Respond in this exact format:
Judgment: relevant / irrelevant
Confidence: high / medium / low
Reason: [brief explanation]

Only provide the above content, no additional text.`;

    try {
      const chatCompletion = await this.client.chat.completions.create({
        messages: [
          {
            role: 'system',
            content: 'You are a professional focus assistant that helps users determine if an application is relevant to their current task.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        model: 'llama-3.3-70b-versatile',
        temperature: 0.2,
        max_tokens: 512
      });

      const responseContent = chatCompletion.choices[0].message.content;
      const result = this._parseResponse(responseContent, appName);

      // Record history
      this.checkHistory.push({
        timestamp: Date.now(),
        appName,
        windowTitle,
        task: this.currentTask,
        result
      });

      console.log(`[AI] ${appName}: ${result.isRelevant ? 'Relevant' : 'Irrelevant'} (${result.confidence})`);

      return result;

    } catch (error) {
      console.error('[AI] API call failed:', error);
      return {
        isRelevant: null,
        confidence: 'none',
        reason: `API error: ${error.message}`,
        action: 'manual'
      };
    }
  }

  _parseResponse(responseContent, appName) {
    // Parse relevance
    const isRelevant = responseContent.toLowerCase().includes('relevant') && 
                      !responseContent.toLowerCase().split('\n')[0].includes('irrelevant');

    // Parse confidence
    let confidence = 'medium';
    if (responseContent.toLowerCase().includes('high')) {
      confidence = 'high';
    } else if (responseContent.toLowerCase().includes('low')) {
      confidence = 'low';
    }

    // Extract reason
    let reason = responseContent;
    const lines = responseContent.split('\n');
    for (const line of lines) {
      if (line.toLowerCase().includes('reason')) {
        reason = line.replace(/reason:/i, '').trim();
        break;
      }
    }

    return {
      isRelevant,
      confidence,
      reason,
      action: isRelevant ? 'allow' : 'block',
      rawResponse: responseContent
    };
  }

  getHistory() {
    return this.checkHistory;
  }

  getStatistics() {
    if (this.checkHistory.length === 0) {
      return null;
    }

    const total = this.checkHistory.length;
    const relevant = this.checkHistory.filter(h => h.result.isRelevant).length;
    const irrelevant = total - relevant;

    return {
      total,
      relevant,
      irrelevant,
      relevanceRate: (relevant / total) * 100
    };
  }

  clearHistory() {
    this.checkHistory = [];
  }

  isEnabled() {
    return this.client !== null;
  }
}

module.exports = AIRelevanceChecker;

