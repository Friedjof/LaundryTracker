document.addEventListener('DOMContentLoaded', function () {
    // CSRF token and building identifier
    const buildingIdentifier = document.getElementById('building-identifier').value;
    const csrfToken = document.getElementById('csrfToken').value;

    // machine modal
    document.getElementById('machine-modal').addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const machineIdentifier = button.getAttribute('data-machine-identifier');
        const machineName = button.getAttribute('data-machine-name');
        const machineType = button.getAttribute('data-machine-type');
        const machineStatus = button.getAttribute('data-machine-status');
        const machineNote = button.getAttribute('data-machine-note');

        const modal = this;

        const modalMachineIdentifier = document.getElementById('modal-machine-identifier');
        const modalTitle = modal.querySelector('.modal-title');
        const modalNote = document.getElementById('defect-badge');
        const modalMachineStatus = document.getElementById('modal-machine-status');
        const modalMachineDuration = document.getElementById('modal-machine-duration');
        const modalDefectForm = document.getElementById('modal-defect-form');

        modalMachineIdentifier.value = machineIdentifier;

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

    // catch form submit event
    document.getElementById('machine-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const timerModal = document.getElementById('machine-modal');
        const machineDuration = document.getElementById('modal-machine-duration').value;
        const machineIdentifier = document.getElementById('modal-machine-identifier').value;

        const formData = new FormData();
        formData.append('machineId', machineIdentifier);
        formData.append('timerDuration', machineDuration);

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const modalInstance = bootstrap.Modal.getInstance(timerModal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            } else {
                alert('Failed to start machine');
            }
        });
    });

    // machine buttons
    Array.from(document.getElementsByClassName('machine-btn')).forEach(function (button) {
        button.addEventListener('click', function () {
            const identifier = button.getAttribute('data-machine-identifier');
            // TODO: make this as a middleware for sending the available status if finished
        });
    });

    // TODO: add update machine function (pulling data from server every 5 seconds)
});