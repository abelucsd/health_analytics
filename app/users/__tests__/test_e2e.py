import json

from django.forms import model_to_dict
import pytest
from users.models import User
from users.schemas import UserIn
from .fixtures import user_factory, mock_user_data
from users.repository import UserRepository
from core.tests.conftest import authenticated_client, mock_authenticate

@pytest.mark.django_db
class TestE2EUsers:
  
  def test_create(self, authenticated_client, mock_user_data):
    payload = mock_user_data.mock_payload()

    response = authenticated_client.post(
      "/api/users/",
      data=json.dumps(payload)
    )
    
    assert response.status_code == 200


  def test_get(self, authenticated_client, user_factory):
    user = user_factory.create()
    user.save()

    response = authenticated_client.get(
      f"/api/users/{user.id}"      
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["email"] == user.email


  def test_list(self, authenticated_client, user_factory):
    user = user_factory.create()
    user.save()
        
    user_list = user_factory.user_list()

    response = authenticated_client.get(
      "/api/users/"
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body[0]["email"] == user_list[0].email
     
  def test_update(self, authenticated_client, user_factory):
    user = user_factory.create()
    user.save()

    updated_user = {
        "first_name": "John",
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "role": user.role,
    }

    response = authenticated_client.put(
      f"/api/users/{user.id}",
      data=json.dumps(updated_user)
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["first_name"] == updated_user["first_name"]


  def test_delete(self, authenticated_client, user_factory):
    user = user_factory.create()
    user.save()
    
    response = authenticated_client.delete(
      f"/api/users/{user.id}"
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["success"] == True