from django.core.exceptions import ValidationError
from django.db import transaction
import datetime

from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None
) -> None:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError("User does not exist")

    order = Order.objects.create(
        user=user,
        created_at=date
    )

    for ticket in tickets:
        ticket_obj = Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        ticket_obj.full_clean()
        ticket_obj.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
