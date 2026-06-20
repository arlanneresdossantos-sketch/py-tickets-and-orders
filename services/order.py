import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from db.models import Order, Ticket

User = get_user_model()


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    user = get_object_or_404(User, username=username)

    with transaction.atomic():
        if date:
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(user=user)
            Order.objects.filter(pk=order.pk).update(created_at=parsed_date)
            order.refresh_from_db()
        else:
            order = Order.objects.create(user=user)

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

        return order
