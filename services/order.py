# services/order.py

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket

UserModel = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str, date: str | None = None) -> Order:
    user = UserModel.objects.get(username=username)

    # [ITEM #3] Criamos a ordem salvando-a uma única vez no banco.
    # O auto_now_add vai colocar a data atual de 2026 inicialmente aqui.
    order = Order.objects.create(user=user)

    if date:
        parsed_date = parse_datetime(date)
        if parsed_date:
            # Usamos .update() para forçar a alteração da data retroativa no banco.
            # O .update() ignora o auto_now_add e não conta como um re-salvamento do ciclo de vida do objeto.
            Order.objects.filter(pk=order.pk).update(created_at=parsed_date)
            # Atualiza a instância na memória para o retorno da função ficar correto
            order.created_at = parsed_date

    # Criação dos tickets vinculados
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset