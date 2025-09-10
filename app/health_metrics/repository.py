import uuid
from .schemas import HealthMetric
from .models import HealthMetric


class HealthMetricRepository:
  @staticmethod
  def create(health_metric_in: HealthMetric):
    health_metric_in_dict = health_metric_in.dict()
    return HealthMetric.objects.create(**health_metric_in_dict)
  

  @staticmethod
  def get_by_id(health_metric_id):
    return HealthMetric.objects.get(id=health_metric_id)
  

  @staticmethod
  def list_all():
    return HealthMetric.objects.all()
  
  
  @staticmethod
  def update(health_metric_id: uuid.UUID, health_metric_in: HealthMetric):
    record = HealthMetric.objects.get(id=health_metric_id)
    for attr, value in health_metric_in.dict().items():
      setattr(record, attr, value)
    record.save()
    return record
  

  @staticmethod
  def delete(health_metric_id: uuid.UUID):
    record = HealthMetric.objects.get(id=health_metric_id)
    record.delete()