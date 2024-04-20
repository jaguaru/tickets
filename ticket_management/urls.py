"""
URL configuration for ticket_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from ticket_management import token, views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/token/login', token.user_login),
    path('api/auth/token/register', token.user_register),
    path('api/auth/token/profile', token.user_profile),

    path('api/tickets/create_ticket', views.create_new_ticket),
    path('api/tickets/upload_cloud_image', views.upload_cloudinary_image),
    path('api/tickets/tickets_paginated', views.tickets_paginated),
    path('api/tickets/check_ticket_status', views.monitoring_ticket_status),
    path('api/tickets/ticket_details', views.all_ticket_details),

]
