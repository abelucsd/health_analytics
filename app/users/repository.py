from .models import User


class UserRepository:
  @staticmethod
  def create(**kwargs):
    return User.objects.create(**kwargs)
  

  @staticmethod
  def get_by_id(user_id):
    return User.objects.get(id=user_id)
  

  @staticmethod
  def list_all():
    return User.objects.all()
  

  @staticmethod
  def delete(user):
    user.delete()