#!/usr/bin/env node
import { Command } from 'commander';
import { TaskStore } from './store.js';
import { DevSystemController, LearningSession, launchResources } from './learning.js';
const program = new Command();
program
    .name('flow')
    .description('FlowState CLI (dev)')
    .version('0.1.0');
const store = new TaskStore();
const sys = new DevSystemController();
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
    .option('-d, --duration <seconds>', 'Duration seconds (default 10)', '10')
    .action(async (taskId, opts) => {
    const t = await store.getTask(taskId);
    if (!t) {
        console.error('Task not found');
        process.exit(1);
    }
    const sess = await store.startSession(taskId);
    const learning = new LearningSession(sys);
    learning.start();
    const seconds = parseInt(opts.duration, 10) || 10;
    console.log(`Learning for ${seconds}s... Press Ctrl+C to abort.`);
    await new Promise((r) => setTimeout(r, seconds * 1000));
    const used = learning.finish();
    await store.endSession(sess.id, used);
    console.log(`Merged ${used.length} resources into task`);
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
program.parseAsync(process.argv);
