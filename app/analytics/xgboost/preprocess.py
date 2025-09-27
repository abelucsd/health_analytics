# TODO: Test with a table

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import shap
from sklearn.metrics import mean_squared_error, r2_score
from health_metrics.models import HealthMetric
from health_metrics.service import HealthMetricService


def preprocess(result_field: str):
  # Load from DB
  health_metrics_qs = HealthMetricService.list()
  df = pd.DataFrame(list(health_metrics_qs))


  # Preprocess
  # drop the result fields?
  X = df.drop(columns=["id", "bmi", "blood_pressure", "heart_rate", "cholesterol", "glucose", "insulin", "stress_level"])
  y = df[result_field]

  # One-hot encode string/categorical features
  categorical_cols = ['gender', 'sleep_quality', 'alcohol_consumption', 'smoking_level', 'diet_type', 'exercise_type', 'sunlight_exposure']
  X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
  
  return {X, y}