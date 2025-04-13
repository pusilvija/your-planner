import { setInitialTaskSpacing } from './utils.js';
import { initializeTaskDragging } from './drag.js';
import { setupEditClickHandler } from './edit.js';
import { setupDeleteClickHandler } from './delete.js';
import { setupTaskClickHandler } from './events.js';
import { updateTaskOrder, editTaskName } from './api.js';

export class TaskManager {
    constructor() {
        this.taskContainers = Array.from(document.querySelectorAll('.task-container')); 
        this.tasks = Array.from(document.querySelectorAll('.task')); 
        // this.taskContainer = document.getElementById('task-container');
        this.taskTitle = document.getElementById('task-title');
        this.taskStatus = document.getElementById('task-status');
        this.taskDescription = document.getElementById('task-description');
        this.taskCategory = document.getElementById('task-category');
        this.addTaskButton = document.getElementById('add-task');
        this.taskHeight = this.tasks[0].offsetHeight; //this.tasks[0]?.offsetHeight || 100;
        this.spaceBetweenTasks = 20;
        this.dragZoneHeight = this.taskHeight + this.spaceBetweenTasks;
        this.isDragging = false;

        this.initialize();
    }

    initialize() {
        this.taskContainers.forEach(container => {
            // console.log('Container: ', container)
            const tasksInContainer = Array.from(container.querySelectorAll('.task'));
            setInitialTaskSpacing(tasksInContainer, container, this.dragZoneHeight, this.spaceBetweenTasks);

            tasksInContainer.forEach(task => {
                initializeTaskDragging(task, container, this);
                setupEditClickHandler(task, this);
                setupTaskClickHandler(task);
                setupDeleteClickHandler(task);
            });
        });


        if (this.addTaskButton) {
            this.addTaskButton.addEventListener('click', () => {
                window.location.href = "/add-task/";
            });
        }
    }

    reorderTasks(container = null) {
        // If a specific container is provided, reorder tasks only in that container
        const containersToReorder = container ? [container] : this.taskContainers;
    
        containersToReorder.forEach(container => {
            const tasksInContainer = Array.from(container.querySelectorAll('.task'));
            const status = container.dataset.status; // Get the status from the container's data-status attribute

            console.log(
                "Tasks in", 
                container.dataset.status, 
                ":", 
                Array.from(container.querySelectorAll('.task')).map(t => `${t.dataset.name}(${t.dataset.order})`)
            );
    
            // Sort tasks by their vertical position (offsetTop)
            const taskPositions = tasksInContainer
                .map(task => ({ task, top: task.offsetTop }))
                .sort((a, b) => a.top - b.top);
    
            // Reassign order and update the backend
            taskPositions.forEach((item, index) => {
                console.log("Item: ", item.task.dataset.name, " -> ", index);
                item.task.style.top = `${index * this.dragZoneHeight + this.spaceBetweenTasks}px`;
                updateTaskOrder(item.task.dataset.id, index, status); // Pass the status to the API
            });
        });
    }

    editTaskName(taskId, newName) {
        editTaskName(taskId, newName);
    }
}
