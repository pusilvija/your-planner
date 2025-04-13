export function updateTaskOrder(taskId, newOrder, newStatus) {
    const csrf = document.querySelector('meta[name="csrf-token"]').content;

    // Get the task element by its ID (assuming each task has a unique ID)
    const taskElement = document.querySelector(`[data-id="${taskId}"]`);

    // Retrieve the task name (assuming the name is stored in the 'data-name' attribute)
    const taskName = taskElement ? taskElement.dataset.name : 'Unknown Task';

    console.log('Updating task order:', { taskId, taskName, newOrder, newStatus });

    fetch(`/update-task-order/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify({
            new_order: newOrder,
            new_status: newStatus
         }),
    })
    .then(res => res.json())
    .then(data => {
        if (data.status !== 'success') {
            console.error('Error updating order:', data.message);
        }
    })
    .catch(err => console.error('Fetch error:', err));
}

export function editTaskName(taskId, newName) {
    const csrf = document.querySelector('meta[name="csrf-token"]').content;

    fetch(`/edit_task_name/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify({ new_task_name: newName }),
    })
    .then(res => res.json())
    .then(data => {
        if (data.status !== 'success') {
            console.error('Error updating title:', data.message);
        }
    })
    .catch(err => console.error('Fetch error:', err));
}
