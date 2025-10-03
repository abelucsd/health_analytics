import logging
import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from health_metrics.exceptions import HealthMetricNotFoundError, InvalidGenderError
from health_metrics.schemas import HealthMetricIn, HealthMetricOut
from health_metrics.models import HealthMetric
from health_metrics.repository import HealthMetricRepository
from core.exceptions import AppError, ValidationError


logger = logging.getLogger("health_metrics")


class HealthMetricService:
  @staticmethod
  def create(health_metric_in: HealthMetricIn):
    try:
      logger.debug("CREATE model=HealthMetric")
      record = HealthMetricRepository.create(health_metric_in)
      logger.debug("CREATE model=HealthMetric success")
      return record
    except IntegrityError as e:
      logger.error("CREATE ERROR", exc_info=True)
      raise ValidationError(f"Failed to create health metric: {str(e)}", status_code=400)    


  @staticmethod
  def get(health_metric_id: uuid.UUID):
    try:
      logger.debug("GET model=HealthMetric id:%s", health_metric_id)
      record = HealthMetricRepository.get_by_id(health_metric_id)     
      logger.debug("GET model=HealthMetric success id:%s", record.id) 
      return record
    except HealthMetric.DoesNotExist as e:
      logger.error("GET ERROR", exc_info=True)
      raise HealthMetricNotFoundError(health_metric_id)    


  @staticmethod
  def list():
    logger.debug("GET model=HealthMetric")
    record = HealthMetricRepository.list_all()
    logger.debug("GET model=HealthMetric success")
    return record


  @staticmethod
  def update(health_metric_id: uuid.UUID, health_metric_in: HealthMetricIn):        
    if health_metric_in.gender not in ["male", "female"]:
      logger.error("UPDATE ERROR: InvalidGenderError", exc_info=True)
      raise InvalidGenderError(health_metric_in.gender)
    
    try:
      logger.debug("UPDATE model=HealthMetric id:%s", health_metric_id)
      record = HealthMetricRepository.update(health_metric_id, health_metric_in)
      logger.debug("UPDATE model=HealthMetric success")
    except HealthMetric.DoesNotExist as e:
      logger.error("UPDATE ERROR", exc_info=True)
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      logger.error("UPDATE ERROR", exc_info=True)
      raise ValidationError(f"Failed to update health metric: {str(e)}", status_code=400)    

    return record


  @staticmethod
  def delete(health_metric_id: uuid.UUID):        
    try:
      logger.debug("DELETE model=HealthMetric id:%s", health_metric_id)
      HealthMetricRepository.delete(health_metric_id)
      logger.debug("DELETE model=HealthMetric success id:%s", health_metric_id)
    except HealthMetric.DoesNotExist as e:
      logger.error("DELETE ERROR", exc_info=True)
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      logger.error("DELETE ERROR", exc_info=True)
      raise ValidationError(f"Failed to delete health metric: {str(e)}", status_code=400)