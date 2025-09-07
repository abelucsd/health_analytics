import pytest
from users.models import User
from users.schemas import UserIn
from .fixtures import user_factory, mock_user_data
from users.repository import UserRepository


@pytest.mark.django_db
class TestUserRepository:

  def test_create(self, mock_user_data):
    payload = mock_user_data.user_payload()    

    created_user = UserRepository.create(payload)

    assert created_user.email == payload["email"]

  
  def test_get_by_id(self, user_factory):
    user = user_factory.create()
    user.save()

    fetched_user = UserRepository.get_by_id(user.id)    

    assert fetched_user.email == user.email


  def test_list_all(self, user_factory):
    user = user_factory.create()
    user.save()

    fetched_users = UserRepository.list_all()

    assert list(fetched_users)[0].email == user.email


  def test_update(self, user_factory, mock_user_data):
    payload = mock_user_data.mock_user_in()
    user = user_factory.create()
    user.save()

    payload.first_name = "John"

    updated_user = UserRepository.update(user.id, payload)

    assert updated_user.first_name == payload.first_name

  
  def test_delete(self, user_factory):
    user = user_factory.create()
    user.save()    

    UserRepository.delete(user.id)

    with pytest.raises(User.DoesNotExist):
      User.objects.get(id=user.id)
    