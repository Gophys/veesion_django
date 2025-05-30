# Veesion Notificaiton alert Django App

## Overview

This application is not ment to be put in production.
It shows an example on how to develop a django rest app to allow a third service to send alerts that are then dispatched according to user preferences

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/veesion.git
    cd veesion
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate     
    ```

5. **Run unit tests**

    ```bash
    python manage.py test alerts/tests
    ```

6. **Run the app**

    ```bash
    python manage.py runserver
    ```

## Basic Usage

Once the app deployed, go to <http://127.0.0.1:8000/> (or the appropriate URL if you updated the configuration) and you will see the availables api endpoints.
The debug mode is still activated for test and practical purposes, but should not be activated to production mode.

The following api endpoints are available:

- users : To create and list created users
- stores : To create and list created stores
- subscriptions : to create and list user subscriptions to alerts
- notifications : to list sent (and not sucessfully sent) notifications
- alerts : to list the received alerts
- webhooks/alerts: the purpose of this project, and enpoint to receive the alerts, treat them, and dispatch them according to user subscriptions

## Limitations

This project is limited in functionnalities, there is no security implemented, not authenticity, no possibility to remove or update informations for a user or its subscriptions as they are out of the scope for a 4h project.

Some views are create for the sole purpose of easy access to insert the data. The sqlite database is also used for simplicity of installation and testing purpose. The dependencies are stored in the requirements.txt file for simplicity sake.
In a real project, and without worrying to make the recipent of this project to install other software or dependecy, a dockerfile would have been provided, and the dependency management would have been set in a pixi, uv or poetry system.

Sending an alert can be slow, depending on the availability of the service (if no service, it can be really slow to have a response from the api), but this issue was not addressed yet, it can be discussed.
