from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
import uuid
from django.shortcuts import get_object_or_404
from .models import User
from .schemas import UserIn, UserOut
from .service import UserService

router = Router()


@router.post("/")
def create_user(request, payload: UserIn):   
  user = UserService.create_user(payload)    
  return {"id": user.id}


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: uuid.UUID):
  user = UserService.get_user(user_id)  
  print("-----")
  print(user)
  print("HELLO at GET USER BY ID")
  return user


@router.get("/", response=List[UserOut])
def list_users(request):
  user = UserService.list_users()
  print("HELLO at GET USERS")
  return user


@router.put("/{user_id}")
def update_user(request, user_id: uuid.UUID, payload: UserIn):
  user = UserService.update_user(user_id, payload)
  return user


@router.delete("/{user_id}")
def delete_user(request, user_id: uuid.UUID):
  UserService.delete_user(user_id)
  return {"success": True}