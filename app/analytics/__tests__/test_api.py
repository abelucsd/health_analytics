import pytest
import os
import uuid
import xgboost as xgb
from core.tests.conftest import authenticated_client, mock_authenticate
from .fixtures import ShapValuesFactory
from analytics.xgboost.predict import run_shap


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "xgboost", "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)


class TestAnalyticsApi:
  def test_explain_features(self, authenticated_client, mocker):        
    mock_shap_values = ShapValuesFactory.create()
    model_type = "bmi"

    mocker.patch("analytics.service.AnalyticsService.explain_features", return_value=mock_shap_values)

    response = authenticated_client.get(
      f"/api/analytics/explain/{uuid.uuid4()}?model_type={model_type}",      
    )    

    response_body = response.json()

    assert response.status_code == 200

    data = response_body["data"]
    for item in data:
        assert "feature" in item
        assert "importance" in item
    
    top_3 = [f["feature"] for f in response_body['data'][:3]]

    assert "weight" in top_3    


  def test_explain_features_invalid_id(self, authenticated_client):
    model_type = "bmi"
    response = authenticated_client.get(f"/api/analytics/explain/invalid-uuid?model_type={model_type}")
    assert response.status_code == 404
    assert "error" in response.json()


  def test_explain_features_missing_model_type(self, authenticated_client):
    response = authenticated_client.get(f"/api/analytics/explain/{uuid.uuid4()}")
    assert response.status_code == 422


  def test_explain_features_service_error(self, authenticated_client, mocker):
    model_type = "bmi"
    mocker.patch(
      "analytics.service.AnalyticsService.explain_features",
      side_effect=Exception("Something went wrong")
    )
    response = authenticated_client.get(f"/api/analytics/explain/{uuid.uuid4()}?model_type={model_type}")
    assert response.status_code == 500
    assert "error" in response.json()