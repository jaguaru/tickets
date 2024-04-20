from django.contrib import admin
from .models import Ticket, Image


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_images', 'user', 'status', 'created_at',)
    actions = ['delete_selected']

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'image_name', 'image_url', 'uploaded_at',)
    actions = ['delete_selected']


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Image, ImageAdmin)

