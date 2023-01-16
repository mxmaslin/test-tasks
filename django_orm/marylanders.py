# Get the list of users are living in hotel Maryland

marylanders = Hotel.objects.select_related('rooms__reservations__user').get(title='Maryland')