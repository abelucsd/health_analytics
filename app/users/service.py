import logging
import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from users.models import User
from users.schemas import UserIn, UserOut
from users.repository import UserRepository
from core.exceptions import AppError, ValidationError
from users.exceptions import InvalidRoleError, UserNotFoundError


logger = logging.getLogger("users")


class UserService:
  @staticmethod
  def create_user(user_in: UserIn):
    try:
      logger.info(f"CREATE model=User")
      user = UserRepository.create(user_in)
      logger.info(f"CREATE model=User success user_id: {user.id}")
      return user
    except IntegrityError as e:
      logger.error(f"CREATE ERROR: {e}")
      raise ValidationError(f"Failed to create user: {str(e)}", status_code=400)    


  @staticmethod
  def get_user(user_id: uuid.UUID):
    try:
      logger.info(f"READ model=User id%s", user_id)
      user = UserRepository.get_by_id(user_id)
      logger.info(f"READ model=User success user_id: id%s", user_id)
      return user
    except User.DoesNotExist as e:
      logger.error(f"READ ERROR: {e}")
      raise UserNotFoundError(user_id)    


  @staticmethod
  def list_users():
    logger.info(f"READ model=User")
    users = UserRepository.list_all()
    logger.info(f"READ model=User success")
    return users


  @staticmethod
  def update_user(user_id: uuid.UUID, user_in: UserIn):        
    if user_in.role not in ["user", "admin"]:
      logger.error(f"UPDATE ERROR: InvalidRoleError {user_in.role}")
      raise InvalidRoleError(user_in.role)
    
    try:
      logger.info(f"UPDATE model=User user_id: id%s", user_id)
      user = UserRepository.update(user_id, user_in)
      logger.info(f"READ model=User success user_id: id%s", user_id)
    except User.DoesNotExist as e:
      logger.error(f"UPDATE ERROR: {e}")
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      logger.error(f"UPDATE ERROR: {e}")
      raise ValidationError(f"Failed to update user: {str(e)}", status_code=400)    

    return user


  @staticmethod
  def delete_user(user_id: uuid.UUID):        
    try:
      logger.info(f"DELETE model=User user_id: id%s", user_id)
      UserRepository.delete(user_id)
      logger.info(f"DELETE model=User success user_id: id%s", user_id)
    except User.DoesNotExist as e:
      logger.error(f"DELETE ERROR: {e}")
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      logger.error(f"DELETE ERROR: {e}")
      raise ValidationError(f"Failed to delete user: {str(e)}", status_code=400)