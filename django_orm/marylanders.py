marylanders = Hotel.objects.select_related('rooms__reservations__user').get(title='Maryland')