document.addEventListener('DOMContentLoaded', function () {
    const buildingId = document.getElementById('building_id').value;
    const csrfToken = document.getElementById('csrfToken').value;

    const timerModal = document.getElementById('timerModal');
    if (timerModal) {
        timerModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const machineId = button.getAttribute('data-machine-id');
            const machineStatus = button.getAttribute('data-machine-status');

            const modalBodyInput = document.getElementById('machineId');
            if (modalBodyInput) {
                modalBodyInput.value = machineId;
            }

            // Set defect button visibility
            if (machineStatus === 'D') {
                document.getElementById('setDefectBtn').style.display = 'none';
                document.getElementById('repairBtn').style.display = 'block';
            } else {
                document.getElementById('setDefectBtn').style.display = 'block';
                document.getElementById('repairBtn').style.display = 'none';
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
            const buildingElement = document.getElementById('building_id');
            const csrfToken = document.getElementById('csrfToken').value;

            if (buildingElement) {
                const building = buildingElement.value;

                const formData = new FormData();
                formData.append('timerDuration', timerDuration);
                formData.append('machineId', machineId);

                fetch(`/building/${building}/laundry/${machineId}/`, {
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
            } else {
                console.error('Building ID element not found');
            }
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

            fetch(`/building/${buildingId}/laundry/${machineId}/defect/`, {
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

            fetch(`/building/${buildingId}/laundry/${machineId}/repair/`, {
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
                fetch(`/building/${buildingId}/laundry/${machineId}/available/`, {
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
        fetch(`/building/${buildingId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            data.machines.forEach(machine => {
                document.getElementById(`header-${machine.identifier}`).innerText = `${machine.number} (${machine.machine_type_display})`;

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
                    machineButton.classList.remove('off', 'running', 'on', 'defect');
                    machineButton.classList.add(getMachineClass(machine.machine_status));
                    machineButton.setAttribute('data-machine-status', machine.machine_status);
                    machineButton.setAttribute('data-machine-notes', machine.notes);
                    machineButton.title = getMachineTitle(machine.machine_status, machine.notes);
                } else {
                    console.error(`Element with ID machine-${machine.identifier} not found`);
                }

                // border color
                const machineHeader = document.getElementById(`header-${machine.identifier}`);
                if (machineHeader) {
                    machineHeader.classList.remove('border-success', 'border-warning', 'border-primary', 'border-danger');
                    machineHeader.classList.add(getMachineClass(machine.machine_status));
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

    // Helper function to get the CSS class for machine status
    function getMachineClass(status) {
        if (status === 'A') return 'off';
        if (status === 'R') return 'running';
        if (status === 'F') return 'on';
        if (status === 'D') return 'defect';
        return '';
    }

    // Helper function to get the appropriate icon for machine status
    function getMachineIcon(status) {
        if (status === 'A') return 'click here';
        if (status === 'F') return 'done';
        if (status === 'D') return 'defect';
        return '';
    }

    // Helper function to get the appropriate status badge
    function getStatusBadge(status) {
        if (status === 'A') return '<span class="badge bg-success">Available</span>';
        if (status === 'R') return '<span class="badge bg-warning">Running</span>';
        if (status === 'F') return '<span class="badge bg-primary">Finished</span>';
        if (status === 'D') return '<span class="badge bg-danger">Defect</span>';
        return '';
    }

    // Helper function to get the end time or last used text
    function getEndTimeText(status, endTime) {
        if (status === 'F') return `Finished at: ${endTime}`;
        if (status === 'R') return `End time: ${endTime}`;
        return `Last used: ${endTime}`;
    }

    // Helper function to get the correct machine title
    function getMachineTitle(status, note) {
        if (note === null || note === undefined || note === '') note = 'No notes';

        if (status === 'A') return 'Click here to start machine';
        if (status === 'F') return 'Machine is available';
        if (status === 'D') return `Machine is defect: ${note}`;
        return '';
    }

    // get notes with fetch
    function getNotes(machineId) {
        var notes = "";
        fetch(`/building/${buildingId}/laundry/${machineId}/notes/`, {
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