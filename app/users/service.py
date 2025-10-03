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
      logger.debug("CREATE model=User")
      user = UserRepository.create(user_in)
      logger.debug("CREATE model=User success user_id: %s", user.id)
      return user
    except IntegrityError as e:
      logger.error("CREATE ERROR: %s", exc_info=True)
      raise ValidationError(f"Failed to create user: {str(e)}", status_code=400)    


  @staticmethod
  def get_user(user_id: uuid.UUID):
    try:
      logger.debug("READ model=User id%s", user_id)
      user = UserRepository.get_by_id(user_id)
      logger.debug("READ model=User success user_id: id%s", user_id)
      return user
    except User.DoesNotExist as e:
      logger.error("READ ERROR: %s", exc_info=True)
      raise UserNotFoundError(user_id)    


  @staticmethod
  def list_users():
    logger.debug("READ model=User")
    users = UserRepository.list_all()
    logger.debug("READ model=User success")
    return users


  @staticmethod
  def update_user(user_id: uuid.UUID, user_in: UserIn):        
    if user_in.role not in ["user", "admin"]:
      logger.error("UPDATE ERROR: InvalidRoleError %s", exc_info=True)
      raise InvalidRoleError(user_in.role)
    
    try:
      logger.debug("UPDATE model=User user_id: id%s", user_id)
      user = UserRepository.update(user_id, user_in)
      logger.debug("READ model=User success user_id: id%s", user_id)
    except User.DoesNotExist as e:
      logger.error("UPDATE ERROR: %s", exc_info=True)
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      logger.error("UPDATE ERROR: %s", exc_info=True)
      raise ValidationError(f"Failed to update user: {str(e)}", status_code=400)    

    return user


  @staticmethod
  def delete_user(user_id: uuid.UUID):        
    try:
      logger.debug("DELETE model=User user_id: id%s", user_id)
      UserRepository.delete(user_id)
      logger.debug("DELETE model=User success user_id: id%s", user_id)
    except User.DoesNotExist as e:
      logger.error("DELETE ERROR: %s", exc_info=True)
      raise UserNotFoundError(user_id)
    except IntegrityError as e:
      logger.error("DELETE ERROR: %s", exc_info=True)
      raise ValidationError(f"Failed to delete user: {str(e)}", status_code=400)