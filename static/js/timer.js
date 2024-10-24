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
        const modalMachineDurationInput = document.getElementById('modal-machine-duration');

        // elements of defect form
        const repairBtn = document.getElementById('repair-btn');
        const setDefectBtn = document.getElementById('set-defect-btn');
        const isDefectNoteInput = document.getElementById('isDefectNote');
        const isDefectNoteLabel = document.getElementById('isDefectNoteLabel');
        const modalDefectLink = document.getElementById('modal-defect-link');
        const isBlinkingBtn = document.getElementById('is-blinking-btn');

        modalMachineIdentifier.value = machineIdentifier;

        modalTitle.textContent = `${machineName} (${machineType})`;

        if (machineStatus === 'Defect' || machineStatus === 'Blinking') {
            if (machineStatus === 'Blinking') {
                modalNote.innerText = 'Machine is temporarily unavailable';
            } else if (machineNote) {
                modalNote.innerText = `Note: ${machineNote}`;
            } else {
                modalNote.innerText = 'No note';
            }

            // set link label style and text
            modalDefectLink.classList.remove('IsDefect');
            modalDefectLink.classList.add('IsWorking');

            if (machineStatus === 'Defect') {
                modalDefectLink.innerText = `Mark ${machineType.toLowerCase()} as repaired`;
            } else {
                modalDefectLink.innerText = `Mark ${machineType.toLowerCase()} as available`;
            }

            // hide defect form elements
            setDefectBtn.style.display = 'none';
            isDefectNoteInput.style.display = 'none';
            isDefectNoteLabel.style.display = 'none';

            // disable duration input
            modalMachineDurationInput.disabled = true;

            // show repair button
            if (machineStatus === 'Defect') {
                repairBtn.style.display = 'block';
            } else {
                repairBtn.style.display = 'none';
                isBlinkingBtn.style.display = 'block';
                isBlinkingBtn.innerText = `Mark as available`;
            }
        } else {
            modalNote.innerText = '';

            // set link label style and text
            modalDefectLink.classList.remove('IsWorking');
            modalDefectLink.classList.add('IsDefect');
            modalDefectLink.innerText = `${machineType} is defect?`;

            // show defect form elements
            setDefectBtn.style.display = 'block';
            isDefectNoteInput.style.display = 'block';
            isDefectNoteLabel.style.display = 'block';

            // hide repair button
            repairBtn.style.display = 'none';

            // enable duration input
            modalMachineDurationInput.disabled = machineStatus === 'Running';

            // reset defect note input
            isDefectNoteInput.value = '';
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
        formData.append('will_ask_for_data_donation', 'true');

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
                update();

                if (data.ask_for) {
                    dataDonation(data.ask_for);
                }
            } else {
                alert('Failed to start machine');
            }
        });
    });

    // defect form button click set-defect-btn
    document.getElementById('set-defect-btn').addEventListener('click', function () {
        const defectForm = document.getElementById('modal-defect-form');
        const machineIdentifier = document.getElementById('modal-machine-identifier').value;
        const isDefectNote = document.getElementById('isDefectNote').value;

        const formData = new FormData(defectForm);
        formData.append('notes', isDefectNote);

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/defect/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('machine-modal'));
                if (modalInstance) {
                    modalInstance.hide();
                }
                update();
            } else {
                alert('Failed to set machine as defect');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('repair-btn').addEventListener('click', function () {
        const machineIdentifier = document.getElementById('modal-machine-identifier').value;

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/repair/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                update()
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('machine-modal'));
                if (modalInstance) {
                    modalInstance.hide();
                }
            } else {
                alert('Failed to repair machine');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // blink machine button
    document.getElementById('is-blinking-btn').addEventListener('click', function () {
        const machineIdentifier = document.getElementById('modal-machine-identifier').value;

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/blinking/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ machine_id: machineIdentifier })})
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                update();
                const modalInstance = bootstrap.Modal.getInstance(document.getElementById('machine-modal'));
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

    // machine buttons
    Array.from(document.getElementsByClassName('machine-btn')).forEach(function (button) {
        button.addEventListener('click', function () {
            const identifier = button.getAttribute('data-machine-identifier');
            //const status = button.getAttribute('data-machine-status');
            //const type = button.getAttribute('data-machine-type');

            const hiddenBtn = document.getElementById(`machine-btn-hidden_${identifier}`);

            hiddenBtn.click();
        });
    });

    function update() {
        fetch(`/${buildingIdentifier}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        }).then(
            response => response.json()
        ).then(
            data => {
                data.machines.forEach(function (machine) {
                    update_machine(machine.identifier, machine);
                });
            }
        )
    }

    function update_machine(identifier, data) {
        const machineStatus = document.getElementById(`machine-status_${identifier}`);
        const machineTime = document.getElementById(`machine-time_${identifier}`);
        const machineBtn = document.getElementById(`machine-btn_${identifier}`);
        const machineBtnHidden = document.getElementById(`machine-btn-hidden_${identifier}`);

        machineStatus.innerText = data.status;
        machineStatus.classList.remove('Available', 'Running', 'Finished', 'Defect', 'Blinking', 'Unknown');
        machineStatus.classList.add(data.status);

        machineTime.innerText = data.time;

        // update machine button attributes
        machineBtn.setAttribute('data-machine-type', data.type);
        machineBtn.setAttribute('data-machine-status', data.status);

        machineBtnHidden.setAttribute('data-machine-type', data.type);
        machineBtnHidden.setAttribute('data-machine-status', data.status);
        machineBtnHidden.setAttribute('data-machine-note', data.notes);
        machineBtnHidden.setAttribute('data-machine-time', data.time);
    }

    function dataDonation(machine) {
        // show data-donation-modal
        const trigger = document.getElementById('data-donation-btn');

        const dataDonationTitle = document.getElementById('data-donation-modal-label');
        const dataDonationMachine = document.getElementById('data-donation-machine');

        // dropdown buttons
        const dataDonationAvailable = document.getElementById('data-donation-available');
        const dataDonationFinished = document.getElementById('data-donation-finished');
        const dataDonationRunning = document.getElementById('data-donation-running');
        const dataDonationBlinking = document.getElementById('data-donation-blinking');
        const dataDonationDefect = document.getElementById('data-donation-defect');

        // set attributes
        dataDonationAvailable.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationAvailable.setAttribute('data-machine-status', 'Available');
        dataDonationFinished.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationFinished.setAttribute('data-machine-status', 'Finished');
        dataDonationRunning.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationRunning.setAttribute('data-machine-status', 'Running');
        dataDonationBlinking.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationBlinking.setAttribute('data-machine-status', 'Blinking');
        dataDonationDefect.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationDefect.setAttribute('data-machine-status', 'Defect');

        if (machine.status === 'Available') {
            dataDonationAvailable.style.display = 'none';
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Running') {
            dataDonationAvailable.style.display = 'block';
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'none';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Finished') {
            dataDonationAvailable.style.display = 'block';
            dataDonationFinished.style.display = 'none';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Blinking') {
            dataDonationAvailable.style.display = 'block';
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'none';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Defect') {
            dataDonationAvailable.style.display = 'block';
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'none';
        } else {
            dataDonationAvailable.style.display = 'block';
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        }

        // set text
        dataDonationTitle.innerText = `Data donation request for ${machine.name} (${machine.type})`;
        dataDonationMachine.innerText = `${machine.name} (${machine.type}), not updated since ${machine.time}`;

        // open modal
        trigger.click();

        console.log(machine);
    }

    document.getElementById('data-donation-available').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/available/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    update()
                } else {
                    alert('Failed to set machine as available');
                }
            });

        document.getElementById('data-donation-close').click();
    });

    document.getElementById('data-donation-finished').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/finished/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    update()
                } else {
                    alert('Failed to set machine as finished');
                }
            });

        document.getElementById('data-donation-close').click();
    });

    document.getElementById('data-donation-running').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        const formData = new FormData();
        formData.append('machineId', machineIdentifier);
        formData.append('timerDuration', '60');
        formData.append('will_ask_for_data_donation', 'false');

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
                update();
            } else {
                alert('Failed to start machine');
            }
        });

        document.getElementById('data-donation-close').click();
    });

    document.getElementById('data-donation-blinking').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/blinking/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    update()
                } else {
                    alert('Failed to set machine as blinking');
                }
            });

        document.getElementById('data-donation-close').click();
    });

    document.getElementById('data-donation-defect').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/defect/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    update()
                } else {
                    alert('Failed to set machine as defect');
                }
            });

        document.getElementById('data-donation-close').click();
    });


    // update machines every 5 seconds
    setInterval(update, 5000);
});