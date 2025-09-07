import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from users.models import User
from users.schemas import UserIn
from users.repository import UserRepository
from core.exceptions import AppError, ValidationError
from users.exceptions import InvalidRoleError, UserNotFoundError

class UserService:
  @staticmethod
  def create_user(payload: UserIn):
    try:
      payload_dict = payload.dict()
      user = UserRepository.create(**payload_dict)      
      return user
    except IntegrityError as e:
      raise ValidationError(f"Failed to create user: {str(e)}", status_code=400)    


  @staticmethod
  def get_user(user_id: uuid.UUID):
    try:
      user = UserRepository.get_by_id(user_id)      
      return user
    except User.DoesNotExist:
      raise UserNotFoundError(user_id)    


  @staticmethod
  def list_users():
    users = UserRepository.list_all()
    return users


  @staticmethod
  def update_user(user_id: uuid.UUID, payload: UserIn):
    try:
      user = UserRepository.get_by_id(user_id)
    except User.DoesNotExist:
      raise UserNotFoundError(user_id)

    try:      
      user = UserRepository.update(user, payload)
    except IntegrityError as e:
      raise ValidationError(f"Failed to update user: {str(e)}", status_code=400)

    return user
  
  @staticmethod
  def update_user(user_id: uuid.UUID, payload: UserIn):        
    if payload["role"] not in ["user", "admin"]:
      raise InvalidRoleError(payload.role)
    
    try:
      user = UserRepository.update(user_id, payload)
    except User.DoesNotExist:
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to update user: {str(e)}", status_code=400)    

    return user


  @staticmethod
  def delete_user(user_id: uuid.UUID):        
    try:
      UserRepository.delete(user_id)
    except User.DoesNotExist:
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to delete user: {str(e)}", status_code=400)