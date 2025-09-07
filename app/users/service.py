import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from app.core.exceptions import AppError, ValidationError
from app.users.exceptions import UserNotFoundError
from app.users.models import User
from app.users.schemas import UserIn


def create_user(payload: UserIn):
  try:
    payload_dict = payload.dict()
    user = User.objects.create(**payload_dict)
    return user
  except IntegrityError as e:
    raise ValidationError(f"Failed to create user: {str(e)}", status_code=400)
  except Exception as e:
    raise AppError(f"Unexpected error: {str(e)}", status_code=500)


def get_user(user_id: uuid.UUID):
  try:
    user = User.objects.get(User, id=user_id)
  except User.DoesNotExist:
    raise UserNotFoundError(user_id)
  return user


def list_users():
  users = User.objects.all()
  return users


def update_user(user_id: uuid.UUID, payload: UserIn):
  try:
    user = User.objects.get(id=user_id)        
  except User.DoesNotExist:
    raise UserNotFoundError(user_id)  
  
  for attr, value in payload.dict().items():
    setattr(user, attr, value)

  try:
    user.save()
  except IntegrityError as e:
    raise ValidationError(f"Failed to update user: {str(e)}", status_code=400)
  except Exception as e:
    raise AppError(f"Unexpected error: {str(e)}", status_code=500)

  return user


def delete_user(user_id: uuid.UUID):
  try:
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    raise UserNotFoundError(user_id)  
  
  try:
    user.delete()
  except IntegrityError as e:
    raise ValidationError(f"Failed to delete user: {str(e)}", status_code=400)
  except Exception as e:
    raise AppError(f"Unexpected error: {str(e)}", status_code=500)
  
  return user