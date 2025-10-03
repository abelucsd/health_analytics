import pytest
import os
import uuid
import xgboost as xgb
from core.tests.conftest import authenticated_client, mock_authenticate
from .fixtures import HealthMetricFactory
from analytics.xgboost.predict import run_shap


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "xgboost", "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)


@pytest.mark.django_db
class TestAnalyticsE2E:
  def test_explain_features(self, authenticated_client, mocker):
    factory = HealthMetricFactory()
    health_metric = factory.create(db=True)    
    id = health_metric.id
    model_type = "bmi"

    response = authenticated_client.get(
      f"/api/analytics/explain/{id}?model_type={model_type}",      
    )

    response_body = response.json()

    assert response.status_code == 200    
    
    for item in response_body:
      assert "feature" in item
      assert "importance" in item