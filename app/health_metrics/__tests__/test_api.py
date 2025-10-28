import json
import pytest
import uuid
from django.forms.models import model_to_dict
from health_metrics.schemas import HealthMetricIn, HealthMetricOut
from health_metrics.models import HealthMetric
from .fixtures import health_metric_factory, mock_record_data
from core.tests.conftest import authenticated_client, mock_authenticate

# Create your tests here.

class TestHealthMetrics:

    
  def test_create(self, authenticated_client, mocker, mock_record_data):
    payload = mock_record_data.mock_payload()
    mock_record = mock_record_data.mock_record()

    mocker.patch("health_metrics.api.HealthMetricService.create", return_value=mock_record)    

    response = authenticated_client.post(
      "/api/health_metrics/",
      data=json.dumps(payload),
    )

    assert response.status_code == 200
    assert response.json() == {"id": str(mock_record.id)}

  
  def test_get_latest(self, authenticated_client, mocker, health_metric_factory):    
    qs = health_metric_factory.queryset()    
    record = qs.first()            
    mocker.patch("health_metrics.api.HealthMetricService.get_latest", return_value=record)
    
    response = authenticated_client.get(f"/api/health_metrics/latest")
    response_body = response.json()    

    assert response.status_code == 200
    assert response_body["id"] == record.id


  def test_get_second_latest(self, authenticated_client, mocker, health_metric_factory):    
    qs = health_metric_factory.queryset()    
    record = qs.first()            
    mocker.patch("health_metrics.api.HealthMetricService.get_second_latest", return_value=record)
    
    response = authenticated_client.get(f"/api/health_metrics/previous")
    response_body = response.json()    

    assert response.status_code == 200
    assert response_body["id"] == record.id

  
  def test_get_target_metrics(self, authenticated_client, mocker):
    target_metrics = ["bmi", "blood_pressure", "heart_rate", "cholesterol", "glucose", "insulin", "stress_level"]
    mocker.patch("health_metrics.api.HealthMetricService.get_target_metrics", return_value=target_metrics)
    response = authenticated_client.get(f"/api/health_metrics/target_metrics")
    response_body = response.json()
    assert response.status_code == 200
    assert all(metric in target_metrics for metric in response_body)

    
  def test_get(self, authenticated_client, mocker, health_metric_factory):
    health_metric_factory.create()
    qs = health_metric_factory.queryset()    
    record = qs.first()    
    mocker.patch("health_metrics.api.HealthMetricService.get", return_value=record)
    
    response = authenticated_client.get(f"/api/health_metrics/{record.id}")
    response_body = response.json()    

    assert response.status_code == 200
    assert response_body["id"] == record.id

    
  def test_list_mock(self, authenticated_client, mocker, health_metric_factory):

    health_metric_factory.create()
    qs = health_metric_factory.queryset()
    record_list = health_metric_factory.list()
    mocker.patch("health_metrics.api.HealthMetricService.list", return_value=qs)
    
    response = authenticated_client.get("/api/health_metrics/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["items"][0]["weight"] == record_list[0].weight

    
  def test_update(self, authenticated_client, mocker, health_metric_factory, mock_record_data):
    payload = mock_record_data.mock_payload()
    health_metric_factory.create()
    qs = health_metric_factory.queryset()    
    record = qs.first()
    updated_record: HealthMetricIn = {      
      "age": record.age,
      "gender": record.gender,
      "height": record.height,
      "weight": record.weight + 10,
      "bmi": 22.9,   

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

    mocker.patch("health_metrics.api.HealthMetricService.update", return_value={"id": uuid.uuid4(), **updated_record})

    response = authenticated_client.put(f"/api/health_metrics/{str(record.id)}", data=json.dumps(updated_record))
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["weight"] == updated_record["weight"]

  
  def test_delete_user(self, authenticated_client, mocker, health_metric_factory):
    health_metric_factory.create()
    qs = health_metric_factory.queryset()
    record = qs.first()
    deleted_record = model_to_dict(record)
    mocker.patch("health_metrics.api.HealthMetricService.delete", return_value=None)

    response = authenticated_client.delete(f"/api/health_metrics/{record.id}")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["success"] == True