import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from db.models import Order, Ticket

User = get_user_model()


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    user = get_object_or_404(User, username=username)

    field = Order._meta.get_field("created_at")

    auto_now_add_original = getattr(field, "auto_now_add", False)

    try:
        if date:
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            setattr(field, "auto_now_add", False)
            order = Order.objects.create(user=user, created_at=parsed_date)
        else:
            order = Order.objects.create(user=user)
    finally:
        setattr(field, "auto_now_add", auto_now_add_original)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order
