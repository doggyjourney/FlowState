import { promises as fs } from 'fs';
import path from 'path';
import { Resource, Session, Task } from './types.js';

export type StoreData = { tasks: Task[]; sessions: Session[] };

const DEFAULT_DATA: StoreData = { tasks: [], sessions: [] };

export class TaskStore {
  private readonly filePath: string;
  private data: StoreData | null = null;

  constructor(filePath?: string) {
    const home = process.env.HOME || process.env.USERPROFILE || '.';
    this.filePath = filePath ?? path.join(home, '.flowstate', 'store.json');
  }

  private async ensureDir() {
    await fs.mkdir(path.dirname(this.filePath), { recursive: true });
  }

  private async readFile(): Promise<StoreData> {
    try {
      const raw = await fs.readFile(this.filePath, 'utf-8');
      const parsed = JSON.parse(raw) as StoreData;
      return { tasks: parsed.tasks ?? [], sessions: parsed.sessions ?? [] };
    } catch (e: any) {
      if (e && (e.code === 'ENOENT' || e.code === 'EISDIR')) {
        return { ...DEFAULT_DATA };
      }
      throw e;
    }
  }

  async load(): Promise<StoreData> {
    if (this.data) return this.data;
    await this.ensureDir();
    this.data = await this.readFile();
    return this.data;
  }

  private async persist() {
    await this.ensureDir();
    const data = this.data ?? DEFAULT_DATA;
    await fs.writeFile(this.filePath, JSON.stringify(data, null, 2), 'utf-8');
  }

  async save(data: StoreData): Promise<void> {
    this.data = data;
    await this.persist();
  }

  async createTask(name: string): Promise<Task> {
    const data = await this.load();
    const now = Date.now();
    const task: Task = {
      id: `task_${now}_${Math.random().toString(36).slice(2, 8)}`,
      name,
      resources: [],
      createdAt: now,
      updatedAt: now,
    };
    data.tasks.push(task);
    await this.persist();
    return task;
  }

  async listTasks(): Promise<Task[]> {
    const data = await this.load();
    return data.tasks.slice().sort((a, b) => b.updatedAt - a.updatedAt);
  }

  async getTask(id: string): Promise<Task | undefined> {
    const data = await this.load();
    return data.tasks.find(t => t.id === id);
  }

  async upsertTask(task: Task): Promise<void> {
    const data = await this.load();
    const idx = data.tasks.findIndex(t => t.id === task.id);
    task.updatedAt = Date.now();
    if (idx >= 0) data.tasks[idx] = task; else data.tasks.push(task);
    await this.persist();
  }

  async startSession(taskId: string): Promise<Session> {
    const data = await this.load();
    const now = Date.now();
    const session: Session = {
      id: `sess_${now}_${Math.random().toString(36).slice(2, 8)}`,
      taskId,
      startedAt: now,
      resourcesUsed: [],
    };
    data.sessions.push(session);
    await this.persist();
    return session;
  }

  async endSession(sessionId: string, used: Resource[]): Promise<void> {
    const data = await this.load();
    const session = data.sessions.find(s => s.id === sessionId);
    if (!session) throw new Error('Session not found');
    session.endedAt = Date.now();
    session.resourcesUsed = used;
    const task = data.tasks.find(t => t.id === session.taskId);
    if (task) {
      const merged = mergeResources(task.resources, used);
      task.resources = merged;
      task.updatedAt = Date.now();
    }
    await this.persist();
  }
}

export function mergeResources(prev: Resource[], next: Resource[]): Resource[] {
  const map = new Map<string, Resource>();
  const key = (r: Resource) => `${r.kind}:${r.id}`;
  for (const r of prev) map.set(key(r), r);
  for (const r of next) map.set(key(r), r);
  return Array.from(map.values());
}
