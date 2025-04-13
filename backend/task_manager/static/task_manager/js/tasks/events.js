export function setupTaskClickHandler(task) {
    let wasDragging = false;

    task.addEventListener('mousedown', () => wasDragging = false);
    task.addEventListener('mousemove', () => wasDragging = true);

    task.addEventListener('click', (e) => {
        if (!wasDragging && !e.target.closest('.task-buttons') && !e.target.closest('input')) {
            window.location.href = `/task/${task.id}/`;
        }
        wasDragging = false;
    });

    const buttons = task.querySelectorAll('.task-buttons button, .task-buttons a');
    buttons.forEach(btn => {
        btn.addEventListener('click', e => e.stopPropagation());
    });
}
