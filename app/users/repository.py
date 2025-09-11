import uuid
from users.schemas import UserIn
from .models import User


class UserRepository:
  @staticmethod
  def create(user_in: UserIn):
    user_in_dict = user_in.dict()
    return User.objects.create(**user_in_dict)
  

  @staticmethod
  def get_by_id(user_id):
    return User.objects.get(id=user_id)
  

  @staticmethod
  def list_all():
    return User.objects.all()
  
  
  @staticmethod
  def update(user_id: uuid.UUID, user_in: UserIn):
    user = User.objects.get(id=user_id)
    for attr, value in user_in.dict().items():
      setattr(user, attr, value)
    user.save()
    return user
  

  @staticmethod
  def delete(user_id: uuid.UUID):
    user = User.objects.get(id=user_id)
    user.delete()