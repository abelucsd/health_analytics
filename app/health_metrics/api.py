from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
import uuid
from django.shortcuts import get_object_or_404
from .models import HealthMetric
from .schemas import HealthMetricIn, HealthMetricOut
from .service import HealthMetricService

router = Router()


@router.post("/")
def create(request, payload: HealthMetricIn):   
  record = HealthMetricService.create_user(payload)
  return {"id": record.id}


@router.get("/{health_metric_id}", response=HealthMetricOut)
def get(request, health_metric_id: uuid.UUID):
  record = HealthMetricService.get_user(health_metric_id)
  return record


@router.get("/", response=List[HealthMetricOut])
def list(request):
  record = HealthMetricService.list_users()  
  return record


@router.put("/{health_metric_id}", response=HealthMetricOut)
def update(request, health_metric_id: uuid.UUID, payload: HealthMetricIn):
  record = HealthMetricService.update_user(health_metric_id, payload)
  return record


@router.delete("/{health_metric_id}")
def delete(request, health_metric_id: uuid.UUID):
  HealthMetricService.delete_user(health_metric_id)
  return {"success": True}