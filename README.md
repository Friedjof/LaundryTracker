### README.md

# LaundryTracker

LaundryTracker is a simple web application built with Django that allows users to track the availability and status of laundry machines (washers and dryers) in a building. The application features a real-time status update system where users can view whether a machine is available, running, finished, or defective. Additionally, users can set timers for machines and view the remaining time on active machines.

## Features

- Track the status of laundry machines (Available, Running, Finished, Defective).
- Real-time updates of machine statuses every 10 seconds via background server polling.
- User-friendly interface for setting timers on machines.
- Ability to mark machines as "Available" after they finish running.
- CSRF protection enabled for secure communication.

## Installation

To get started with LaundryTracker, follow the steps below to set up the project on your local machine.

### Requirements

- Python 3.x
- Django 3.x or higher
- Redis (if using Celery for background tasks)

### Setup

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
   python manage.py process_tasks
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`.

## Docker

To set up and run the LaundryTracker application using Docker and Docker Compose, follow these steps:

### Environment Variables

Create a `.env` file in the root directory of your project with the following content:
```env
DJANGO_SECRET_KEY=<random-django-secret-string>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,your-domain.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=<admin-email>
DJANGO_SUPERUSER_PASSWORD=<admin-password>
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

### 1. **GET `/building/<str:building>/`**
   - **Description**: Retrieves the laundry machine status for a specific building and renders the web page.
   - **Method**: `GET`
   - **Parameters**:
     - `building`: The code for the building.
   - **Response**: HTML page with machine statuses.

### 2. **POST `/building/<str:building>/`**
   - **Description**: Fetches the latest machine statuses for the specified building in JSON format. This is used for real-time updates on the frontend.
   - **Method**: `POST`
   - **Parameters**:
     - `building`: The code for the building.
   - **Response**: JSON containing updated machine statuses.

### 3. **POST `/building/<str:building>/laundry/<int:machine_id>/`**
   - **Description**: Sets a timer for a specific machine (washer or dryer) in the given building.
   - **Method**: `POST`
   - **Parameters**:
     - `building`: The code for the building.
     - `machine_id`: The ID of the machine.
   - **Request Body**: 
     - `timerDuration`: The duration (in minutes) to set the timer.
   - **Response**: Success or failure message in JSON format.

### 4. **POST `/building/<str:building>/laundry/<int:machine_id>/available/`**
   - **Description**: Marks a specific machine as available after it has finished running.
   - **Method**: `POST`
   - **Parameters**:
     - `building`: The code for the building.
     - `machine_id`: The ID of the machine.
   - **Response**: Success or failure message in JSON format.

### 5. **GET `/building/<str:building>/laundry/<int:machine_id>/notes/`**
   - **Description**: Retrieves any notes or comments associated with the specified machine.
   - **Method**: `GET`
   - **Parameters**:
     - `building`: The code for the building.
     - `machine_id`: The ID of the machine.
   - **Response**: JSON containing machine notes.

### 6. **POST `/building/<str:building>/laundry/<int:machine_id>/defect/`**
   - **Description**: Marks a machine as defective if it is broken or malfunctioning.
   - **Method**: `POST`
   - **Parameters**:
     - `building`: The code for the building.
     - `machine_id`: The ID of the machine.
   - **Response**: Success or failure message in JSON format.

### 7. **POST `/building/<str:building>/laundry/<int:machine_id>/repair/`**
   - **Description**: Marks a machine as repaired after it has been fixed.
   - **Method**: `POST`
   - **Parameters**:
     - `building`: The code for the building.
     - `machine_id`: The ID of the machine.
   - **Response**: Success or failure message in JSON format.

## Configuration

- The building codes and machine configurations can be updated in the database.
- You can configure the update interval and other settings in the JavaScript files and Django views.

## Contributing

Contributions to LaundryTracker are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

If you have any questions or feedback, feel free to contact us at [programming@noweck.info](mailto:programming@noweck.info).
