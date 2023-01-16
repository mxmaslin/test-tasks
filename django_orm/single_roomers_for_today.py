# Get list of hotels with only one free room (for today)

from datetime import date
from django.db.models import Q, Count


today = date.today() 

free_hotel_ids = Room.objects.filter(reservations__start__lte=today, reservations__end__gte=today)\
    .values('hotel')\
    .annotate(free_rooms=Count('id', filter=Q(reservations__isnull=True))) \
    .filter(free_rooms=1)\
    .values_list('hotel', flat=True)
hotels = Hotel.objects.filter(id__in=free_hotel_ids)
