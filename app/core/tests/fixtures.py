import pytest 
import uuid
from django.test import Client
from .utils import AuthenticatedClient

class CustomUser():
  def __init__(self):
    self.id = uuid.uuid4()
    self.email = "email@test.com"
    self.name="test"


@pytest.fixture
def mock_authenticate(mocker):
  test_user = CustomUser()

  mocker.patch(
    "core.users.Authentication.authenticate",
    return_value=test_user,
  )


@pytest.fixture
def authenticated_client(mock_authenticate):
  authenticated_client = AuthenticatedClient(Client())
  return authenticated_client