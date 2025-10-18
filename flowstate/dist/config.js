import { promises as fs } from 'fs';
import path from 'path';
export class ConfigManager {
    configPath;
    config = null;
    constructor(configPath) {
        const home = process.env.HOME || process.env.USERPROFILE || '.';
        this.configPath = configPath ?? path.join(home, '.flowstate', 'config.json');
    }
    getDefaultConfig() {
        return {
            version: '1.0.0',
            userPreferences: {
                learningSession: {
                    defaultDuration: 30,
                    autoStart: false,
                    smartDeduplication: true,
                },
                distractionDetection: {
                    enabled: true,
                    sensitivity: 'medium',
                    autoIntervention: false,
                    warningThreshold: 0.7,
                },
                notifications: {
                    enabled: true,
                    sound: true,
                    desktop: true,
                },
                ui: {
                    theme: 'auto',
                    language: 'en',
                    showAdvanced: false,
                },
            },
            apiConfig: {
                groq: {
                    model: 'llama-3.1-8b-instant',
                    baseUrl: 'https://api.groq.com/openai/v1',
                    timeout: 30000,
                },
            },
            system: {
                dataDir: path.join(process.env.HOME || process.env.USERPROFILE || '.', '.flowstate'),
                logLevel: 'info',
                maxLogFiles: 10,
            },
            tasks: {
                autoSave: true,
                maxHistoryDays: 30,
                defaultTaskDuration: 25, // 25分钟 Pomodoro
            },
        };
    }
    async ensureConfigDir() {
        await fs.mkdir(path.dirname(this.configPath), { recursive: true });
    }
    async load() {
        if (this.config)
            return this.config;
        try {
            await this.ensureConfigDir();
            const raw = await fs.readFile(this.configPath, 'utf-8');
            const loaded = JSON.parse(raw);
            // 合并默认配置，确保新字段有默认值
            this.config = this.mergeWithDefaults(loaded);
            return this.config;
        }
        catch (error) {
            if (error?.code === 'ENOENT') {
                // 配置文件不存在，使用默认配置
                this.config = this.getDefaultConfig();
                await this.save();
                return this.config;
            }
            throw new Error(`Failed to load config: ${error.message}`);
        }
    }
    mergeWithDefaults(loaded) {
        const defaults = this.getDefaultConfig();
        return {
            ...defaults,
            ...loaded,
            userPreferences: {
                ...defaults.userPreferences,
                ...loaded.userPreferences,
                learningSession: {
                    ...defaults.userPreferences.learningSession,
                    ...loaded.userPreferences?.learningSession,
                },
                distractionDetection: {
                    ...defaults.userPreferences.distractionDetection,
                    ...loaded.userPreferences?.distractionDetection,
                },
                notifications: {
                    ...defaults.userPreferences.notifications,
                    ...loaded.userPreferences?.notifications,
                },
                ui: {
                    ...defaults.userPreferences.ui,
                    ...loaded.userPreferences?.ui,
                },
            },
            apiConfig: {
                ...defaults.apiConfig,
                ...loaded.apiConfig,
                groq: {
                    ...defaults.apiConfig.groq,
                    ...loaded.apiConfig?.groq,
                },
            },
            system: {
                ...defaults.system,
                ...loaded.system,
            },
            tasks: {
                ...defaults.tasks,
                ...loaded.tasks,
            },
        };
    }
    async save() {
        if (!this.config) {
            throw new Error('No config loaded to save');
        }
        await this.ensureConfigDir();
        await fs.writeFile(this.configPath, JSON.stringify(this.config, null, 2), 'utf-8');
    }
    async updateUserPreferences(updates) {
        const config = await this.load();
        config.userPreferences = {
            ...config.userPreferences,
            ...updates,
            learningSession: {
                ...config.userPreferences.learningSession,
                ...updates.learningSession,
            },
            distractionDetection: {
                ...config.userPreferences.distractionDetection,
                ...updates.distractionDetection,
            },
            notifications: {
                ...config.userPreferences.notifications,
                ...updates.notifications,
            },
            ui: {
                ...config.userPreferences.ui,
                ...updates.ui,
            },
        };
        await this.save();
    }
    async updateAPIConfig(updates) {
        const config = await this.load();
        config.apiConfig = {
            ...config.apiConfig,
            ...updates,
            groq: {
                ...config.apiConfig.groq,
                ...updates.groq,
            },
        };
        await this.save();
    }
    async setAPIKey(service, apiKey) {
        const config = await this.load();
        if (!config.apiConfig[service]) {
            throw new Error(`Unknown API service: ${service}`);
        }
        config.apiConfig[service].apiKey = apiKey;
        await this.save();
    }
    async getAPIKey(service) {
        const config = await this.load();
        return config.apiConfig[service]?.apiKey;
    }
    async validateConfig() {
        const config = await this.load();
        const errors = [];
        // 验证API配置
        if (config.userPreferences.distractionDetection.enabled) {
            if (!config.apiConfig.groq.apiKey) {
                errors.push('Groq API key is required for distraction detection');
            }
        }
        // 验证数值范围
        if (config.userPreferences.distractionDetection.warningThreshold < 0 ||
            config.userPreferences.distractionDetection.warningThreshold > 1) {
            errors.push('Warning threshold must be between 0 and 1');
        }
        if (config.userPreferences.learningSession.defaultDuration < 1) {
            errors.push('Default learning duration must be at least 1 second');
        }
        if (config.tasks.defaultTaskDuration < 1) {
            errors.push('Default task duration must be at least 1 minute');
        }
        return {
            valid: errors.length === 0,
            errors,
        };
    }
    async resetToDefaults() {
        this.config = this.getDefaultConfig();
        await this.save();
    }
    getConfigPath() {
        return this.configPath;
    }
}
