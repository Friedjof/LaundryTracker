document.addEventListener('DOMContentLoaded', function () {
    const buildingId = document.getElementById('building_id').value;
    const csrfToken = document.getElementById('csrfToken').value;

    const timerModal = document.getElementById('timerModal');
    if (timerModal) {
        timerModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const machineId = button.getAttribute('data-machine-id');
            const machineStatus = button.getAttribute('data-machine-status');
            const machineNumber = button.getAttribute('data-machine-number');
            const machineType = button.getAttribute('data-machine-type');
            const machineNotes = button.getAttribute('data-machine-notes');

            const timerModalLabel = document.getElementById('timerModalLabel');
            if (timerModalLabel) {
                if (machineStatus === 'A' || machineStatus === 'F') {
                    timerModalLabel.innerText = `Start machine ${machineNumber} (${getMachineTypeDisplay(machineType)})`;
                } else if (machineStatus === 'R') {
                    timerModalLabel.innerText = `Machine ${machineNumber} (${getMachineTypeDisplay(machineType)}) is already running`;
                } else if (machineStatus === 'D') {
                    timerModalLabel.innerText = `Machine ${machineNumber} (${getMachineTypeDisplay(machineType)}) is defect`;
                } else if (machineStatus === 'B') {
                    timerModalLabel.innerText = `Machine ${machineNumber} (${getMachineTypeDisplay(machineType)}) is blinking`;
                } else if (machineStatus === 'U') {
                    timerModalLabel.innerText = `Machine ${machineNumber} (${getMachineTypeDisplay(machineType)}) is unknown`;
                } else {
                    timerModalLabel.innerText = `Machine ${machineNumber} (${getMachineTypeDisplay(machineType)})`;
                }
            }

            const defectBadge = document.getElementById('defectBadge');
            if (defectBadge) {
                defectBadge.style.display = machineStatus === 'D' ? 'block' : 'none';

                if (machineStatus === 'D') {
                    defectBadge.innerText = machineNotes === null || machineNotes === '' ? 'Defect: no notes' : `Defect: ${machineNotes}`;
                }
            }

            const defectLink = document.getElementById('defectLink');
            const isDefectNote = document.getElementById('isDefectNote');
            const isDefectNoteLabel = document.getElementById('isDefectNoteLabel');
            if (defectLink && isDefectNote && isDefectNoteLabel) {
                if (machineStatus === 'D') {
                    defectLink.innerText = `Mark ${getMachineTypeDisplay(machineType)} as repaired`;
                    defectLink.style.color = 'green';

                    // hide defect note
                    isDefectNote.style.display = 'none';
                    isDefectNoteLabel.style.display = 'none';
                } else if (machineStatus === 'B') {
                    defectLink.innerText = `Mark ${getMachineTypeDisplay(machineType)} as not blinking`;
                    defectLink.style.color = 'green';

                    // hide defect note
                    isDefectNote.style.display = 'none';
                    isDefectNoteLabel.style.display = 'none';
                } else {
                    defectLink.innerText = `${getMachineTypeDisplay(machineType)} is defect?`;
                    defectLink.style.color = 'red';

                    // show defect note
                    isDefectNote.style.display = 'block';
                    isDefectNoteLabel.style.display = 'block';
                }
            }

            const modalBodyInput = document.getElementById('machineId');
            if (modalBodyInput) {
                modalBodyInput.value = machineId;
            }

            // Set defect button visibility
            if (machineStatus === 'D') {
                document.getElementById('setDefectBtn').style.display = 'none';
                document.getElementById('repairBtn').style.display = 'block';
                document.getElementById('isBlinkingBtn').innerText = 'Mark as blinking';
            } else if (machineStatus === 'B') {
                document.getElementById('setDefectBtn').style.display = 'none';
                document.getElementById('repairBtn').style.display = 'none';
                document.getElementById('isBlinkingBtn').innerText = 'Mark as available';
            } else {
                document.getElementById('setDefectBtn').style.display = 'block';
                document.getElementById('repairBtn').style.display = 'none';
                document.getElementById('isBlinkingBtn').innerText = 'Machine is blinking';
            }

            const timerDuration = document.getElementById('timerDuration');
            const submitButton = document.querySelector('.btn-primary');

            timerDuration.value = 1;

            // Set notes from machine
            const notes = button.getAttribute('data-machine-notes');
            if (notes && notes !== '') {
                document.getElementById('isDefectNote').value = notes;
            } else {
                document.getElementById('isDefectNote').value = null;
            }

            if (machineStatus === 'A' || machineStatus === 'F') {
                timerDuration.disabled = false;
                submitButton.disabled = false;
            } else {
                timerDuration.disabled = true;
                submitButton.disabled = true;
            }
        });
    }

    const timerForm = document.getElementById('timerForm');
    if (timerForm) {
        timerForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const form = event.target;
            const timerModal = document.getElementById('timerModal');
            const machineId = document.getElementById('machineId').value;
            const timerDuration = document.getElementById('timerDuration').value;

            const formData = new FormData();
            formData.append('timerDuration', timerDuration);
            formData.append('machineId', machineId);

            fetch(`/${buildingId}/laundry/${machineId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateMachineStatus();
                    const modalInstance = bootstrap.Modal.getInstance(timerModal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                } else {
                    alert('Failed to start machine');
                }
            });
        });
    }

    const setDefectBtn = document.getElementById('setDefectBtn');
    const repairBtn = document.getElementById('repairBtn');

    if (setDefectBtn) {
        setDefectBtn.addEventListener('click', function (event) {
            event.preventDefault();
            const defectForm = document.getElementById('defectForm');
            const machineId = document.getElementById('machineId').value;
            const isDefectNote = document.getElementById('isDefectNote').value;

            const formData = new FormData(defectForm);
            formData.append('machineId', machineId);
            formData.append('notes', isDefectNote);

            fetch(`/${buildingId}/laundry/${machineId}/defect/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateMachineStatus();
                    const modalInstance = bootstrap.Modal.getInstance(document.getElementById('timerModal'));
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                } else {
                    alert('Failed to set machine as defect');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    if (repairBtn) {
        repairBtn.addEventListener('click', function (event) {
            event.preventDefault();
            const machineId = document.getElementById('machineId').value;

            fetch(`/${buildingId}/laundry/${machineId}/repair/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateMachineStatus();
                    const modalInstance = bootstrap.Modal.getInstance(document.getElementById('timerModal'));
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                } else {
                    alert('Failed to repair machine');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    document.querySelectorAll('.set-available-btn').forEach(button => {
        button.addEventListener('click', function () {
            const machineId = this.getAttribute('data-machine-id');

            if (buildingId) {
                fetch(`/${buildingId}/laundry/${machineId}/available/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        updateMachineStatus();
                    } else {
                        alert('Failed to set machine as available');
                    }
                });
            } else {
                console.error('Building ID element not found');
            }
        });
    });

    document.getElementById('isBlinkingBtn').addEventListener('click', function() {
        const machineId = document.getElementById('machineId').value;
        const buildingId = document.getElementById('building_id').value;
        const csrfToken = document.getElementById('csrfToken').value;

        fetch(`/${buildingId}/laundry/${machineId}/blinking/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ machine_id: machineId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateMachineStatus();
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('timerModal'));
                if (modalInstance) {
                    modalInstance.hide();
                }
            } else {
                console.error('Failed to set machine as blinking');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('defectLink').addEventListener('click', function(event) {
        event.preventDefault();
        const form = document.getElementById('defectForm');
        if (form.style.display === 'none') {
            form.style.display = 'block';
        } else {
            form.style.display = 'none';
        }
    });

    function updateMachineStatus() {
        fetch(`/${buildingId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            data.machines.forEach(machine => {
                document.getElementById(`header-${machine.identifier}`).innerText = `${machine.name} (${machine.machine_type_display})`;

                document.getElementById(`mark-as-available-${machine.identifier}`).style.display = machine.machine_status === 'F' ? 'block' : 'none';

                // Update machine button style and content
                const innerButtonText = document.getElementById(`inner-button-text-${machine.identifier}`);

                // Update remaining time
                if (machine.machine_status === 'R') {
                    innerButtonText.innerHTML = `${machine.remaining_time} min`;
                } else {
                    innerButtonText.innerHTML = getMachineIcon(machine.machine_status);
                }

                // Update machine button class
                const machineButton = document.getElementById(`button-${machine.identifier}`);
                if (machineButton) {
                    machineButton.classList.remove('A', 'R', 'F', 'D', 'B', 'U');
                    machineButton.classList.add(machine.machine_status);
                    machineButton.setAttribute('data-machine-status', machine.machine_status);
                    machineButton.setAttribute('data-machine-notes', machine.notes);
                    machineButton.title = getMachineTitle(machine.machine_status, machine.notes);
                } else {
                    console.error(`Element with ID machine-${machine.identifier} not found`);
                }

                // border color
                const machineHeader = document.getElementById(`header-${machine.identifier}`);
                if (machineHeader) {
                    machineHeader.classList.remove('R', 'F', 'D', 'B', 'U');
                    machineHeader.classList.add(machine.machine_status);
                } else {
                    console.error(`Element with ID header-${machine.identifier} not found`);
                }

                // Update machine status label
                document.getElementById(`status-${machine.identifier}`).innerHTML = getStatusBadge(machine.machine_status);

                // Update end time label
                const endTimeText = getEndTimeText(machine.machine_status, machine.end_time);
                document.getElementById(`end-time-${machine.identifier}`).innerHTML = `<i>${endTimeText}</i>`;
            });
        })
        .catch(error => console.error('Error:', error));
    }

    // Helper function to get the machine type display
    function getMachineTypeDisplay(type) {
        if (type === 'W') return 'washer';
        if (type === 'D') return 'dryer';
        return '';
    }

    // Helper function to get the appropriate icon for machine status
    function getMachineIcon(status) {
        if (status === 'A') return 'click here';
        if (status === 'F') return 'done';
        if (status === 'D') return 'defect';
        if (status === 'B') return 'blinking';
        if (status === 'U') return 'unknown';
        return '';
    }

    // Helper function to get the appropriate status badge
    function getStatusBadge(status) {
        if (status === 'A') return '<span class="badge bg-success">Available</span>';
        if (status === 'R') return '<span class="badge bg-warning">Running</span>';
        if (status === 'F') return '<span class="badge bg-primary">Finished</span>';
        if (status === 'D') return '<span class="badge bg-danger">Defect</span>';
        if (status === 'B') return '<span class="badge bg-warning">Blinking</span>';
        if (status === 'U') return '<span class="badge bg-secondary">Unknown</span>';
        return '';
    }

    // Helper function to get the end time text
    function getEndTimeText(status, endTime) {
        if (status === 'F') return `Finished at:<br>${endTime}`;
        if (status === 'R') return `End time:<br>${endTime}`;
        if (status === 'D') return `Defect since:<br>${endTime}`;
        if (status === 'B') return `Will be available soon:<br>${endTime}`;
        return `Updated at:<br>${endTime}`;
    }

    // Helper function to get the correct machine title
    function getMachineTitle(status, note) {
        if (note === null || note === undefined || note === '') note = 'No notes';

        if (status === 'A') return 'Click here to start machine';
        if (status === 'F') return 'Machine is available';
        if (status === 'D') return `Machine is defect: ${note}`;
        if (status === 'B') return 'Machine is blinking';
        if (status === 'U') return 'Machine status is unknown';
        return '';
    }

    // get notes with fetch
    function getNotes(machineId) {
        var notes = "";
        fetch(`/${buildingId}/laundry/${machineId}/notes/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            notes = data.notes;
        });
        return notes;
    }

    // Set interval to update every 5 seconds
    setInterval(updateMachineStatus, 5000);
});