from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import User
from .schemas import UserIn, UserOut
from . import service

router = Router()


@router.post("/")
def create_user(request, payload: UserIn):  
  user = service.create_user(payload)  
  return {"id": user.id}


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
  return service.get_user(user_id)  


@router.get("/", response=List[UserOut])
def list_users(request):
  return service.list_users()  


@router.put("/{user_id}")
def update_user(request, user_id: int, payload: UserIn):
  service.update_user(user_id, payload)
  return {"success": True}


@router.delete("/{user_id}")
def delete_user(request, user_id: int):
  service.delete_user(user_id)
  return {"success": True}