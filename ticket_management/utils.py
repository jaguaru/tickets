from django.shortcuts import get_object_or_404

from .models import Ticket


def verify_owner(user_id, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return ticket.user_id == user_id
