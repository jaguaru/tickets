# TicketApp ticket management to upload images in the cloud

TicketApp is a REST API application built with Django. This allows users to upload images asynchronously to the cloud through ticket management.


# Firt steps:


### Dowload the repository:

Open a window console and type

    $ git clone https://github.com/jaguaru/tickets.git


## Setting up the virtual environment:

Open the tickets directory:

    $ cd tickets

Create the directory for the virtual environment:

    $ mkdir django_venv

Create the virtual environment:

    $ python3 -m venv django_venv

Activate the virtual environment:

    $ source django_venv/bin/activate

Virtual environment activated:

    (django_venv) $

Install the required packages:

    (vserver) $ pip install -r requirements.txt

Make the migration process

    $ python3 manage.py makemigrations

    $ python3 manage.py migrate

Run the Django server:

    (vserver) $ python3 manage.py runserver

In the same directory open a second window console activate another virtual environment:

    $ source django_venv/bin/activate

Run the Celery server

    (vserver) $ celery -A ticket_management worker -l info

Now that we have the Django and Celery server activated, we can use the REST API endpoints.


# Interacting with the REST API

This REST API consists of two sections, the first is for user authentication and the second is for managing tickets and uploading images to the cloud.

User Autentication

The first step is to visit this URL with Postman or another similar application to make http requests. You

    Request:

    URL: http://127.0.0.1:8000/api/auth/token/login
    Method: POST
    Body:
        {
            "email": "test_dos@outlook.com",
            "username": "test_dos",
            "password": "Jaguar12345"
        }
    
    Response:

        {
            "token": "fa24b09db3cf450a3780b0c95124aa94ea8f77d2",
            "user": {
                "id": 3,
                "username": "test_dos",
                "email": "test_dos@outlook.com"
            }
        }

    
    
    $ http://127.0.0.1:8000/api/auth/token/register
    
    $ http://127.0.0.1:8000/api/auth/token/profile

    $ http://127.0.0.1:8000/api/tickets/upload_cloud_image

    $ http://127.0.0.1:8000/api/tickets/tickets_paginated

    $ http://127.0.0.1:8000/api/tickets/check_ticket_status
    
    $ http://127.0.0.1:8000/api/tickets/ticket_details
