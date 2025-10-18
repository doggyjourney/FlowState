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
