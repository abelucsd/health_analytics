import pytest
import os
import uuid
import xgboost as xgb
from .fixtures import HealthMetricFactory
from analytics.xgboost.predict import run_shap
from analytics.xgboost.preprocess import preprocess_queryset


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "xgboost", "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)


class TestXGBoostPreprocess:
  def test_preprocess_queryset(self, mocker):
    factory = HealthMetricFactory()
    health_metric = factory.create()
    id = health_metric.id
    model_type = "bmi"

    booster = xgb.Booster()
    booster.load_model(os.path.join(MODEL_PATH, f"xgb_model_{model_type}.json"))

    mocker.patch("health_metrics.models.HealthMetric.objects.get", return_value=health_metric)

    df = preprocess_queryset(id, booster.feature_names)

    features = list(df.columns)

    assert set(features) == set(booster.feature_names)