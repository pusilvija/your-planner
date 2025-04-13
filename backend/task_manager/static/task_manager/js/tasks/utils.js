export function setInitialTaskSpacing(tasks, container, height, spacing) {
    tasks.forEach((task, index) => {
        task.style.top = `${index * height + spacing}px`;
    });

    let totalHeight = tasks.length * (height + spacing) + height;
    container.style.height = `${totalHeight}px`;
    document.body.style.minHeight = `${totalHeight + 500}px`;
}
