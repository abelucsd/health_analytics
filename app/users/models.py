import uuid
from django.db import models


class UserRoleChoices(models.TextChoices):
  ADMIN = "admin",
  USER = "user"

# Create your models here.
class User(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
  role = models.CharField(
    max_length = 10,
    choices = UserRoleChoices.choices,
    default = UserRoleChoices.USER,
  )

  def __str__(self):
    return f"{self.first_name} {self.last_name}"