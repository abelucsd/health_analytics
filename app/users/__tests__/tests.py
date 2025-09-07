# import json
# from django.test import TestCase
# from unittest.mock import patch, MagicMock
# import pytest
# from django.db.models.query import QuerySet
# from users.schemas import UserIn
# from ninja.testing import TestClient
# from app.urls import api
# from users.api import router
# from users.models import User
# import uuid

# # Create your tests here.

# @pytest.fixture
# @pytest.mark.django_db
# def test_user():
#   user = User.objects.create(
#     first_name="Foo",
#     last_name="Bar",
#     email="foobar@email.com",
#     password="secretpassword",
#     role="user"
#   )
#   return user

# @pytest.fixture
# def user_payload() -> UserIn:
#   return {
#     "first_name": "Alice",
#     "last_name": "Smith",
#     "email": "alicesmith@email.com",
#     "password": "secretpassword",
#     "role": "user"
#   }

# @pytest.fixture
# def mock_user():
#   user = MagicMock()
#   user.id = "mocked-id"
#   user.first_name = "Alice"
#   user.last_name = "Smith"
#   user.email = "alicesmith@email.com"
#   user.role = "user"
#   return user


# @pytest.mark.django_db
# class TestUsers:

#   @pytest.mark.django_db
#   @patch("users.api.User.objects.create")
#   def test_create(self, mock_create, client, user_payload, mock_user):        
#     mock_create.return_value = mock_user

#     response = client.post(
#         "/api/users/",
#         data=json.dumps(user_payload),
#         content_type="application/json"
#     )

#     assert response.status_code == 200
#     assert response.json() == {"id": "mocked-id"}
#     mock_create.assert_called_once_with(**user_payload)


#   @pytest.mark.django_db  
#   def test_list_users_mock(mock_all, client, test_user):     

#     # Make request
#     response = client.get("/api/users/")

#     assert response.status_code == 200    
#     assert response.json() == [
#       {
#           "id": str(test_user.id),
#           "first_name": test_user.first_name,
#           "last_name": test_user.last_name,
#           "email": test_user.email,
#           "password": test_user.password,
#           "role": test_user.role
#       }
#     ]