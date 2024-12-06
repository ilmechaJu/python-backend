import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.utils.jwt_utils import generate_access_token, generate_refresh_token, verify_token

@pytest.mark.django_db
def test_access_token_generation(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    token = generate_access_token(user.id)

    assert token is not None
    payload = verify_token(token)
    assert payload['user_id'] == user.id

@pytest.mark.django_db
def test_refresh_token_generation(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    refresh_token = generate_refresh_token(user.id)

    assert refresh_token is not None
    payload = verify_token(refresh_token)
    assert payload['user_id'] == user.id

@pytest.mark.django_db
def test_login_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    login_url = reverse('login')
    response = client.post(login_url, {'username': 'testuser', 'password': 'testpassword'}, content_type='application/json')

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()

@pytest.mark.django_db
def test_refresh_token_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    refresh_token = generate_refresh_token(user.id)
    refresh_url = reverse('refresh_token')

    response = client.post(refresh_url, {'refresh_token': refresh_token}, content_type='application/json')

    assert response.status_code == 200
    assert 'access_token' in response.json()
