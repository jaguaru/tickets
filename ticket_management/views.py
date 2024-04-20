from rest_framework import status, serializers, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Ticket, Image


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_new_ticket(request):

    num_images = request.data['num_images']
    user = request.user
    
    if num_images:
        ticket = Ticket.objects.create(num_images=num_images, user=user)
        return Response({ 'ticket_id': ticket.id, 'status': ticket.status }, status=status.HTTP_201_CREATED)
    else:
        return Response({ 'error': 'Número de imágenes no proporcionado' }, status=status.HTTP_400_BAD_REQUEST)
