import pytest
from users.models import User
from users.schemas import UserIn
from .fixtures import user_factory, mock_user_data
from users.repository import UserRepository
