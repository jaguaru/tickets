import base64

from django.shortcuts import get_object_or_404

from rest_framework import status, serializers, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Ticket, Image
from .my_cloudinary import save_cloud_image_wait
from .utils import verify_owner
from .pagination import paginate_ticket_data
from .serializers import TicketSerializer, TicketImageSerializer, TicketStatusSerializer


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
        return Response({ 'error': 'Number of images not provided.' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def monitoring_ticket_status(request):

    ticket_id = request.data['ticket_id']
    user_id = request.user.id
    user_is_owner = verify_owner(user_id, ticket_id)

    if user_is_owner:

        try:
            ticket = get_object_or_404(Ticket, id=ticket_id, user_id=user_id)
            ticket_serializer = TicketStatusSerializer(ticket)
 
            return Response(ticket_serializer.data)

        except Ticket.DoesNotExist:
            return Response({ 'error': 'The ticket does not exist or has not been found!' }, status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response({ 'error': 'You do not have permission to view this ticket!' }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_ticket_details(request):

    ticket_id = request.data['ticket_id']
    user_id = request.user.id
    user_is_owner = verify_owner(user_id, ticket_id)

    if user_is_owner:

        try:
            ticket = get_object_or_404(Ticket, id=ticket_id, user_id=user_id)
            ticket_serializer = TicketImageSerializer(ticket)
 
            return Response(ticket_serializer.data)

        except Ticket.DoesNotExist:
            return Response({ 'error': 'The ticket does not exist or has not been found!' }, status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response({ 'error': 'You do not have permission to view this ticket!' }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_cloudinary_image(request):
    
    ticket_id = request.data['ticket_id']
    ticket = Ticket.objects.get(id=ticket_id)

    user_id = request.user.id
    user_is_owner = verify_owner(user_id, ticket_id)

    if user_is_owner:

        if 'ticket_id' not in request.data:
            return JsonResponse({ 'error': 'Ticket_id not found in the request!' }, status=status.HTTP_400_BAD_REQUEST)

        if 'images' not in request.data:
            return JsonResponse({ 'error': 'No images found in the request!' }, status=status.HTTP_400_BAD_REQUEST)

        max_num_images = ticket.num_images
        num_uploaded_images = ticket.images.count()

        total_to_upload = max_num_images - num_uploaded_images

        if total_to_upload == 0:
            ticket.status = 'completed'
            ticket.save()

        if ticket.status != 'pending':
            return Response({ 'error': 'No se pueden subir más imágenes, el ticket ya está completado' }, status=status.HTTP_400_BAD_REQUEST)

        if num_uploaded_images >= max_num_images:
            return Response({ 'error': 'Se ha alcanzado el límite de imágenes para este ticket' }, status=status.HTTP_409_CONFLICT)
        
        images_list = request.data.get('images')

        for num, images in zip(reversed(range(total_to_upload)), images_list):

            base64_data = images.get('image_base64', '')
            image_bytes = base64.b64decode(base64_data)

            info_cloud_image = save_cloud_image_wait(image_bytes)

            try:
                image_name = info_cloud_image['public_id']
                extension = info_cloud_image['format']
                cloud_url = info_cloud_image['url']

                image_name_ext = image_name + '.' + extension

                image = Image.objects.create(ticket=ticket, image_name=image_name_ext, image_url=cloud_url)
        
            except Exception as _except:
                return Response({ 'error': '{}'.format(_except) }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({ 'message': 'Las imagenes se subieron correctamente!' }, status=status.HTTP_200_OK)
    
    else:
        return Response({ 'error': 'No puedes usar este ticket!' }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tickets_paginated(request):

    user_id = request.user.id
    ticket_id = request.data['ticket_id']

    user_is_owner = verify_owner(user_id, ticket_id)

    if user_is_owner:

        tickets = Ticket.objects.all()
        ticket_serializer = TicketSerializer(tickets, many=True)
        
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        status = request.GET.get('status', None)

        try:
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            paginated_data = paginate_ticket_data(ticket_serializer.data, page_number, page_size, start_date, end_date, status)

            paginated_data_serializable = list(paginated_data.object_list)

            ticket_data = { 
                            'current_page': paginated_data.number, 
                            'total_pages': paginated_data.paginator.num_pages,
                            'tickets': paginated_data_serializable
                          }

            return Response(ticket_data)

        except Ticket.DoesNotExist:
            return Response({'error': 'No se encontró el ticket para este usuario'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({ 'error': 'No puedes ver este ticket!' }, status=status.HTTP_401_UNAUTHORIZED)
