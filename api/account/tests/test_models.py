import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'
    name = 'Test User'

    user = User.objects.create_user(
        username=username, email=email, password=password, name=name,
    )

    assert user.username == username
    assert user.email == email
    assert user.name == name
    assert user.is_staff is False
    assert user.is_active is True
    assert user.get_full_name() == name
    assert user.get_short_name() == 'Test'
