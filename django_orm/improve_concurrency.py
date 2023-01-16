# improved views

from django.db.models import F

def like_hotel_view(request, hotel_id):
    Hotel.objects.filter(id=hotel_id).update(likes=F('likes') + 1)
    return HttpResponse({'details': 'success'})

def dislike_hotel_view(request, hotel_id):
    Hotel.objects.filter(id=hotel_id).update(dislikes=F('dislikes') + 1)
    return HttpResponse({'details': 'success'})

# or

from django.db import transaction

@transaction.atomic
def like_hotel_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.likes += 1
    hotel.save()
    return HttpResponse({'details': 'success'})

@transaction.atomic
def dislike_hotel_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.dislikes += 1
    hotel.save()
    return HttpResponse({'details': 'success'})
