import pytest
import os
import uuid
import xgboost as xgb
from .fixtures import HealthMetricFactory
from analytics.xgboost.predict import run_shap

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "xgboost", "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)


class TestXGBoostPredict:
  def test_run_shap(self, mocker):
    factory = HealthMetricFactory()
    health_metric = factory.create()
    id = health_metric.id
    model_type = "bmi"    

    mocker.patch("health_metrics.models.HealthMetric.objects.get", return_value=health_metric)

    shap_vals = run_shap(id, model_type)

    # It is known that weight should be in the top 3.
    top_3 = [f["feature"] for f in shap_vals[:3]]

    assert "weight" in top_3