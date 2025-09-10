import uuid
from .schemas import HealthMetricsIn
from .models import HealthMetrics


class HealthMetricsRepository:
  @staticmethod
  def create(health_metrics_in: HealthMetricsIn):
    health_metrics_in_dict = health_metrics_in.dict()
    return HealthMetrics.objects.create(**health_metrics_in_dict)
  

  @staticmethod
  def get_by_id(health_metrics_id):
    return HealthMetrics.objects.get(id=health_metrics_id)
  

  @staticmethod
  def list_all():
    return HealthMetrics.objects.all()
  
  
  @staticmethod
  def update(health_metrics_id: uuid.UUID, health_metrics_in: HealthMetricsIn):
    record = HealthMetrics.objects.get(id=health_metrics_id)
    for attr, value in health_metrics_in.dict().items():
      setattr(record, attr, value)
    record.save()
    return record
  

  @staticmethod
  def delete(health_metrics_id: uuid.UUID):
    record = HealthMetrics.objects.get(id=health_metrics_id)
    record.delete()