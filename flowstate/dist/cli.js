#!/usr/bin/env node
import { Command } from 'commander';
import { TaskStore } from './store.js';
import { DevSystemController, LearningSession, launchResources } from './learning.js';
import { ConfigManager } from './config.js';
import { GroqDistractionDetector } from './groq-detector.js';
const program = new Command();
program
    .name('flow')
    .description('FlowState CLI (dev)')
    .version('0.1.0');
const store = new TaskStore();
const sys = new DevSystemController();
const config = new ConfigManager();
program
    .command('task:create')
    .description('Create a new task')
    .argument('<name>', 'Task name')
    .action(async (name) => {
    const t = await store.createTask(name);
    console.log('Created task:', t.id, t.name);
});
program
    .command('task:list')
    .description('List tasks')
    .action(async () => {
    const list = await store.listTasks();
    for (const t of list) {
        console.log(`${t.id}\t${t.name}\tresources:${t.resources.length}`);
    }
});
program
    .command('task:show')
    .description('Show a task')
    .argument('<taskId>', 'Task id')
    .action(async (taskId) => {
    const t = await store.getTask(taskId);
    if (!t) {
        console.error('Task not found');
        process.exit(1);
    }
    console.log(JSON.stringify(t, null, 2));
});
program
    .command('task:learn')
    .description('Start a learning session and merge resources into the task')
    .argument('<taskId>', 'Task id')
    .option('-d, --duration <seconds>', 'Duration seconds (default from config)')
    .option('--with-detection', 'Enable distraction detection during learning')
    .action(async (taskId, opts) => {
    const t = await store.getTask(taskId);
    if (!t) {
        console.error('Task not found');
        process.exit(1);
    }
    const cfg = await config.load();
    const seconds = opts.duration ? parseInt(opts.duration, 10) : cfg.userPreferences.learningSession.defaultDuration;
    const sess = await store.startSession(taskId);
    const learning = new LearningSession(sys);
    // 如果启用分心检测
    if (opts.withDetection && cfg.userPreferences.distractionDetection.enabled) {
        const detector = new GroqDistractionDetector(config);
        console.log('🔍 Distraction detection enabled');
        // 这里可以添加实时检测逻辑
        // 为了简化，我们只在学习结束时进行分析
    }
    learning.start();
    console.log(`Learning for ${seconds}s... Press Ctrl+C to abort.`);
    await new Promise((r) => setTimeout(r, seconds * 1000));
    const used = learning.finish();
    await store.endSession(sess.id, used);
    console.log(`Merged ${used.length} resources into task`);
    console.log(`Learning session duration: ${Math.round(learning.getDuration() / 1000)}s`);
    // 如果启用了分心检测，分析收集的资源
    if (opts.withDetection && cfg.userPreferences.distractionDetection.enabled) {
        const detector = new GroqDistractionDetector(config);
        console.log('🔍 Analyzing collected resources for distractions...');
        for (const resource of used) {
            const analysis = await detector.analyzeResource(resource, t);
            if (analysis.isDistracted && analysis.confidence > cfg.userPreferences.distractionDetection.warningThreshold) {
                console.log(`⚠️  Potential distraction: ${resource.kind}:${resource.id}`);
                console.log(`   Reason: ${analysis.reason}`);
                console.log(`   Suggestion: ${analysis.suggestion}`);
            }
        }
    }
});
program
    .command('task:start')
    .description('Launch resources for a task')
    .argument('<taskId>', 'Task id')
    .action(async (taskId) => {
    const t = await store.getTask(taskId);
    if (!t) {
        console.error('Task not found');
        process.exit(1);
    }
    await launchResources(t.resources, sys);
    console.log('Launched resources');
});
// 配置管理命令
program
    .command('config:show')
    .description('Show current configuration')
    .option('-j, --json', 'Output as JSON')
    .action(async (opts) => {
    const cfg = await config.load();
    if (opts.json) {
        console.log(JSON.stringify(cfg, null, 2));
    }
    else {
        console.log('Configuration:');
        console.log(`  Config file: ${config.getConfigPath()}`);
        console.log(`  Version: ${cfg.version}`);
        console.log(`  Data directory: ${cfg.system.dataDir}`);
        console.log(`  Log level: ${cfg.system.logLevel}`);
        console.log(`  Groq API configured: ${cfg.apiConfig.groq.apiKey ? 'Yes' : 'No'}`);
        console.log(`  Distraction detection: ${cfg.userPreferences.distractionDetection.enabled ? 'Enabled' : 'Disabled'}`);
        console.log(`  Learning auto-start: ${cfg.userPreferences.learningSession.autoStart ? 'Enabled' : 'Disabled'}`);
    }
});
program
    .command('config:set')
    .description('Set configuration values')
    .argument('<key>', 'Configuration key (e.g., learningSession.defaultDuration)')
    .argument('<value>', 'Configuration value')
    .action(async (key, value) => {
    try {
        const cfg = await config.load();
        const keys = key.split('.');
        let current = cfg;
        // 导航到目标对象
        for (let i = 0; i < keys.length - 1; i++) {
            if (!current[keys[i]]) {
                current[keys[i]] = {};
            }
            current = current[keys[i]];
        }
        // 设置值
        const lastKey = keys[keys.length - 1];
        const parsedValue = isNaN(Number(value)) ? value : Number(value);
        current[lastKey] = parsedValue;
        await config.save();
        console.log(`Set ${key} = ${parsedValue}`);
    }
    catch (error) {
        console.error(`Failed to set config: ${error.message}`);
        process.exit(1);
    }
});
program
    .command('config:api-key')
    .description('Set API key for a service')
    .argument('<service>', 'API service (groq, openai, anthropic)')
    .argument('<key>', 'API key')
    .action(async (service, key) => {
    try {
        await config.setAPIKey(service, key);
        console.log(`Set ${service} API key`);
    }
    catch (error) {
        console.error(`Failed to set API key: ${error.message}`);
        process.exit(1);
    }
});
program
    .command('config:validate')
    .description('Validate current configuration')
    .action(async () => {
    const validation = await config.validateConfig();
    if (validation.valid) {
        console.log('✅ Configuration is valid');
    }
    else {
        console.log('❌ Configuration has errors:');
        validation.errors.forEach(error => console.log(`  - ${error}`));
        process.exit(1);
    }
});
program
    .command('config:reset')
    .description('Reset configuration to defaults')
    .option('-f, --force', 'Force reset without confirmation')
    .action(async (opts) => {
    if (!opts.force) {
        console.log('This will reset all configuration to defaults. Continue? (y/N)');
        // 在hackathon环境中，我们直接重置
    }
    await config.resetToDefaults();
    console.log('Configuration reset to defaults');
});
program
    .command('config:preferences')
    .description('Manage user preferences')
    .option('-s, --set <key=value>', 'Set preference (can be used multiple times)')
    .option('-l, --list', 'List all preferences')
    .action(async (opts) => {
    if (opts.list) {
        const cfg = await config.load();
        console.log('User Preferences:');
        console.log(JSON.stringify(cfg.userPreferences, null, 2));
    }
    else if (opts.set) {
        for (const setting of opts.set) {
            const [key, value] = setting.split('=');
            if (!key || !value) {
                console.error(`Invalid setting format: ${setting}. Use key=value`);
                continue;
            }
            try {
                const updates = {};
                const keys = key.split('.');
                let current = updates;
                for (let i = 0; i < keys.length - 1; i++) {
                    current[keys[i]] = {};
                    current = current[keys[i]];
                }
                const lastKey = keys[keys.length - 1];
                const parsedValue = isNaN(Number(value)) ? value : Number(value);
                current[lastKey] = parsedValue;
                await config.updateUserPreferences(updates);
                console.log(`Set ${key} = ${parsedValue}`);
            }
            catch (error) {
                console.error(`Failed to set preference: ${error.message}`);
            }
        }
    }
    else {
        console.log('Use --list to show preferences or --set key=value to set them');
    }
});
// 分心检测监控命令
program
    .command('monitor:start')
    .description('Start real-time distraction monitoring for a task')
    .argument('<taskId>', 'Task id to monitor')
    .option('-i, --interval <seconds>', 'Check interval in seconds (default 5)', '5')
    .action(async (taskId, opts) => {
    const t = await store.getTask(taskId);
    if (!t) {
        console.error('Task not found');
        process.exit(1);
    }
    const cfg = await config.load();
    if (!cfg.userPreferences.distractionDetection.enabled) {
        console.error('Distraction detection is disabled. Enable it in config first.');
        process.exit(1);
    }
    if (!cfg.apiConfig.groq.apiKey) {
        console.error('Groq API key not configured. Set it with: flow config:api-key groq <your-key>');
        process.exit(1);
    }
    const detector = new GroqDistractionDetector(config);
    const interval = parseInt(opts.interval, 10) || 5;
    console.log(`🔍 Starting distraction monitoring for task: ${t.name}`);
    console.log(`   Check interval: ${interval}s`);
    console.log(`   Press Ctrl+C to stop`);
    const checkDistraction = async () => {
        try {
            const activeWindow = await sys.getActiveWindow();
            const focusEvent = {
                ts: Date.now(),
                appId: activeWindow.appId,
                url: activeWindow.url,
                title: activeWindow.title,
            };
            const analysis = await detector.analyzeFocusEvent(focusEvent, t);
            if (analysis.isDistracted && analysis.confidence > cfg.userPreferences.distractionDetection.warningThreshold) {
                console.log(`\n⚠️  DISTRACTION DETECTED!`);
                console.log(`   App: ${activeWindow.appId}`);
                console.log(`   URL: ${activeWindow.url || 'N/A'}`);
                console.log(`   Title: ${activeWindow.title || 'N/A'}`);
                console.log(`   Reason: ${analysis.reason}`);
                console.log(`   Confidence: ${Math.round(analysis.confidence * 100)}%`);
                console.log(`   Suggestion: ${analysis.suggestion.toUpperCase()}`);
                if (analysis.alternativeResources && analysis.alternativeResources.length > 0) {
                    console.log(`   Suggested alternatives:`);
                    analysis.alternativeResources.forEach(resource => {
                        console.log(`     - ${resource.kind}:${resource.id} (${resource.title || 'No title'})`);
                    });
                }
            }
            else {
                process.stdout.write('.');
            }
        }
        catch (error) {
            console.warn(`\nError during monitoring: ${error.message}`);
        }
    };
    // 立即检查一次
    await checkDistraction();
    // 设置定期检查
    const intervalId = setInterval(checkDistraction, interval * 1000);
    // 处理退出信号
    process.on('SIGINT', () => {
        clearInterval(intervalId);
        console.log('\n🛑 Monitoring stopped');
        process.exit(0);
    });
});
program.parseAsync(process.argv);
