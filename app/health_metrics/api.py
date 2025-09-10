from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
import uuid
from django.shortcuts import get_object_or_404
from .models import HealthMetrics
from .schemas import HealthMetricsIn, HealthMetricsOut
from .service import HealthMetricsService

router = Router()


@router.post("/")
def create(request, payload: HealthMetricsIn):   
  record = HealthMetricsService.create_user(payload)
  return {"id": record.id}


@router.get("/{health_metrics_id}", response=HealthMetricsOut)
def get(request, health_metrics_id: uuid.UUID):
  record = HealthMetricsService.get_user(health_metrics_id)
  return record


@router.get("/", response=List[HealthMetricsOut])
def list(request):
  record = HealthMetricsService.list_users()
  print("HELLO at GET USERS")
  return record


@router.put("/{health_metrics_id}", response=HealthMetricsOut)
def update(request, health_metrics_id: uuid.UUID, payload: HealthMetricsIn):
  record = HealthMetricsService.update_user(health_metrics_id, payload)
  return record


@router.delete("/{health_metrics_id}")
def delete(request, health_metrics_id: uuid.UUID):
  HealthMetricsService.delete_user(health_metrics_id)
  return {"success": True}