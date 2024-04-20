from .serializers import UserRegisterSerializer, UserDataSerializer

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@api_view(['POST'])
def user_register(request):

    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return Response({ 'token': token.key, "user": serializer.data }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):

    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({ "error": "Invalid password" }, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserDataSerializer(instance=user)

    return Response({ "message": "Welcome, you have logged in correctly!", "token": token.key, "user": serializer.data }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    
    serializer = UserDataSerializer(instance=request.user)
    
    user_data = serializer.data
    id = user_data['id']
    user = user_data['username']
    email = user_data['email']

    return Response({ "message": "You are logged as {}. User data: ID = {}, USERNAME = {}, EMAIL = {}.".format(user, id, user, email) }, status=status.HTTP_200_OK)
