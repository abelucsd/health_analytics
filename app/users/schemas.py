from typing import Optional
from uuid import UUID
from ninja import ModelSchema, Schema
from pydantic import EmailStr
from .models import User
from .models import UserRoleChoices


class UserIn(Schema):
  first_name: str
  last_name: str
  email: EmailStr
  password: str
  role: Optional[UserRoleChoices] = UserRoleChoices.USER

  class Config:
    extra = "forbid"


class UserOut(Schema):
  id: UUID
  first_name: str
  last_name: str
  email: EmailStr
  password: str
  role: UserRoleChoices = UserRoleChoices.USER

  class Config:
    extra = "forbid"