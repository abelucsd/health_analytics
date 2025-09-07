import json
import pytest
import uuid
from django.forms.models import model_to_dict
from users.schemas import UserIn
from users.models import User

# Create your tests here.

@pytest.fixture
@pytest.mark.django_db
def user_factory(mocker):
  class FakeQuerySet(list):
    def first(self):
      return self[0] if self else None
    
  class UserFactory:
    def create(self, **kwargs):
      defaults = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alicesmith@email.com",
        "password": "secretpassword",
        "role": "user"
      }
      defaults.update(kwargs)      
      return User(id=uuid.uuid4(), **defaults)
        
    def queryset(self):      
      return FakeQuerySet([self.create()])

    def user_list(self):
      return [self.create()]
    
  return UserFactory()


@pytest.fixture
@pytest.mark.django_db
def mock_user_data():
  class MockUserData():
    def __init__(self):
      self.data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alicesmith@email.com",
        "password": "secretpassword",
        "role": "user"
      }
    
    def user_payload(self) -> UserIn:
      return self.data

    def mock_user_in(self):
      return UserIn(**self.data)      
    
    def mock_user(self):
      return User(id=uuid.uuid4(), **self.data)
          
  return MockUserData()


@pytest.mark.django_db
class TestUsers:
        
  def test_create(self, client, mocker, mock_user_data):
    user_payload = mock_user_data.user_payload()
    mock_user = mock_user_data.mock_user()

    mocker.patch("users.api.UserService.create_user", return_value=mock_user)    

    response = client.post(
        "/api/users/",
        data=json.dumps(user_payload),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json() == {"id": str(mock_user.id)}


  @pytest.mark.django_db
  def test_get(self, client, mocker, user_factory):
    user_factory.create()
    qs = user_factory.queryset()    
    user = qs.first()    
    mocker.patch("users.api.UserService.get_user", return_value=user)
    
    response = client.get(f"/api/users/{user.id}")
    response_body = response.json()    

    assert response.status_code == 200
    assert response_body["email"] == user.email


  @pytest.mark.django_db  
  def test_list_users_mock(self, client, mocker, user_factory):

    user_factory.create()
    qs = user_factory.queryset()
    user_list = user_factory.user_list()
    mocker.patch("users.api.UserService.list_users", return_value=qs)

    # Make request    
    response = client.get("/api/users/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body[0]["email"] == user_list[0].email


  @pytest.mark.django_db
  def test_update_user(self, client, mocker, user_factory):
    user_factory.create()
    qs = user_factory.queryset()    
    user = qs.first()
    updated_user = model_to_dict(user)        
    updated_user["first_name"] = "John"    
    mocker.patch("users.api.UserService.update_user", return_value=updated_user)

    response = client.put(f"/api/users/{user.id}", data=json.dumps(updated_user), content_type="application/json")
    response_body = response.json()    

    assert response.status_code == 200
    assert response_body["first_name"] == updated_user["first_name"]


  @pytest.mark.django_db
  def test_delete_user(self, client, mocker, user_factory):
    user_factory.create()
    qs = user_factory.queryset()
    user = qs.first()
    deleted_user = model_to_dict(user)
    mocker.patch("users.api.UserService.delete_user", return_value=None)

    response = client.delete(f"/api/users/{user.id}")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["success"] == True