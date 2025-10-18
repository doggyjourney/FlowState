export type Resource =
  | { kind: 'app'; id: string; title?: string; meta?: Record<string, unknown> }
  | { kind: 'url'; id: string; title?: string; meta?: Record<string, unknown> };

export type Task = {
  id: string;
  name: string;
  resources: Resource[];
  createdAt: number;
  updatedAt: number;
};

export type Session = {
  id: string;
  taskId: string;
  startedAt: number;
  endedAt?: number;
  resourcesUsed: Resource[];
};

export type FocusEvent = {
  ts: number;
  appId: string;
  url?: string;
  title?: string;
};

export type DistractionAnalysis = {
  isDistracted: boolean;
  confidence: number; // 0-1
  reason: string;
  suggestion: 'close' | 'warn' | 'allow';
  alternativeResources?: Resource[];
};

export type DistractionDetector = {
  analyzeFocusEvent(event: FocusEvent, task: Task): Promise<DistractionAnalysis>;
  analyzeResource(resource: Resource, task: Task): Promise<DistractionAnalysis>;
};

export type UserPreferences = {
  // 学习会话设置
  learningSession: {
    defaultDuration: number; // 默认学习时长（秒）
    autoStart: boolean; // 是否自动开始学习会话
    smartDeduplication: boolean; // 是否启用智能去重
  };
  
  // 分心检测设置
  distractionDetection: {
    enabled: boolean; // 是否启用分心检测
    sensitivity: 'low' | 'medium' | 'high'; // 检测敏感度
    autoIntervention: boolean; // 是否自动干预
    warningThreshold: number; // 警告阈值（0-1）
  };
  
  // 通知设置
  notifications: {
    enabled: boolean; // 是否启用通知
    sound: boolean; // 是否播放声音
    desktop: boolean; // 是否显示桌面通知
  };
  
  // 界面设置
  ui: {
    theme: 'light' | 'dark' | 'auto'; // 主题
    language: string; // 语言
    showAdvanced: boolean; // 是否显示高级选项
  };
};

export type APIConfig = {
  groq: {
    apiKey?: string;
    model: string;
    baseUrl: string;
    timeout: number;
  };
  // 为未来扩展其他AI服务预留
  openai?: {
    apiKey?: string;
    model: string;
    baseUrl: string;
  };
  anthropic?: {
    apiKey?: string;
    model: string;
    baseUrl: string;
  };
};

export type AppConfig = {
  version: string;
  userPreferences: UserPreferences;
  apiConfig: APIConfig;
  // 系统设置
  system: {
    dataDir: string; // 数据目录
    logLevel: 'debug' | 'info' | 'warn' | 'error';
    maxLogFiles: number;
  };
  // 任务设置
  tasks: {
    autoSave: boolean; // 是否自动保存
    maxHistoryDays: number; // 最大历史记录天数
    defaultTaskDuration: number; // 默认任务时长（分钟）
  };
};
