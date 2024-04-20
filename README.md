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

The first step is to get an application, such as Postman or another similar application, to make local and remote http requests and get a response.

### User Register: To interact with the application, the first thing we must do is create a user with the following data: username, password and email.

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
            "token": "fa24b09db3cf450a3780b0c95124aa94ea8f77d2",
            "user": {
                "id": 2,
                "username": "test_dos",
                "email": "test_dos@outlook.com",
                "password": "asdfasdfasdfadf"
            }
        }

### User Login: In this section we need to put the data entered in the previous step.

    Request:

    URL: http://127.0.0.1:8000/api/auth/token/login
    Method: POST
    Body:

        {
            "username": "test_dos",
            "password": "Jaguar12345",
            "email": "test_dos@outlook.com"
        }
    
    Response:

        {
            "message": "Welcome, you have logged in correctly!",
            "token": "fa24b09db3cf450a3780b0c95124aa94ea8f77d2",
            "user": {
                "id": 2,
                "username": "test_dos",
                "email": "test_dos@outlook.com"
            }
        }

### User Profile: In this section we can see our profile data in an easier to read way. You must add the generated token code in the Login and Register section and put it in the authorization header to be able to use this endpoint and all the others where indicated.

    Request:

    URL: http://127.0.0.1:8000/api/auth/token/profile
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "username": "test_dos",
            "password": "Jaguar12345",
            "email": "test_dos@outlook.com"
        }

    Response:
        {
            "message": "You are logged as test_dos. User data: ID = 2, USERNAME = test_dos, EMAIL = test_dos@outlook.com."
        }

## IMPORTANT: In order to use the Ticket creation section, you must have previously logged in and have configured the Token code.

### Create Ticket: To use this endpoint, you must indicate the number of images you want to upload. This will generate the ticket_id and status data.
    
    Request:

    URL: http://127.0.0.1:8000/api/tickets/create_ticket
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "num_images": 7
        }

    Response

        {
            "ticket_id": 7,
            "status": "pending"
        }

### Upload Cloud Image: To use this endpoint, you must enter the ticket_id generated in the previous section and upload the images in base64 with the format indicated in the request instructions. The number of images to upload must match the number requested. *You can only see this section if you are the creator of the ticket.

    Request:

    URL: http://127.0.0.1:8000/api/tickets/upload_cloud_image
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "ticket_id": 7,
            "images": [
                        {  
                            "image_base64": "<base_64 image>"
                        },
                        {  
                            "image_base64": "<base_64 image>"
                        }
                      ] 
        }

    Response:
        
        {
            "message": "Las imagenes se subieron correctamente!"
        }
    
### Ticket Paginated: To use this endpoint, you must enter the ticket_id in the format indicated in the request instructions. In this case you can indicate a date range in "start_date" and "end_date". You can also search by the status of the Ticket, which can be "pending" or "completed". *You can only see this section if you are the creator of the ticket.

    Request:

    URL: http://127.0.0.1:8000/api/tickets/tickets_paginated
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "ticket_id": 7,
            "fecha_inicio": "",
            "fecha_fin": "",
            "estado": ""
        }

    Response:

        {
            "current_page": 1,
            "total_pages": 10,
            "tickets": [
                {
                "id": 1,
                "num_images": 4,
                "user": 1,
                "status": "pending",
                "created_at": "2024-04-16T21:37:17.085783Z"
                },
                {
                "id": 2,
                "num_images": 4,
                "user": 1,
                "status": "pending",
                "created_at": "2024-04-16T21:44:53.441392Z"
                },
                {
                "id": 4,
                "num_images": 8,
                "user": 1,
                "status": "pending",
                "created_at": "2024-04-17T04:28:08.327998Z"
                },
            ]
        }

### Check Ticket Status: To use this endpoint, you must enter the ticket id in the format indicated in the request instructions. This will show the status of the Ticket, which may be "pending" if the total number of images uploaded has not been completed and the status of "completed" will be shown once the limit has been reached. *You can only see this section if you are the creator of the ticket.

    Request:

    URL: http://127.0.0.1:8000/api/tickets/check_ticket_status
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "ticket_id": 7
        }

    Response:

        {
            "status": "pending"
        }

### Ticket Details: To use this endpoint, you must enter the ticket id in the format indicated in the request instructions. This will show the complete information of the Tickets and Images that have been uploaded. *You can only see this section if you are the creator of the ticket. 

    Request:

    URL: http://127.0.0.1:8000/api/tickets/ticket_details
    Method: POST
    Authorization: Token fa24b09db3cf450a3780b0c95124aa94ea8f77d2
    Body:

        {
            "ticket_id": 7
        }

    Response:
        {
            "id": 7,
            "num_images": 4,
            "user": 2,
            "status": "pending",
            "created_at": "2024-04-17T05:14:26.653317Z",
            "images": [
                {
                    "id": 6,
                    "image_name": "ldbqhifpf8xxnwwakbii.jpg",
                    "image_url": "http://res.cloudinary.com/dq26ryqbo/image/upload/v1713333104/ldbqhifpf8xxnwwakbii.jpg",
                    "uploaded_at": "2024-04-17T05:51:44.590921Z"
                },
                {
                    "id": 7,
                    "image_name": "dusmm1pp7gvss99ek1mp.jpg",
                    "image_url": "http://res.cloudinary.com/dq26ryqbo/image/upload/v1713333104/dusmm1pp7gvss99ek1mp.jpg",
                    "uploaded_at": "2024-04-17T05:51:45.306836Z"
                },
                {
                    "id": 8,
                    "image_name": "pjbmwbtxi3lcz7fuas8i.jpg",
                    "image_url": "http://res.cloudinary.com/dq26ryqbo/image/upload/v1713333108/pjbmwbtxi3lcz7fuas8i.jpg",
                    "uploaded_at": "2024-04-17T05:51:48.789506Z"
                },
                {
                    "id": 9,
                    "image_name": "fdl2wec3vpj9vpfv1rfc.jpg",
                    "image_url": "http://res.cloudinary.com/dq26ryqbo/image/upload/v1713333108/fdl2wec3vpj9vpfv1rfc.jpg",
                    "uploaded_at": "2024-04-17T05:51:49.300646Z"
                }
            ]
        } 
























