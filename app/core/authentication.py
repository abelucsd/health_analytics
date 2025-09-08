import jwt
from django.conf import settings
from users.models import User
from users.exceptions import UserNotFoundError

class Authentication:
  @staticmethod
  def authenticate(token: str) -> User:
    if not token:
      raise ValueError("Missing authentication token")
    
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
      raise ValueError("Token expired")
    except jwt.InvalidTokenError:
      raise ValueError("Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
      raise ValueError("Invalid payload: no subject")
    
    try:
      return User.objects.get(id=user_id)
    except User.DoesNotExist:
      raise UserNotFoundError(user_id)