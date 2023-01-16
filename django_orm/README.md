Our Django app uses the following models:

```
class Hotel(models.Model):
	title = models.CharField(max_length=128)
	likes = models.PositiveIntegerField()
	dislikes = models.PositiveIntegerField()

class Room(models.Model):
	title = models.CharField(max_length=128)
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

class Reservation(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
	start = models.DateField()
	end = models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
```

1) Get the list of users are living in hotel Maryland. [Solution](https://github.com/mxmaslin/test-tasks/blob/master/django_orm/marylanders.py)

2) What should be fixed and improved in these views (in terms of concurrency)

```
	def like_hotel_view(request, hotel_id):
		hotel = get_object_or_404(Hotel, id=hotel_id)
		hotel.likes += 1
		hotel.save()
		return HttpResponse({'details': 'success'})
	
	def dislike_holet_view(request, hotel_id):
		hotel = get_object_or_404(Hotel, id=hotel_id)
		hotel.dislikes += 1
		hotel.save()
		return HttpResponse({'details': 'success'})
```

[Solution](https://github.com/mxmaslin/test-tasks/blob/master/django_orm/improve_concurrency.py)

3) Get list of all rooms with sold_out(True|False) sign (attribute of room object). Sold_out sign should be calculated for user’s move in and move out dates.

```
def get_rooms_list_with_sold_out_sign(move_in, move_out):
	# your code here
```

[Solution](https://github.com/mxmaslin/test-tasks/blob/master/django_orm/annotate.py)

4. Get list of hotels with only one free room (for today) [Solution](https://github.com/mxmaslin/test-tasks/blob/master/django_orm/single_roomers_for_today.py)
