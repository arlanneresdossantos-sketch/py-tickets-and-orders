from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.utils import timezone
from db.models import Order, Ticket

UserModel = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str | None = None
) -> Order:
    user = UserModel.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        parsed_date = parse_datetime(date)
        if parsed_date:
            if getattr(
                    settings, "USE_TZ", False
            ) and timezone.is_naive(parsed_date):
                try:
                    parsed_date = timezone.make_aware(parsed_date)
                except Exception:
                    pass

            order.created_at = parsed_date
            order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
