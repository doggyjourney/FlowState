import { DistractionDetector, DistractionAnalysis, FocusEvent, Resource, Task } from './types.js';
import { ConfigManager } from './config.js';

export class GroqDistractionDetector implements DistractionDetector {
  private config: ConfigManager;

  constructor(config: ConfigManager) {
    this.config = config;
  }

  async analyzeFocusEvent(event: FocusEvent, task: Task): Promise<DistractionAnalysis> {
    const cfg = await this.config.load();
    const apiKey = cfg.apiConfig.groq.apiKey;
    
    if (!apiKey) {
      return {
        isDistracted: false,
        confidence: 0,
        reason: 'Groq API key not configured',
        suggestion: 'allow',
      };
    }

    try {
      // 构建分析提示
      const prompt = this.buildAnalysisPrompt(event, task);
      
      // 调用Groq API
      const response = await this.callGroqAPI(prompt, apiKey, cfg.apiConfig.groq);
      
      // 解析响应
      return this.parseGroqResponse(response);
    } catch (error: any) {
      console.warn(`Groq API error: ${error.message}`);
      return {
        isDistracted: false,
        confidence: 0,
        reason: `API error: ${error.message}`,
        suggestion: 'allow',
      };
    }
  }

  async analyzeResource(resource: Resource, task: Task): Promise<DistractionAnalysis> {
    const cfg = await this.config.load();
    const apiKey = cfg.apiConfig.groq.apiKey;
    
    if (!apiKey) {
      return {
        isDistracted: false,
        confidence: 0,
        reason: 'Groq API key not configured',
        suggestion: 'allow',
      };
    }

    try {
      const prompt = this.buildResourceAnalysisPrompt(resource, task);
      const response = await this.callGroqAPI(prompt, apiKey, cfg.apiConfig.groq);
      return this.parseGroqResponse(response);
    } catch (error: any) {
      console.warn(`Groq API error: ${error.message}`);
      return {
        isDistracted: false,
        confidence: 0,
        reason: `API error: ${error.message}`,
        suggestion: 'allow',
      };
    }
  }

  private buildAnalysisPrompt(event: FocusEvent, task: Task): string {
    return `You are a productivity assistant analyzing whether a user is distracted from their current task.

Current Task: "${task.name}"
Task Resources: ${JSON.stringify(task.resources.map(r => ({ type: r.kind, id: r.id, title: r.title })))}

Current Activity:
- App: ${event.appId}
- URL: ${event.url || 'N/A'}
- Title: ${event.title || 'N/A'}

Analyze if the user is distracted from their task. Consider:
1. Is the current app/website related to the task?
2. Is it a common distraction (social media, news, entertainment)?
3. Does it align with the task's purpose?

Respond with a JSON object:
{
  "isDistracted": boolean,
  "confidence": number (0-1),
  "reason": "brief explanation",
  "suggestion": "close|warn|allow",
  "alternativeResources": [{"kind": "app|url", "id": "string", "title": "string"}] (optional)
}`;
  }

  private buildResourceAnalysisPrompt(resource: Resource, task: Task): string {
    return `You are a productivity assistant analyzing whether a resource is relevant to a task.

Current Task: "${task.name}"
Task Resources: ${JSON.stringify(task.resources.map(r => ({ type: r.kind, id: r.id, title: r.title })))}

Resource to analyze:
- Type: ${resource.kind}
- ID: ${resource.id}
- Title: ${resource.title || 'N/A'}

Determine if this resource is relevant to the task or if it's a distraction.

Respond with a JSON object:
{
  "isDistracted": boolean,
  "confidence": number (0-1),
  "reason": "brief explanation",
  "suggestion": "close|warn|allow"
}`;
  }

  private async callGroqAPI(prompt: string, apiKey: string, config: any): Promise<any> {
    const response = await fetch(`${config.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: config.model,
        messages: [
          {
            role: 'system',
            content: 'You are a helpful productivity assistant. Always respond with valid JSON.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.1,
        max_tokens: 500,
      }),
    });

    if (!response.ok) {
      throw new Error(`Groq API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.choices[0]?.message?.content || '{}';
  }

  private parseGroqResponse(response: string): DistractionAnalysis {
    try {
      const parsed = JSON.parse(response);
      return {
        isDistracted: Boolean(parsed.isDistracted),
        confidence: Math.max(0, Math.min(1, Number(parsed.confidence) || 0)),
        reason: String(parsed.reason || 'No reason provided'),
        suggestion: ['close', 'warn', 'allow'].includes(parsed.suggestion) 
          ? parsed.suggestion 
          : 'allow',
        alternativeResources: parsed.alternativeResources || undefined,
      };
    } catch (error) {
      console.warn('Failed to parse Groq response:', response);
      return {
        isDistracted: false,
        confidence: 0,
        reason: 'Failed to parse AI response',
        suggestion: 'allow',
      };
    }
  }
}