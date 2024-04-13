import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from api.core.models import Event, Participant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def participant():
    return baker.make(Participant)


@pytest.fixture
@pytest.mark.django_db
def event():
    return baker.make(Event, participants=[baker.make(Participant)])


@pytest.mark.django_db
class TestParticipantView:
    endpoint = '/participants/'

    def test_list_participants(self, api_client, participant):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == participant.id

    def test_update_participant(self, api_client, participant):
        data = {
            'username': 'updatedusername',
            'email': 'updatedemail@example.com',
            'password': 'updatedpassword',
            'phone': participant.phone,
            'address': participant.address.id,
        }
        url = f'{self.endpoint}{participant.id}/'
        print(url)
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert Participant.objects.count() == 1
        assert Participant.objects.first().username == data['username']

    def test_create_participant(self, api_client):
        data = {
            'username': 'username',
            'email': 'higor@gmail.com',
            'password': 'password',
            'phone': '123456789',
            'address': baker.make('core.Address').id,
        }
        response = api_client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Participant.objects.count() == 1
        assert Participant.objects.first().username == data['username']

    def test_delete_participant(self, api_client, participant):
        url = f'{self.endpoint}{participant.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Participant.objects.count() == 0


@pytest.mark.django_db
class TestEventView:
    endpoint = '/events/'

    def test_list_events(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_create_event(self, api_client):
        data = {
            'title': 'Sua festa',
            'description': 'Festa de aniversário',
            'date': '2024-04-22',
            'time': '12:00:00',
            'address': baker.make('core.Address').id,
        }
        response = api_client.post(self.endpoint, data)
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
        assert Event.objects.first().title == data['title']

    def test_update_event(self, api_client, event):
        data = {
            'title': event.title,
            'description': event.description,
            'date': '2025-04-24',
            'participants': event.participants.values_list('id', flat=True),
            'time': event.time,
            'address': event.address.id,
        }
        url = f'{self.endpoint}{event.id}/'
        response = api_client.put(url, data)
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert Event.objects.count() == 1
        assert Event.objects.first().title == data['title']

    def test_delete_event(self, api_client, event):
        url = f'{self.endpoint}{event.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Event.objects.count() == 0
