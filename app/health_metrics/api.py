import logging
from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from ninja import File
import uuid
from django.shortcuts import get_object_or_404
from health_metrics.models import HealthMetric
from health_metrics.schemas import HealthMetricIn, HealthMetricOut, HealthMetricListOut
from health_metrics.service import HealthMetricService
from health_metrics.data import HEALTH_METRIC_RANGES


router = Router()
logger = logging.getLogger("health_metrics")


@router.post("/")
def create(request, payload: HealthMetricIn): 
  logger.info("API POST /") 
  record = HealthMetricService.create(payload)
  logger.info("API POST / 201 OK id=%s", record.id)
  return {"id": record.id}


@router.get("/latest", response=HealthMetricOut)
def get_latest(request):
  logger.info("API GET /latest") 
  record = HealthMetricService.get_latest()
  logger.info("API GET / 200 OK id=%s", record.id)  
  record.ranges = HEALTH_METRIC_RANGES
  return record


@router.get("/previous", response=HealthMetricOut)
def get_second_latest(request):
  logger.info("API GET /previous") 
  record = HealthMetricService.get_second_latest()
  logger.info("API GET / 200 OK id=%s", record.id)
  record.ranges = HEALTH_METRIC_RANGES
  return record


@router.get("/target_metrics")
def get_target_metrics(request):
  logger.info("API GET /target_metrics")
  records = HealthMetricService.get_target_metrics()
  logger.info("API GET / 200 ok")
  return records


@router.get("/{health_metric_id}", response=HealthMetricOut)
def get(request, health_metric_id: uuid.UUID):
  logger.info("API GET /%s", health_metric_id)
  record = HealthMetricService.get(health_metric_id)
  logger.info("API GET /%s 200 OK id=%s", health_metric_id, record.id)
  record.ranges = HEALTH_METRIC_RANGES
  return record


@router.get("/", response=HealthMetricListOut)
def list(request):
  logger.info(f"API GET /")
  records = HealthMetricService.list()  
  logger.info(f"API GET / 200 OK")
  # record.ranges = HEALTH_METRIC_RANGES
  # items = [HealthMetricOut.from_orm(record) for record in records]
  response = {}  
  response["items"] = records
  response["ranges"] = HEALTH_METRIC_RANGES  
  return response


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