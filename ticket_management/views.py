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


def verify_owner(user_id, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return ticket.user_id == user_id


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_cloudinary_image(request):

    request_json_data = request.data

    ticket_id = request_json_data['ticket_id']
    ticket = Ticket.objects.get(id=ticket_id)

    user_id = request.user.id
    user_is_owner = verify_owner(user_id, ticket_id)

    if user_is_owner:

        if 'ticket_id' not in request_json_data:
            return JsonResponse({ 'error': 'No se encontro el ticket_id' }, status=status.HTTP_400_BAD_REQUEST)

        if 'images' not in request_json_data:
            return JsonResponse({ 'error': 'No se encontraron imagenes en el json' }, status=status.HTTP_400_BAD_REQUEST)

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
        
        images_list = request_json_data.get('images')

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
                return Response({ 'error': 'A ocurrido un error. {}'.format(_except) }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({ 'message': 'Las imagenes se subieron correctamente!' }, status=status.HTTP_200_OK)
    
    else:
        return Response({ 'error': 'No puedes usar este ticket!' }, status=status.HTTP_401_UNAUTHORIZED)
