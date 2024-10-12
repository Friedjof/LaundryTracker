# LaundryTracker

LaundryTracker is a simple web application built with Django that allows users to track the availability and status of laundry machines (washers and dryers) in a building. The application features a real-time status update system where users can view whether a machine is available, running, finished, or defective. Additionally, users can set timers for machines and view the remaining time on active machines.

## Features

- Track the status of laundry machines (Available, Running, Finished, Defective).
- Real-time updates of machine statuses every 10 seconds via background server polling.
- User-friendly interface for setting timers on machines.
- Ability to mark machines as "Available" after they finish running.
- CSRF protection enabled for secure communication.

## Screenshots
![demo-home](/static/media/demo-home.png)
![demo-done](/static/media/demo-done.png)
![demo-report-defect](/static/media/demo-report-defect.png)

## Installation

To get started with LaundryTracker, follow the steps below to set up the project on your local machine.

### Requirements

- Python 3.x
- Django 3.x or higher
- Redis (if using Celery for background tasks)

### Setup development environment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd laundrytracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Run background tasks:**
   ```bash
   python manage.py simulate_cron --interval 10
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`.

## Docker

To set up and run the LaundryTracker application using Docker and Docker Compose, follow these steps:

### Environment Variables

Create a `.env` file in the root directory of your project with the following content:
```env
DJANGO_SECRET_KEY='<random-django-secret-string>' # generate a random string for the secret key
DJANGO_DEBUG='False'                              # set to 'True' for development
DJANGO_ALLOWED_HOSTS='your-domain.com,localhost'  # this first should be your main domain, multiple domains should be separated by commas
DJANGO_SUPERUSER_USERNAME='admin'                 # this is the default superuser username
DJANGO_SUPERUSER_EMAIL='<admin-email>'            # this is the default superuser email
DJANGO_SUPERUSER_PASSWORD='<admin-password>'      # this is the default superuser password
TLS_ACTIVE='True'                                 # set to 'False' if you don't want to use HTTPS
```

### Build and Run the Docker Container

1. **Build the Docker container**:
    ```bash
    docker-compose build
    ```

2. **Run the Docker container in detached mode**:
    ```bash
    docker-compose up -d
    ```

This will start the LaundryTracker application and make it accessible at `http://localhost:8000`.

## Usage

> Acces the admin panel at `http://<your-domain>/admin/` and log in with the superuser credentials you created.
> You can add buildings, machines, and notes in the admin panel.

Once the server is running, you can navigate to the home page, select your building, and view the status of each machine. 

- If a machine is **running**, you will see the remaining time displayed.
- If a machine is **finished**, you can mark it as **Available** and set a new timer.
- The application updates the machine status every 10 seconds to reflect real-time changes.

## API Endpoints
> Coming soon…

## Configuration

- The building codes and machine configurations can be updated in the database.
- You can configure the update interval and other settings in the JavaScript files and Django views.

## Contributing

Contributions to LaundryTracker are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

If you have any questions or feedback, feel free to contact us at [programming@noweck.info](mailto:programming@noweck.info).
