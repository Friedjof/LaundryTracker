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
                isBlinkingBtn.innerText = 'Mark as blinking';
            } else {
                repairBtn.style.display = 'none';
                isBlinkingBtn.innerText = `Mark as available`;
            }
        } else {
            modalNote.innerText = '';

            isBlinkingBtn.innerText = 'Mark as blinking';

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
    document.getElementById('modal-defect-link').addEventListener('click', function (event) {
        event.preventDefault();

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
                showNotification('Machine started', 'success', 'info');
            } else {
                showNotification('Failed to start machine', 'danger', 'error');
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
                showNotification('Machine set as defect', 'success', 'info');
            } else {
                showNotification('Failed to set machine as defect', 'danger', 'error');
            }
        })
        .catch(error => showNotification('Failed to set machine as defect', 'danger', 'error'));
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
                showNotification('Machine repaired', 'success', 'info');
            } else {
                showNotification('Failed to repair machine', 'danger', 'error');
            }
        })
        .catch(error => showNotification('Failed to repair machine', 'danger', 'error'));
    });

    // blink machine button logic
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
                showNotification('Machine set as blinking', 'success', 'info');
            } else {
                showNotification('Failed to set machine as blinking', 'danger', 'error');
            }
        })
        .catch(error => {
            showNotification('Failed to set machine as blinking', 'danger', 'error');
        });
    });

    // machine button logic
    Array.from(document.getElementsByClassName('machine-btn')).forEach(function (button) {
        button.addEventListener('click', function () {
            const identifier = button.getAttribute('data-machine-identifier');
            const hiddenBtn = document.getElementById(`machine-btn-hidden_${identifier}`);

            if (hiddenBtn.getAttribute('data-machine-status') === 'Finished') {
                fetch(`/${buildingIdentifier}/laundry/${identifier}/available/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        update();
                    } else {
                        showNotification('Failed to set machine as available', 'danger', 'error');
                    }
                });
            } else {
                hiddenBtn.click();
            }
        });
    });

    // update logic
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

        const specialSymboleDefect = document.getElementById(`special-symbole-defect_${identifier}`);
        const specialSymboleRunning = document.getElementById(`special-symbole-running_${identifier}`);
        const specialSymboleBlinking = document.getElementById(`special-symbole-blinking_${identifier}`);
        const specialSymboleFinished = document.getElementById(`special-symbole-finished_${identifier}`);
        const specialSymboleAvailable = document.getElementById(`special-symbole-available_${identifier}`);

        if (data.status === 'Defect') {
            specialSymboleDefect.style.display = 'inline';
            specialSymboleRunning.style.display = 'none';
            specialSymboleBlinking.style.display = 'none';
            specialSymboleFinished.style.display = 'none';
            specialSymboleAvailable.style.display = 'none';
        } else if (data.status === 'Running') {
            specialSymboleDefect.style.display = 'none';
            specialSymboleRunning.style.display = 'inline';
            specialSymboleBlinking.style.display = 'none';
            specialSymboleFinished.style.display = 'none';
            specialSymboleAvailable.style.display = 'none';
        } else if (data.status === 'Blinking') {
            specialSymboleDefect.style.display = 'none';
            specialSymboleRunning.style.display = 'none';
            specialSymboleBlinking.style.display = 'inline';
            specialSymboleFinished.style.display = 'none';
            specialSymboleAvailable.style.display = 'none';
        } else if (data.status === 'Finished') {
            specialSymboleDefect.style.display = 'none';
            specialSymboleRunning.style.display = 'none';
            specialSymboleBlinking.style.display = 'none';
            specialSymboleFinished.style.display = 'inline';
            specialSymboleAvailable.style.display = 'none';
        } else if (data.status === 'Available') {
            specialSymboleDefect.style.display = 'none';
            specialSymboleRunning.style.display = 'none';
            specialSymboleBlinking.style.display = 'none';
            specialSymboleFinished.style.display = 'none';
            specialSymboleAvailable.style.display = 'inline';
        } else {
            specialSymboleDefect.style.display = 'none';
            specialSymboleRunning.style.display = 'none';
            specialSymboleBlinking.style.display = 'none';
            specialSymboleFinished.style.display = 'none';
            specialSymboleAvailable.style.display = 'none';
        }

        if (data.status !== machineStatus.innerText) {
            if (data.status === 'Available') {
                showNotification(`Machine ${data.name} (${data.type}) can now be used`, 'success', 'info', true);
            } else if (data.status === 'Finished') {
                showNotification(`Machine ${data.name} (${data.type}) has finished`, 'success', 'info', true);
            }
        }

        machineStatus.innerText = data.status;
        machineStatus.classList.remove('Available', 'Running', 'Finished', 'Defect', 'Blinking', 'Unknown');
        machineStatus.classList.add(data.status);

        machineTime.innerText = data.time;

        // update machine button attributes
        machineBtn.setAttribute('data-machine-type', data.type);
        machineBtn.setAttribute('data-machine-status', data.status);

        if (data.status === 'Finished') {
            machineBtn.innerText = `mark as available`;
        } else if (data.status === 'Running') {
            machineBtn.innerText = `is running`;
        } else if (data.status === 'Blinking' || data.status === 'Defect') {
            machineBtn.innerText = `mark as repaired`;
        } else {
            machineBtn.innerText = `start ${data.type.toLowerCase()}`;
        }

        machineBtnHidden.setAttribute('data-machine-type', data.type);
        machineBtnHidden.setAttribute('data-machine-status', data.status);
        machineBtnHidden.setAttribute('data-machine-note', data.notes);
        machineBtnHidden.setAttribute('data-machine-time', data.time);
    }

    // data donation modal
    function dataDonation(machine) {
        // show data-donation-modal
        const trigger = document.getElementById('data-donation-btn');

        const dataDonationTitle = document.getElementById('data-donation-modal-label');
        const dataDonationMachine = document.getElementById('data-donation-machine');

        // dropdown buttons
        const dataDonationFinished = document.getElementById('data-donation-finished');
        const dataDonationRunning = document.getElementById('data-donation-running');
        const dataDonationBlinking = document.getElementById('data-donation-blinking');
        const dataDonationDefect = document.getElementById('data-donation-defect');
        const unchangedBtn = document.getElementById('data-donation-close');

        // set attributes
        dataDonationFinished.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationFinished.setAttribute('data-machine-status', 'Finished');
        dataDonationRunning.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationRunning.setAttribute('data-machine-status', 'Running');
        dataDonationBlinking.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationBlinking.setAttribute('data-machine-status', 'Blinking');
        dataDonationDefect.setAttribute('data-machine-identifier', machine.identifier);
        dataDonationDefect.setAttribute('data-machine-status', 'Defect');
        unchangedBtn.setAttribute('data-machine-identifier', machine.identifier);

        if (machine.status === 'Available') {
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Running') {
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'none';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Finished') {
            dataDonationFinished.style.display = 'none';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Blinking') {
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'none';
            dataDonationDefect.style.display = 'block';
        } else if (machine.status === 'Defect') {
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'none';
        } else {
            dataDonationFinished.style.display = 'block';
            dataDonationRunning.style.display = 'block';
            dataDonationBlinking.style.display = 'block';
            dataDonationDefect.style.display = 'block';
        }

        // set text
        dataDonationTitle.innerText = `Your data donation for ${machine.name} (${machine.type})`;
        dataDonationMachine.innerText = `${machine.name} (${machine.type}), not updated since ${machine.time}`;

        // open modal
        trigger.click();
    }

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
                    showNotification('Thank you for your data donation :)', 'success', 'info');
                } else {
                    showNotification('Failed to set machine as finished', 'danger', 'error');
                }
            });

        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('data-donation-modal'));
        if (modalInstance) {
            modalInstance.hide();
        }
    });

    document.getElementById('data-donation-running').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        const machineBtn = document.getElementById(`machine-btn_${machineIdentifier}`);

        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('data-donation-modal'));
        if (modalInstance) {
            modalInstance.hide();
        }

        machineBtn.click();

        showNotification('Thank you for your data donation :)', 'success', 'info');
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
                    showNotification('Thank you for your data donation :)', 'success', 'info');
                } else {
                    showNotification('Failed to set machine as blinking', 'danger', 'error');
                }
            });

        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('data-donation-modal'));
        if (modalInstance) {
            modalInstance.hide();
        }
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
                    showNotification('Thank you for your data donation :)', 'success', 'info');
                } else {
                    showNotification('Failed to set machine as defect', 'danger', 'error');
                }
            });

        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('data-donation-modal'));
        if (modalInstance) {
            modalInstance.hide();
        }
    });

    document.getElementById('data-donation-close').addEventListener('click', function () {
        const machineIdentifier = this.getAttribute('data-machine-identifier');

        fetch(`/${buildingIdentifier}/laundry/${machineIdentifier}/unchanged/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    update()
                    showNotification('Thank you for your data donation :)', 'success', 'info');
                } else {
                    showNotification('Failed to set machine as unchanged', 'danger', 'error');
                }
            });
    });

    update();
    // update machines every 5 seconds
    setInterval(update, 5000);
});