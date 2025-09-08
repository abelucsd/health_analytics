import pytest
import uuid
from users.models import User
from users.schemas import UserIn



@pytest.fixture
@pytest.mark.django_db
def user_factory(mocker):
  class FakeQuerySet(list):
    def first(self):
      return self[0] if self else None
    
    def __repr__(self):
      return f"<QuerySet {list.__repr__(self)}>"
    
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
    
    def mock_payload(self) -> UserIn:
      return self.data.copy()

    def mock_user_in(self):
      return UserIn(**self.data)
    
    def mock_user(self):
      return User(id=uuid.uuid4(), **self.data)
          
  return MockUserData()