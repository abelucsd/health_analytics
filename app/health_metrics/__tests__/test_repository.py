import pytest
from health_metrics.models import HealthMetric
from health_metrics.schemas import HealthMetricIn
from .fixtures import health_metric_factory, mock_record_data
from health_metrics.repository import HealthMetricRepository


@pytest.mark.django_db
class TestHealthMetricRepository:
  
  def test_create(self, mock_record_data):    
    record_in = mock_record_data.mock_record_in()

    created_record = HealthMetricRepository.create(record_in)

    assert created_record.weight == record_in.weight


  def test_get_by_id(self, health_metric_factory):
    record = health_metric_factory.create()
    record.save()

    fetched_record = HealthMetricRepository.get_by_id(record.id)    

    assert fetched_record.weight == record.weight


  def test_list_all(self, health_metric_factory):
    record = health_metric_factory.create()
    record.save()

    fetched_records = HealthMetricRepository.list_all()

    assert list(fetched_records)[0].weight == record.weight

  
  def test_get_latest(self, health_metric_factory):
    record = health_metric_factory.create()
    record.save()
    record2 = health_metric_factory.create()
    record2.save()

    fetched_record = HealthMetricRepository.get_latest()

    assert fetched_record.weight == record.weight


  def test_get_second_latest(self, health_metric_factory):
    record = health_metric_factory.create()    
    record.save()
    record2 = health_metric_factory.create()
    record2.save()

    fetched_record = HealthMetricRepository.get_second_latest()

    assert fetched_record.weight == record2.weight

    
  def test_get_fields(self):
    fetched_record = HealthMetricRepository.get_fields()
    assert "bmi" in fetched_record


  def test_update(self, health_metric_factory, mock_record_data):
    record_in = mock_record_data.mock_record_in()
    record = health_metric_factory.create()
    record.save()

    record_in.weight += 10

    updated_record = HealthMetricRepository.update(record.id, record_in)

    assert updated_record.weight == record_in.weight

  
  def test_delete(self, health_metric_factory):
    record = health_metric_factory.create()
    record.save()    

    HealthMetricRepository.delete(record.id)

    with pytest.raises(HealthMetric.DoesNotExist):
      HealthMetric.objects.get(id=record.id)
    