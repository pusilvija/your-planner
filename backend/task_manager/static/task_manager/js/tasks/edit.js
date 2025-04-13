export function setupEditClickHandler(task, manager) {
    const editBtn = task.querySelector('#edit-task-name');
    const taskName = task.querySelector('.task-name');
    const editInput = task.querySelector('.edit-input');

    if (editBtn && taskName && editInput) {
        editBtn.addEventListener('mousedown', (e) => {
            e.stopPropagation(); 
            // Optionally: e.preventDefault(); 
        });
        editBtn.addEventListener('click', (e) => {
            e.preventDefault();
            taskName.style.display = 'none';
            editInput.style.display = 'block';
            editInput.focus();
            const val = editInput.value;
            editInput.value = '';
            editInput.value = val;
        });

        editInput.addEventListener('blur', () => {
            const newName = editInput.value.trim();
            if (newName) {
                taskName.textContent = newName;
                manager.editTaskName(task.dataset.id, newName);
            }
            editInput.style.display = 'none';
            taskName.style.display = 'block';
        });

        editInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') editInput.blur();
        });
    }
}
