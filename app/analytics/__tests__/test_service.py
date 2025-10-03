import pytest
import os
import uuid
import xgboost as xgb
from .fixtures import HealthMetricFactory
from analytics.xgboost.predict import run_shap
from analytics.service import AnalyticsService


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "xgboost", "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)


class TestAnalyticsService:
  def test_explain_features(self, mocker):
    factory = HealthMetricFactory()
    health_metric = factory.create()
    id = health_metric.id
    model_type = "bmi"

    mocker.patch("health_metrics.models.HealthMetric.objects.get", return_value=health_metric)

    result = AnalyticsService.explain_features(id, model_type)

    top_3 = [f["feature"] for f in result[:3]]

    assert "weight" in top_3
