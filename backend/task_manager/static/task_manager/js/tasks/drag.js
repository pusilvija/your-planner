export function initializeTaskDragging(task, container, manager) {
    task.addEventListener('mousedown', (e) => startDragging(task, e, container, manager));
}

function startDragging(task, e, container, manager) {
    manager.isDragging = false;

    // Initial mouse position
    const startX = e.clientX;
    const startY = e.clientY;

    // Offset between mouse and task
    const offsetX = e.clientX - task.offsetLeft;
    const offsetY = e.clientY - task.offsetTop;

    const onMouseMove = (e) => {
        console.log("onMouseMove: DRAGGING")
        // Measures how far mouse moved
        const deltaX = Math.abs(e.clientX - startX);
        const deltaY = Math.abs(e.clientY - startY);

        console.log("deltaX: ", deltaX, "deltaY: ", deltaY);

        // Only start dragging if the mouse moves beyond the threshold (e.g., 5px)
        if (!manager.isDragging && (deltaX > 20 || deltaY > 20)) {
            manager.isDragging = true;
            task.classList.add('dragging');
        }

        if (manager.isDragging) {
            const finalContainer = getContainerUnderMouse(e);
            const currentContainer = finalContainer.dataset.status === container.dataset.status ? container : finalContainer;

            updateDraggedTaskPosition(task, e, offsetX, offsetY, currentContainer);
        }
    };

    const onMouseUp = (e) => {
        if (!manager.isDragging) {
            return;
        } else {
            stopDragging(task, e, onMouseMove, onMouseUp, manager, container);
        }
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
}

function updateDraggedTaskPosition(task, e, offsetX, offsetY, container) {
    requestAnimationFrame(() => {
        if (!container) {
            console.error('Container is null. Skipping position update.');
            return;
        }

        let new_top = Math.max(0, Math.min(e.clientY - offsetY, container.offsetHeight - task.offsetHeight));
        let new_left = Math.max(0, Math.min(e.clientX - offsetX, container.offsetWidth - task.offsetWidth));

        task.style.left = `${new_left}px`;
        task.style.top = `${new_top}px`;

        const prev_task_status = task.dataset.status;
        const prev_task_container = task.dataset.container;

        task.dataset.status = container.dataset.status;
        task.dataset.container = container.dataset.status;

        // Check the task's relative position in the container (whether it's above or below other tasks)
        const tasksInContainer = Array.from(container.querySelectorAll('.task'));
        tasksInContainer.sort((a, b) => a.offsetTop - b.offsetTop); // Sort tasks by their vertical position (top)

        let targetTask = null;
        tasksInContainer.forEach((taskInContainer, index) => {
            // Check if the mouse is in the middle of the task
            if (e.clientY > taskInContainer.offsetTop && e.clientY < taskInContainer.offsetTop + taskInContainer.offsetHeight) {
                targetTask = taskInContainer;
            }
        });

        if (targetTask) {
            // Insert the task before or after the target task based on its position
            if (e.clientY < targetTask.offsetTop) {
                container.insertBefore(task, targetTask);
            } else if (e.clientY > targetTask.offsetTop + targetTask.offsetHeight) {
                container.insertBefore(task, targetTask.nextSibling);
            }
        }

    });
}

function stopDragging(task, e, onMouseMove, onMouseUp, manager, container) {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
    task.classList.remove('dragging');
    manager.isDragging = false;

    // Determine the final container
    const finalContainer = getContainerUnderMouse(e);
    finalContainer.appendChild(task);

    // Reorder tasks in the container
    document.querySelectorAll('.task-container').forEach((c) => {
        manager.reorderTasks(c);
    });
}

function getContainerUnderMouse(e) {
    const containers = document.querySelectorAll('.task-container');
    for (const container of containers) {
        const rect = container.getBoundingClientRect();
        if (
            e.clientX >= rect.left &&
            e.clientX <= rect.right &&
            e.clientY >= rect.top &&
            e.clientY <= rect.bottom
        ) {
            return container; // Return the container under the mouse
        }
    }
    return null; // No container found under the mouse
}
