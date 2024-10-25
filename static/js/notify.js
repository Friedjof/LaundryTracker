function playNotificationSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();

    // Harmonie aus einem C-Dur-Akkord: C, E, G, C (Oktave)
    const frequencies = [261.63, 329.63, 392.00, 523.25]; // C-Dur Akkord-Frequenzen
    const duration = 0.2; // Dauer jedes Tons in Sekunden

    frequencies.forEach((frequency, index) => {
        // Erstellen eines Oszillators
        const oscillator = audioContext.createOscillator();
        oscillator.type = 'sine'; // Sinuswelle für einen angenehmen und harmonischen Klang
        oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime + index * duration);

        // Erstellen eines Gain-Nodes für Lautstärke-Hüllkurve
        const gainNode = audioContext.createGain();
        gainNode.gain.setValueAtTime(0, audioContext.currentTime + index * duration);
        gainNode.gain.linearRampToValueAtTime(0.5, audioContext.currentTime + index * duration + 0.05); // Lautstärke langsam steigern
        gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + (index + 1) * duration); // Lautstärke verringern

        // Verbinden des Oszillators mit dem Gain-Nodes und dem Audio-Context
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        // Starten und Stoppen des Oszillators
        oscillator.start(audioContext.currentTime + index * duration);
        oscillator.stop(audioContext.currentTime + (index + 1) * duration);
    });
}

function showNotification(message, type = 'success', logLevel = 'info', bell = false) {
    const container = document.getElementById('notification-container');
    const alert = document.createElement('div');
    const badgeClass = getBadgeClass(logLevel);
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        <div class="row">
            <div class="col-auto">
                <span class="badge ${badgeClass}">${logLevel.toUpperCase()}</span>
            </div>
            <div class="col">
                ${message}
            </div>
            <div class="col-auto">
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>
    `;
    container.appendChild(alert);

    if (bell) {
        playNotificationSound();
    }

    // Automatically remove the alert after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        alert.addEventListener('transitionend', () => alert.remove());
    }, 5000);
}

function getBadgeClass(logLevel) {
    const logLevelClasses = {
        info: 'bg-info',
        success: 'bg-success',
        warning: 'bg-warning',
        error: 'bg-danger'
    };
    return logLevelClasses[logLevel] || 'bg-secondary'; // Default to 'bg-secondary' if logLevel is not found
}
