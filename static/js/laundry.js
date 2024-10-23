document.addEventListener('DOMContentLoaded', function () {
    // CSRF token and building identifier
    const buildingId = document.getElementById('building-identifier').value;
    const csrfToken = document.getElementById('csrf-token').value;

    // machine modal
    document.getElementById('machine-modal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const machineIdentifier = button.getAttribute('data-machine-identifier');
        const machineName = button.getAttribute('data-machine-name');
        const machineType = button.getAttribute('data-machine-type');
        const machineStatus = button.getAttribute('data-machine-status');
        const machineNote = button.getAttribute('data-machine-note');

        const modal = this;

        const modalTitle = modal.querySelector('.modal-title');
        const modalNote = document.getElementById('defect-badge');
        const modalMachineStatus = document.getElementById('modal-machine-status');
        const modalMachineDuration = document.getElementById('modal-machine-duration');
        const modalDefectForm = document.getElementById('modal-defect-form');

        modalTitle.textContent = `${machineName} (${machineType})`;

        if (machineStatus === 'defect') {
            modalNote.innerText = machineNote;
        } else {
            modalNote.innerText = '';
        }

        modalMachineStatus.innerText = machineStatus;
        modalMachineStatus.classList.remove('Available', 'Running', 'Finished', 'Defect', 'Blinking', 'Unknown');
        modalMachineStatus.classList.add(machineStatus);

        modalMachineDuration.value = '';

        modalDefectForm.style.display = 'none';
    });

    // machine modal defect link
    document.getElementById('modal-defect-link').addEventListener('click', function () {
        const modalDefectForm = document.getElementById('modal-defect-form');

        if (modalDefectForm.style.display === 'none') {
            modalDefectForm.style.display = 'block';
        } else {
            modalDefectForm.style.display = 'none';
        }
    });

    // machine buttons
    Array.from(document.getElementsByClassName('machine-btn')).forEach(function (button) {
        button.addEventListener('click', function () {
            const identifier = button.getAttribute('data-machine-identifier');
            // TODO: add logic
        });
    });

    // websocket test TODO: remove
    function sendMessageEverySecond() {
        const socket = new WebSocket('wss://laundry.local.dev/laundry/ws/laundry');

        // Verbindung öffnen
        socket.onopen = function(event) {
            console.log("WebSocket-Verbindung hergestellt.");

            // Sende eine Nachricht jede Sekunde
            setInterval(function() {
                const message = { message: "Hallo, dies ist eine Nachricht!" };
                socket.send(JSON.stringify(message));
                console.log("Nachricht gesendet:", message);
            }, 1000);  // 1000ms = 1 Sekunde
        };

        // Fehlermeldung anzeigen
        socket.onerror = function(error) {
            console.log('WebSocket-Fehler: ' + error);
        };

        // Schließen der Verbindung anzeigen
        socket.onclose = function(event) {
            console.log("WebSocket-Verbindung geschlossen.");
        };

        // Nachrichten empfangen
        socket.onmessage = function(event) {
            console.log("Nachricht erhalten:", event.data);
        };
    }

    sendMessageEverySecond();
});