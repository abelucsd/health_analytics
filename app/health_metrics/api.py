import logging
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
logger = logging.getLogger("health_metrics")


@router.post("/")
def create(request, payload: HealthMetricIn): 
  logger.info("API POST /") 
  record = HealthMetricService.create(payload)
  logger.info("API POST / 201 OK id=%s", record.id)
  return {"id": record.id}


@router.get("/{health_metric_id}", response=HealthMetricOut)
def get(request, health_metric_id: uuid.UUID):
  logger.info("API GET /%s", health_metric_id)
  record = HealthMetricService.get(health_metric_id)
  logger.info("API GET /%s 200 OK id=%s", health_metric_id, record.id)
  return record


@router.get("/", response=List[HealthMetricOut])
def list(request):
  logger.info(f"API GET /")
  record = HealthMetricService.list()  
  logger.info(f"API GET / 200 OK")
  return record


@router.put("/{health_metric_id}", response=HealthMetricOut)
def update(request, health_metric_id: uuid.UUID, payload: HealthMetricIn):  
  logger.info("API PUT /%s", health_metric_id)
  record = HealthMetricService.update(health_metric_id, payload)
  logger.info("API PUT /%s 200 OK")
  return record


@router.delete("/{health_metric_id}")
def delete(request, health_metric_id: uuid.UUID):
  logger.info("API DELETE /%s", health_metric_id)
  HealthMetricService.delete(health_metric_id)
  logger.info("API DELETE /%s 200 OK", health_metric_id)
  return {"success": True}


# @router.post("/upload")
# def upload_file(request, file: UploadedFile = File(...)):
#   content = file.read()
#   filename = file.size
#   size = file.size
#   return {"filename": filename, "size": size}