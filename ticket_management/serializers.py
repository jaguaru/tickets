from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image_name', 'image_url', 'uploaded_at']


class TicketSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'num_images', 'user', 'status', 'created_at', 'images']


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status']
