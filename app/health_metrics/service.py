import uuid
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from app.health_metrics.exceptions import HealthMetricsNotFoundError, InvalidGenderError
from .schemas import HealthMetricsIn, HealthMetricsOut
from .models import HealthMetrics
from .repository import HealthMetricsRepository
from core.exceptions import AppError, ValidationError

class HealthMetricsService:
  @staticmethod
  def create(health_metrics_in: HealthMetricsIn):
    try:      
      record = HealthMetricsRepository.create(health_metrics_in)
      return record
    except IntegrityError as e:
      raise ValidationError(f"Failed to create health metrics: {str(e)}", status_code=400)    


  @staticmethod
  def get(health_metrics_id: uuid.UUID):
    try:
      record = HealthMetricsRepository.get_by_id(health_metrics_id)      
      return record
    except HealthMetrics.DoesNotExist:
      raise HealthMetricsNotFoundError(health_metrics_id)    


  @staticmethod
  def list():
    record = HealthMetricsRepository.list_all()
    return record


  @staticmethod
  def update(health_metrics_id: uuid.UUID, health_metrics_in: HealthMetricsIn):        
    if health_metrics_in.gender not in ["user", "admin"]:
      raise InvalidGenderError(health_metrics_in.gender)
    
    try:
      record = HealthMetricsRepository.update(health_metrics_id, health_metrics_in)
    except HealthMetrics.DoesNotExist:
      raise HealthMetricsNotFoundError(health_metrics_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to update health metrics: {str(e)}", status_code=400)    

    return record


  @staticmethod
  def delete(health_metrics_id: uuid.UUID):        
    try:
      HealthMetricsRepository.delete(health_metrics_id)
    except HealthMetrics.DoesNotExist:
      raise HealthMetricsNotFoundError(health_metrics_id)
    except IntegrityError as e:
      raise ValidationError(f"Failed to delete health metrics: {str(e)}", status_code=400)