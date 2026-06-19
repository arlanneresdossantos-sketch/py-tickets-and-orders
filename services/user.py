from typing import cast
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from db.models import User


UserModel = cast(UserManager, get_user_model().objects)


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> User:
    extra_fields = {}
    if email:
        extra_fields["email"] = email
    if first_name:
        extra_fields["first_name"] = first_name
    if last_name:
        extra_fields["last_name"] = last_name

    user = UserModel.create_user(
        username=username,
        password=password,
        **extra_fields
    )
    return user  # type: ignore


def get_user(user_id: int) -> User:
    return UserModel.get(id=user_id)  # type: ignore


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> User:
    user = get_user(user_id)

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user