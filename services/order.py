from django.db import transaction
from django.db.models import QuerySet
from django.forms import DateTimeField

from db.models import Order
from db.models import User
from db.models import Ticket
from db.models import MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: DateTimeField = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        if date:
            order = Order.objects.create(user=user, created_at=date)
        else:
            order = Order.objects.create(user=user)
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session
            )
        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
