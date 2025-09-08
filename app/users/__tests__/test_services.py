from users.models import User
import pytest
import uuid
from django.forms.models import model_to_dict
from users.service import UserService
from .fixtures import user_factory, mock_user_data

class TestUserService:
  def test_create_user(self, mocker, mock_user_data):
    payload = mock_user_data.mock_user_in()
    mock_user = mock_user_data.mock_user()
    mocker.patch("users.service.UserRepository.create", return_value=mock_user)

    user = UserService.create_user(payload)

    assert user == mock_user


  def test_get_user(self, mocker, mock_user_data):
    mock_user = mock_user_data.mock_user()
    mocker.patch("users.service.UserRepository.get_by_id", return_value=mock_user)

    user = UserService.get_user(mock_user.id)

    assert user == mock_user


  def test_list_users(self, mocker, user_factory):
    user_factory.create()
    qs = user_factory.queryset()        

    mocker.patch("users.service.UserRepository.list_all", return_value=qs)

    users = UserService.list_users()

    assert users == qs


  def test_update_user(self, mocker, mock_user_data):
    user = mock_user_data.mock_user()
    mock_user_in = mock_user_data.mock_user_in()

    mock_user_in.first_name = "John"    

    updated_user = User(
        id=user.id,
        first_name="John",
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        role=user.role
    )

    mocker.patch("users.service.UserRepository.update", return_value=updated_user)

    result = UserService.update_user(user.id, mock_user_in)

    assert result.email == updated_user.email


  def test_delete_user(self, mocker, mock_user_data):
    mock_user = mock_user_data.mock_user()

    mocker.patch("users.service.UserRepository.delete")

    result = UserService.delete_user(mock_user.id)

    assert result is None