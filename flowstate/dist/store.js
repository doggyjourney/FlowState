import { promises as fs } from 'fs';
import path from 'path';
const DEFAULT_DATA = { tasks: [], sessions: [] };
export class TaskStore {
    filePath;
    data = null;
    constructor(filePath) {
        const home = process.env.HOME || process.env.USERPROFILE || '.';
        this.filePath = filePath ?? path.join(home, '.flowstate', 'store.json');
    }
    async ensureDir() {
        await fs.mkdir(path.dirname(this.filePath), { recursive: true });
    }
    async readFile() {
        try {
            const raw = await fs.readFile(this.filePath, 'utf-8');
            const parsed = JSON.parse(raw);
            return { tasks: parsed.tasks ?? [], sessions: parsed.sessions ?? [] };
        }
        catch (e) {
            if (e && (e.code === 'ENOENT' || e.code === 'EISDIR')) {
                return { ...DEFAULT_DATA };
            }
            throw e;
        }
    }
    async load() {
        if (this.data)
            return this.data;
        await this.ensureDir();
        this.data = await this.readFile();
        return this.data;
    }
    async persist() {
        await this.ensureDir();
        const data = this.data ?? DEFAULT_DATA;
        await fs.writeFile(this.filePath, JSON.stringify(data, null, 2), 'utf-8');
    }
    async save(data) {
        this.data = data;
        await this.persist();
    }
    async createTask(name) {
        const data = await this.load();
        const now = Date.now();
        const task = {
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
    async listTasks() {
        const data = await this.load();
        return data.tasks.slice().sort((a, b) => b.updatedAt - a.updatedAt);
    }
    async getTask(id) {
        const data = await this.load();
        return data.tasks.find(t => t.id === id);
    }
    async upsertTask(task) {
        const data = await this.load();
        const idx = data.tasks.findIndex(t => t.id === task.id);
        task.updatedAt = Date.now();
        if (idx >= 0)
            data.tasks[idx] = task;
        else
            data.tasks.push(task);
        await this.persist();
    }
    async startSession(taskId) {
        const data = await this.load();
        const now = Date.now();
        const session = {
            id: `sess_${now}_${Math.random().toString(36).slice(2, 8)}`,
            taskId,
            startedAt: now,
            resourcesUsed: [],
        };
        data.sessions.push(session);
        await this.persist();
        return session;
    }
    async endSession(sessionId, used) {
        const data = await this.load();
        const session = data.sessions.find(s => s.id === sessionId);
        if (!session)
            throw new Error('Session not found');
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
export function mergeResources(prev, next) {
    const map = new Map();
    const key = (r) => `${r.kind}:${r.id}`;
    for (const r of prev)
        map.set(key(r), r);
    for (const r of next)
        map.set(key(r), r);
    return Array.from(map.values());
}
