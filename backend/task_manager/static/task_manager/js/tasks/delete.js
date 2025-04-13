export function setupDeleteClickHandler(task) {
    const deleteBtn = task.querySelector('#delete-task');

    if (deleteBtn) {
        deleteBtn.addEventListener('mousedown', (e) => {
            e.stopPropagation(); 
            // Optionally: e.preventDefault(); 
        });
    }
}
