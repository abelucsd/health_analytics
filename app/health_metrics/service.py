import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from health_metrics.exceptions import HealthMetricNotFoundError, InvalidGenderError
from health_metrics.schemas import HealthMetricIn, HealthMetricOut
from health_metrics.models import HealthMetric
from health_metrics.repository import HealthMetricRepository
from core.exceptions import AppError, ValidationError

class HealthMetricService:
  @staticmethod
  def create(health_metric_in: HealthMetricIn):
    try:      
      record = HealthMetricRepository.create(health_metric_in)
      return record
    except IntegrityError as e:
      raise ValidationError(f"Failed to create health metric: {str(e)}", status_code=400)    


  @staticmethod
  def get(health_metric_id: uuid.UUID):
    try:
      record = HealthMetricRepository.get_by_id(health_metric_id)      
      return record
    except HealthMetric.DoesNotExist:
      raise HealthMetricNotFoundError(health_metric_id)    


  @staticmethod
  def list():
    record = HealthMetricRepository.list_all()
    return record


  @staticmethod
  def update(health_metric_id: uuid.UUID, health_metric_in: HealthMetricIn):        
    if health_metric_in.gender not in ["male", "female"]:
      raise InvalidGenderError(health_metric_in.gender)
    
    try:
      record = HealthMetricRepository.update(health_metric_id, health_metric_in)
    except HealthMetric.DoesNotExist:
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to update health metric: {str(e)}", status_code=400)    

    return record


  @staticmethod
  def delete(health_metric_id: uuid.UUID):        
    try:
      HealthMetricRepository.delete(health_metric_id)
    except HealthMetric.DoesNotExist:
      raise HealthMetricNotFoundError(health_metric_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to delete health metric: {str(e)}", status_code=400)