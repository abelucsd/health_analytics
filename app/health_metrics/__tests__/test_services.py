from health_metrics.models import HealthMetric
import pytest
import uuid
from django.forms.models import model_to_dict
from health_metrics.service import HealthMetricService
from .fixtures import health_metric_factory, mock_record_data

class TestHealthServiceService:
  def test_create(self, mocker, mock_record_data):
    payload = mock_record_data.mock_record_in()
    mock_record = mock_record_data.mock_record()
    mocker.patch("health_metrics.service.HealthMetricRepository.create", return_value=mock_record)

    record = HealthMetricService.create(payload)

    assert record == mock_record


  def test_get(self, mocker, mock_record_data):
    mock_record = mock_record_data.mock_record()
    mocker.patch("health_metrics.service.HealthMetricRepository.get_by_id", return_value=mock_record)

    record = HealthMetricService.get(mock_record.id)

    assert record == mock_record


  def test_list(self, mocker, health_metric_factory):
    health_metric_factory.create()
    qs = health_metric_factory.queryset()        

    mocker.patch("health_metrics.service.HealthMetricRepository.list_all", return_value=qs)

    records = HealthMetricService.list()

    assert records == qs


  def test_latest(self, mocker, mock_record_data):
    mock_record = mock_record_data.mock_record()
    mocker.patch("health_metrics.service.HealthMetricRepository.get_latest", return_value=mock_record)

    record = HealthMetricService.get_latest()

    assert record == mock_record

  
  def test_second_latest(self, mocker, mock_record_data):
    mock_record = mock_record_data.mock_record()
    mocker.patch("health_metrics.service.HealthMetricRepository.get_second_latest", return_value=mock_record)

    record = HealthMetricService.get_second_latest()

    assert record == mock_record


  def test_update(self, mocker, mock_record_data):
    mock_record = mock_record_data.mock_record()
    mock_record_in = mock_record_data.mock_record_in()

    # update through payload
    mock_record_in.weight += 10

    # mock the update
    updated_record = mock_record
    mock_record.weight += 10

    mocker.patch("health_metrics.service.HealthMetricRepository.update", return_value=updated_record)

    result = HealthMetricService.update(mock_record.id, mock_record_in)

    assert result.weight == updated_record.weight


  def test_delete(self, mocker, mock_record_data):
    mock_record = mock_record_data.mock_record()

    mocker.patch("health_metrics.service.HealthMetricRepository.delete")

    result = HealthMetricService.delete(mock_record.id)

    assert result is None