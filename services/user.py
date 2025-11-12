from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:

    if not username or not password:
        raise ValueError("Username and password are required")

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    user.set_password(password)
    user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        new_password: str = None,
        new_username: str = None,
        new_email: str = None,
        new_first_name: str = None,
        new_last_name: str = None) -> None:

    if not user_id or user_id <= 0:
        raise ValueError("User id is required")

    try:
        user = get_user_model().objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User does not exist")

    if new_username is not None:
        user.username = new_username

    if new_email is not None:
        user.email = new_email

    if new_first_name is not None:
        user.first_name = new_first_name

    if new_last_name is not None:
        user.last_name = new_last_name

    if new_password:
        user.set_password(new_password)

    user.save()
