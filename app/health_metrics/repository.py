import uuid
from health_metrics.schemas import HealthMetricIn
from health_metrics.models import HealthMetric


class HealthMetricRepository:
  @staticmethod
  def create(health_metric_in: HealthMetricIn):
    health_metric_in_dict = health_metric_in.dict()
    return HealthMetric.objects.create(**health_metric_in_dict)
  

  @staticmethod
  def get_by_id(health_metric_id):
    return HealthMetric.objects.get(id=health_metric_id)
  

  @staticmethod
  def list_all():
    return HealthMetric.objects.all()
  

  @staticmethod
  def get_latest():
    return HealthMetric.objects.latest('created_at')
  
  
  @staticmethod
  def get_second_latest():
    return HealthMetric.objects.order_by('-created_at')[1]
  
  
  @staticmethod
  def update(health_metric_id: uuid.UUID, health_metric_in: HealthMetricIn):
    record = HealthMetric.objects.get(id=health_metric_id)
    for attr, value in health_metric_in.dict().items():
      setattr(record, attr, value)
    record.save()
    return record
  

  @staticmethod
  def delete(health_metric_id: uuid.UUID):
    record = HealthMetric.objects.get(id=health_metric_id)
    record.delete()