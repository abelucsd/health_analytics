from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from ninja import File
import uuid
from django.shortcuts import get_object_or_404
from health_metrics.models import HealthMetric
from health_metrics.schemas import HealthMetricIn, HealthMetricOut
from health_metrics.service import HealthMetricService


router = Router()


@router.post("/")
def create(request, payload: HealthMetricIn):  
  record = HealthMetricService.create(payload)
  return {"id": record.id}


@router.get("/{health_metric_id}", response=HealthMetricOut)
def get(request, health_metric_id: uuid.UUID):
  record = HealthMetricService.get(health_metric_id)
  return record


@router.get("/", response=List[HealthMetricOut])
def list(request):
  record = HealthMetricService.list()  
  return record


@router.put("/{health_metric_id}", response=HealthMetricOut)
def update(request, health_metric_id: uuid.UUID, payload: HealthMetricIn):  
  record = HealthMetricService.update(health_metric_id, payload)
  return record


@router.delete("/{health_metric_id}")
def delete(request, health_metric_id: uuid.UUID):
  HealthMetricService.delete(health_metric_id)
  return {"success": True}


# @router.post("/upload")
# def upload_file(request, file: UploadedFile = File(...)):
#   content = file.read()
#   filename = file.size
#   size = file.size
#   return {"filename": filename, "size": size}