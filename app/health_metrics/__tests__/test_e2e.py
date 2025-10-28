import json
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.forms import model_to_dict
import pytest
from health_metrics.models import HealthMetric
from health_metrics.schemas import HealthMetricIn
from .fixtures import health_metric_factory, mock_record_data, clean_db
from health_metrics.repository import HealthMetricRepository
from core.tests.conftest import authenticated_client, mock_authenticate

@pytest.mark.django_db
class TestE2EHealthMetrics:

  @classmethod
  def setUpClass(cls):
      super().setUpClass()      
      HealthMetric.objects.all().delete()
    
  @classmethod
  def tearDownClass(cls):      
      HealthMetric.objects.all().delete()
      super().tearDownClass()
  
  def test_create(self, authenticated_client, mock_record_data):
    payload = mock_record_data.mock_payload()

    response = authenticated_client.post(
      "/api/health_metrics/",
      data=json.dumps(payload)
    )
    
    assert response.status_code == 200


  def test_get_latest(self, authenticated_client, health_metric_factory):
    record = health_metric_factory.create()
    record.save()

    response = authenticated_client.get(
      f"/api/health_metrics/latest"      
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] == record.id

  
  def test_get_second_latest(self, authenticated_client, health_metric_factory, clean_db):
    record = health_metric_factory.create(created_at=datetime.datetime(2025, 10, 10, 12, 0, 0))    
    record.save()

    record2 = health_metric_factory.create(created_at=datetime.datetime(2025, 10, 10, 13, 0, 20))    
    record2.save()

    response = authenticated_client.get(
      f"/api/health_metrics/previous"      
    )
    response_body = response.json()
    print(response_body)

    assert response_body["created_at"] == str(record.created_at)


  def test_get_target_metrics(self, authenticated_client, mocker):
    target_metrics = ["bmi", "blood_pressure", "heart_rate", "cholesterol", "glucose", "insulin", "stress_level"]
    mocker.patch("health_metrics.api.HealthMetricService.get_target_metrics", return_value=target_metrics)
    response = authenticated_client.get(f"/api/health_metrics/target_metrics")
    response_body = response.json()
    assert response.status_code == 200
    assert all(metric in target_metrics for metric in response_body)


  def test_get(self, authenticated_client, health_metric_factory):
    record = health_metric_factory.create()
    record.save()

    response = authenticated_client.get(
      f"/api/health_metrics/{record.id}"      
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] == record.id


  def test_list(self, authenticated_client, health_metric_factory):
    record = health_metric_factory.create()
    record.save()
        
    record_list = health_metric_factory.list()

    response = authenticated_client.get(
      "/api/health_metrics/"
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["items"][0]["weight"] == record_list[0].weight

     
  def test_update(self, authenticated_client, health_metric_factory):
    record = health_metric_factory.create()
    record.save()

    updated_record = {      
      "age": record.age,
      "gender": record.gender,
      "height": record.height,
      "weight": record.weight + 10,
      "bmi": record.bmi,

      # results
      "blood_pressure": record.blood_pressure,
      "heart_rate": record.heart_rate,
      "cholesterol": record.cholesterol,
      "glucose": record.glucose,
      "insulin": record.insulin,
      "stress_level": record.stress_level,

      # lifestyle choices
      "sleep_hours": record.sleep_hours,
      "sleep_quality": record.sleep_quality,
      "work_hours": record.work_hours,
      "physical_activity": record.physical_activity,
      "daily_steps": record.daily_steps,
      "calorie_intake": record.calorie_intake,
      "alcohol_consumption": record.alcohol_consumption,
      "smoking_level": record.smoking_level,
      "water_intake": record.water_intake,
      "diet_type": record.diet_type,
      "exercise_type": record.exercise_type,
      "sunlight_exposure": record.sunlight_exposure
    }

    response = authenticated_client.put(
      f"/api/health_metrics/{record.id}",
      data=json.dumps(updated_record)
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["weight"] == updated_record["weight"]


  def test_delete(self, authenticated_client, health_metric_factory):
    record = health_metric_factory.create()
    record.save()
    
    response = authenticated_client.delete(
      f"/api/health_metrics/{record.id}"
    )
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["success"] == True