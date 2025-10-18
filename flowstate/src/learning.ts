import { FocusEvent, Resource } from './types.js';

export interface SystemController {
  openApp(appId: string): Promise<void>;
  openUrl(url: string): Promise<void>;
  getActiveWindow(): Promise<{ appId: string; url?: string; title?: string }>;
  subscribeActiveWindow(cb: (e: FocusEvent) => void): () => void;
}

export class DevSystemController implements SystemController {
  private interval: NodeJS.Timeout | null = null;
  private urls = ['https://docs.google.com', 'https://stackoverflow.com', 'https://news.ycombinator.com'];
  private apps = ['code', 'terminal', 'browser'];

  async openApp(appId: string): Promise<void> {
    console.log(`[DEV] open app: ${appId}`);
  }
  async openUrl(url: string): Promise<void> {
    console.log(`[DEV] open url: ${url}`);
  }
  async getActiveWindow(): Promise<{ appId: string; url?: string; title?: string }> {
    return { appId: 'browser', url: this.urls[0], title: 'DEV Active' };
  }
  subscribeActiveWindow(cb: (e: FocusEvent) => void): () => void {
    if (this.interval) clearInterval(this.interval);
    this.interval = setInterval(() => {
      const ts = Date.now();
      const appId = this.apps[Math.floor(Math.random() * this.apps.length)];
      const url = Math.random() > 0.5 ? this.urls[Math.floor(Math.random() * this.urls.length)] : undefined;
      const title = url ? `Browsing ${new URL(url).hostname}` : `Using ${appId}`;
      cb({ ts, appId, url, title });
    }, 1000);
    return () => { if (this.interval) clearInterval(this.interval); this.interval = null; };
  }
}

export function canonicalizeUrl(url: string): string {
  try {
    const u = new URL(url);
    u.hash = '';
    u.search = '';
    return u.toString();
  } catch { return url; }
}

export class LearningSession {
  private stop?: () => void;
  private seen = new Map<string, Resource>();

  constructor(private sys: SystemController) {}

  start() {
    this.stop?.();
    this.stop = this.sys.subscribeActiveWindow((e) => {
      this.see({ kind: 'app', id: e.appId, title: e.title });
      if (e.url) this.see({ kind: 'url', id: canonicalizeUrl(e.url), title: e.title });
    });
  }

  private see(r: Resource) {
    const key = `${r.kind}:${r.id}`;
    this.seen.set(key, r);
  }

  finish(): Resource[] {
    this.stop?.();
    this.stop = undefined;
    return Array.from(this.seen.values());
  }
}

export async function launchResources(resources: Resource[], sys: SystemController) {
  for (const r of resources) {
    if (r.kind === 'app') await sys.openApp(r.id);
    else await sys.openUrl(r.id);
    await delay(300);
  }
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));
