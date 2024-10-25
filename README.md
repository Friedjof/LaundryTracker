# LaundryTracker

**LaundryTracker** is a solution for monitoring washing machines and dryers in communal laundry rooms, commonly found in shared living spaces or dormitories.
Users themselves collect the data by setting timers for the machines or reporting defects.
This allows other users to see in real-time which machines are available or out of order.
Additionally, it helps the property management quickly identify defective machines and arrange for repairs efficiently.

> **Note:** The quality of the displayed data depends on user input. Reliable usage can only be ensured through accurate and up-to-date information.

> This project is still in development and may include bugs or incomplete features. Feel free to contribute to the project by submitting a pull request.

## Features

- **Timers** can be set by users when they start using a machine.
- **Defective machines** can be marked as defective or temporarily defective, with a short note.
- **Admin panel** allows configuration of the app.
- **Special links** are required for users to control machines, helping to prevent unauthorized use.
- **Analytics dashboard** provides administrators with detailed usage insights. All changes are logged and visualized in charts.
- **Telegram bot** can be set up via the admin panel. It sends various events to configured Telegram channels and notifies users via push notifications (optional).
- **Moderators** can be assigned via the admin panel to manage individual laundry rooms (in development).

## Demo Screenshots

<table>
  <tr>
    <td><img src="/media/demo-home.png" alt="demo-home" /></td>
    <td><img src="/media/demo-machines.png" alt="demo-machines" /></td>
    <td><img src="/media/demo-analytics-1.png" alt="demo-analytics-1" /></td>
  </tr>
  <tr>
    <td><img src="/media/demo-404.png" alt="demo-404" /></td>
    <td><img src="/media/demo-timer-modal-defect.png" alt="demo-report-defect" /></td>
    <td><img src="/media/demo-admin-panel.png" alt="demo-admin-panel" /></td>
  </tr>
</table>

## Installation
```bash
git clone https://github.com/Friedjof/LaundryTracker.git
```
The project can be started in two ways:
- **For development**, the project can be started as usual with Django.
- Alternatively, you can build the project as a **Docker container** or use the existing Docker image from this repository.

### Development
1. Create a virtual Python environment and activate it: `python -m venv venv && source venv/bin/activate`
2. Install the dependencies: `pip install -r requirements.txt`
3. Migrate the database: `python manage.py migrate`
4. Start Django: `python manage.py runserver`
5. To update the database entries in the background, run the following command: `python manage.py simulate_cron --interval 60`

### Production
1. Build the Docker image: `docker compose build --no-cache`
2. Create a `.env` file with the following content:
   ```env
   DJANGO_SECRET_KEY='<random-django-secret-string>' # generate a random string for the secret key
   DJANGO_DEBUG='False'                              # set to 'True' for development
   DJANGO_ALLOWED_HOSTS='your-domain.com,localhost'  # the first should be your main domain, multiple domains should be separated by commas
   DJANGO_SUPERUSER_USERNAME='admin'                 # this is the default superuser username
   DJANGO_SUPERUSER_EMAIL='<admin-email>'            # this is the default superuser email
   DJANGO_SUPERUSER_PASSWORD='<admin-password>'      # this is the default superuser password
   TLS_ACTIVE='True'                                 # set to 'False' if you don't want to use HTTPS
   ```
3. Start the Docker container: `docker compose up -d`

Now you can access the LaundryTracker application on port `8000` with your configured domain.

## The Makefile
The project includes a `Makefile` with various commands to simplify development and deployment. You can run the following commands:
- Django commands:
  - `make migrations`: Create the database migrations.
  - `make migrate`: Apply the database migrations.
  - `make admin`: Create a superuser for the Django admin panel.
  - `make shell`: Start the Django shell.
- Docker commands:
  - `make build`: Build the Docker image.
  - `make up`: Start the Docker container.
  - `make down`: Stop the Docker container.
  - `make logs`: Show the Docker container logs.
  - `make restart`: Restart the Docker container.
  - `make clean`: Remove the Docker container and image.
- Python commands:
  - `make requirements`: Freeze the current dependencies to the `requirements.txt` file.
- Deployment commands:
  - `make release`: Saves the version tag in the `version.txt` file, commits it, and pushes it to the repository.
  - After pushing tags to the repository (e.g. like `v1.0.0`), the GitHub Actions workflow will automatically build and push the Docker image to the GitHub Container Registry.

## Usage

> Access the admin panel at `http(s)://<your-domain>/admin/` and log in with the superuser credentials you created.
> You can add buildings, machines, and notes in the admin panel.

![admin-panel](/media/demo-admin-panel.png)

### Machine Status
- **Available**: The machine is available for use.
- **Running**: The machine is currently in use.
- **Finished**: The machine has finished its cycle.
- **Defective**: The machine is defective and cannot be used.
- **Blinking**: The machine is blinking, indicating a temporary defect (will automatically switch back to 'Available' after 8 hours).
- **Unknown**: The machine status is unknown (currently not in use).

## API Endpoints

- **`/<uuid:building>/`**: Displays an overview of the selected building.
- **`/<uuid:building>/laundry/<uuid:machine_id>/`**: Allows users to set a timer for the specified machine.
- **`/<uuid:building>/laundry/<uuid:machine_id>/available/`**: Returns the availability status of the machine.
- **`/<uuid:building>/laundry/<uuid:machine_id>/notes/`**: Retrieves notes associated with the specified machine.
- **`/<uuid:building>/laundry/<uuid:machine_id>/defect/`**: Marks the machine as defective.
- **`/<uuid:building>/laundry/<uuid:machine_id>/repair/`**: Marks the machine as repaired after maintenance.
- **`/<uuid:building>/laundry/<uuid:machine_id>/blinking/`**: Controls the blinking indicator for the machine to signal specific states.
- **`/404`**: Handles invalid requests by returning a 404 error page.
- **`/`**: The homepage of the application.

## Contributing

Contributions to LaundryTracker are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the GNU (General Public License) v3.0. See the [`LICENSE`](LICENSE) file for more information.

---

If you have any questions or feedback, feel free to contact us at [programming@noweck.info](mailto:programming@noweck.info).
