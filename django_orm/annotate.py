def get_rooms_list_with_sold_out_sign(move_in, move_out):
    reserved_room_ids = Reservation.objects.filter(start__lt=move_out, end__gt=move_in).values('room')
    rooms = Room.objects.annotate(
        sold_out=Case(
            When(id__in=Subquery(reserved_room_ids), then=True),
            default=False,
            output_field=BooleanField()
        )
    )
    return rooms