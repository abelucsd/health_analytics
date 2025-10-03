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
      logger.debug(f"CREATE model=HealthMetric")
      record = HealthMetricRepository.create(health_metric_in)
      logger.debug(f"CREATE model=HealthMetric success id:{record.id}")
      return record
    except IntegrityError as e:
      logger.error(f"CREATE ERROR: {e}")
      raise ValidationError(f"Failed to create health metric: {str(e)}", status_code=400)    


  @staticmethod
  def get(health_metric_id: uuid.UUID):
    try:
      logger.debug(f"GET model=HealthMetric id:{health_metric_id}")
      record = HealthMetricRepository.get_by_id(health_metric_id)     
      logger.debug(f"GET model=HealthMetric success id:{record.id}") 
      return record
    except HealthMetric.DoesNotExist as e:
      logger.error(f"GET ERROR: {e}")
      raise HealthMetricNotFoundError(health_metric_id)    


  @staticmethod
  def list():
    logger.debug(f"GET model=HealthMetric")
    record = HealthMetricRepository.list_all()
    logger.debug(f"GET model=HealthMetric success")
    return record


  @staticmethod
  def update(health_metric_id: uuid.UUID, health_metric_in: HealthMetricIn):        
    if health_metric_in.gender not in ["male", "female"]:
      logger.error(f"UPDATE ERROR: InvalidGenderError {health_metric_in.gender}")
      raise InvalidGenderError(health_metric_in.gender)
    
    try:
      logger.debug(f"UPDATE model=HealthMetric id:{health_metric_id}")
      record = HealthMetricRepository.update(health_metric_id, health_metric_in)
      logger.debug(f"UPDATE model=HealthMetric success record:{record.id}")
    except HealthMetric.DoesNotExist as e:
      logger.error("UPDATE ERROR: {e}")
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      logger.error("UPDATE ERROR: {e}")
      raise ValidationError(f"Failed to update health metric: {str(e)}", status_code=400)    

    return record


  @staticmethod
  def delete(health_metric_id: uuid.UUID):        
    try:
      logger.debug(f"DELETE model=HealthMetric id:{health_metric_id}")
      HealthMetricRepository.delete(health_metric_id)
      logger.debug(f"DELETE model=HealthMetric success id:{health_metric_id}")
    except HealthMetric.DoesNotExist as e:
      logger.error("DELETE ERROR: {e}")
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      logger.error("DELETE ERROR: {e}")
      raise ValidationError(f"Failed to delete health metric: {str(e)}", status_code=400)