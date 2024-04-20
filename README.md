# TicketApp ticket management to upload images in the cloud

TicketApp is a REST API application built with Django. This allows users to upload images asynchronously to the cloud, through ticket management, using the Cloudinary service. The transaction data, Tickets and Images uploaded, are saved in PostgreSQL.


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

    (django_venv) $ pip install -r requirements.txt

Run the Django server:

    (django_venv) $ python3 manage.py runserver

In the same directory open a second window console activate another virtual environment:

    $ source django_venv/bin/activate

Run the Celery server

    (django_venv) $ celery -A ticket_management worker -l info

Now that we have the Django and Celery server activated, we can use the REST API endpoints.


# Interacting with the REST API

This REST API consists of two sections, the first is for user authentication and the second is for managing tickets and uploading images to the cloud.

The first step is to get an app like Postman or another similar application to make local and remote http requests.



    Request:

    URL: http://127.0.0.1:8000/api/auth/token/register
    Method: POST
    Body:

        {
            "username": "test_dos",
            "password": "Jaguar12345",
            "email": "test_dos@outlook.com"
        }

    Response:

        {
            "token": "ad5b5c5086e5b64d55e35650f769370991b87c9f",
            "user": {
                "id": 1375,
                "username": "test_dos",
                "email": "test_dos@outlook.com",
                "password": "asdfasdfasdfadf"
            }
        }


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

    

    



    Request: http://127.0.0.1:8000/api/auth/token/profile

    URL: 
    Method: POST
    Body:

    Response
    
    
    
    
    Request: http://127.0.0.1:8000/api/tickets/upload_cloud_image

    URL: 
    Method: POST
    Body:

    Response
    
    

    
    Request: http://127.0.0.1:8000/api/tickets/tickets_paginated

    URL: 
    Method: POST
    Body:

    Response
    
    
    

    Request: http://127.0.0.1:8000/api/tickets/check_ticket_status

    URL: 
    Method: POST
    Body:

    Response




    Request: http://127.0.0.1:8000/api/tickets/ticket_details

    URL: 
    Method: POST
    Body:

    Response

    

    

    
    
    
