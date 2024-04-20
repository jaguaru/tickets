from django.core.paginator import Paginator
from django.db.models import Q


def paginate_ticket_data(serializer_data, page_number, page_size, start_date=None, end_date=None, status=None):
    
    if start_date and end_date:
        serializer_data = [item for item in serializer_data if item['created_at'] >= start_date and item['created_at'] <= end_date]
    
    if status:
        serializer_data = [item for item in serializer_data if item['status'] == status]
    
    paginator = Paginator(filtered_data, page_size)
    
    try:
        paginated_data = paginator.page(page_number)
    
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return paginated_data
