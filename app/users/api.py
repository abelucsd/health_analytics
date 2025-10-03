import logging
from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
import uuid
from django.shortcuts import get_object_or_404
from .models import User
from .schemas import UserIn, UserOut
from .service import UserService

router = Router()
logger = logging.getLogger("users")

@router.post("/")
def create_user(request, payload: UserIn):
  logger.info("API POST /")
  user = UserService.create_user(payload)
  logger.info("API POST / 201 OK id=%s", user.id)
  return {"id": user.id}


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: uuid.UUID):
  logger.info("API GET /%s", user_id)
  user = UserService.get_user(user_id)
  logger.info("API GET /%s 200 OK", user_id)
  return user


@router.get("/", response=List[UserOut])
def list_users(request):  
  logger.info("API GET /")
  user = UserService.list_users()
  logger.info("API GET / 200 OK")
  return user


@router.put("/{user_id}", response=UserOut)
def update_user(request, user_id: uuid.UUID, payload: UserIn):  
  logger.info("API PUT /%s", user_id)
  user = UserService.update_user(user_id, payload)
  logger.info("API PUT /%s 200 OK", user_id)
  return user


@router.delete("/{user_id}")
def delete_user(request, user_id: uuid.UUID):
  logger.info("API DELETE model=User id%s", user_id)
  UserService.delete_user(user_id)
  logger.info("API DELETE /%s 200 OK", user_id)
  return {"success": True}