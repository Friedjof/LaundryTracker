function showNotification(message, type = 'success', logLevel = 'info') {
    const container = document.getElementById('notification-container');
    const alert = document.createElement('div');
    const timestamp = new Date().toLocaleTimeString();
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        [${logLevel.toUpperCase()}] ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    container.appendChild(alert);

    // Automatically remove the alert after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        alert.addEventListener('transitionend', () => alert.remove());
    }, 5000);
}