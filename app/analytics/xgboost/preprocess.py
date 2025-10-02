# TODO: Test with a table
import uuid
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import shap
from sklearn.metrics import mean_squared_error, r2_score
from analytics.xgboost.import_dataset import import_dataset
from health_metrics.models import HealthMetric

TARGET_FIELDS = ["bmi", "blood_pressure", "heart_rate", "cholesterol", "glucose", "insulin", "stress_level"]
CATEGORICAL_COLS = ['gender', 'sleep_quality', 'alcohol_consumption', 'smoking_level', 'diet_type', 'exercise_type', 'sunlight_exposure']


def preprocess(result_field: str):
  # Load from DB
  # health_metrics_qs = HealthMetricService.list()
  # df = pd.DataFrame(list(health_metrics_qs))

  # Load the dataset into Pandas
  df_unfiltered = import_dataset()

  # Drop unnecessary columns
  columns_to_keep = [
    "age",
    "gender",
    "height",
    "weight",
    "bmi",
    "blood_pressure",
    "heart_rate",
    "cholesterol",
    "glucose",
    "insulin",
    "stress_level",
    "sleep_hours",
    "sleep_quality",
    "work_hours",
    "physical_activity",
    "daily_steps",
    "calorie_intake",
    "alcohol_consumption",
    "smoking_level",
    "water_intake",
    "diet_type",
    "exercise_type",
    "sunlight_exposure",
  ]
  df = df_unfiltered[columns_to_keep].copy()


  # Preprocess
  # Drop the result fields    
  if result_field not in TARGET_FIELDS:
    raise ValueError(f"The input result attribute {result_field} does not exist in the dataset or result fields.")  
  X = df.drop(columns=TARGET_FIELDS)
  y = df[result_field]

  # One-hot encode string/categorical features
  categorical_cols = ['gender', 'sleep_quality', 'alcohol_consumption', 'smoking_level', 'diet_type', 'exercise_type', 'sunlight_exposure']
  categorical_cols = [c for c in categorical_cols if c in X.columns]
  X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
  
  return X, y


def preprocess_queryset(id: uuid.UUID):
  """
  Query 1 row from HealthMetric database for analysis.
  """
  try:
    # Load the dataset into Pandas
    qs = HealthMetric.objects.get(id=id)    
    

    # Drop unnecessary columns
    columns_to_keep = [
      "age",
      "gender",
      "height",
      "weight",
      "bmi",
      "blood_pressure",
      "heart_rate",
      "cholesterol",
      "glucose",
      "insulin",
      "stress_level",
      "sleep_hours",
      "sleep_quality",
      "work_hours",
      "physical_activity",
      "daily_steps",
      "calorie_intake",
      "alcohol_consumption",
      "smoking_level",
      "water_intake",
      "diet_type",
      "exercise_type",
      "sunlight_exposure",
    ]  

    df = pd.DataFrame([{col: getattr(qs, col) for col in columns_to_keep}])
    print(df.columns)

    # Drop other target fields
    targets = [r for r in TARGET_FIELDS]
    df = df.drop(columns=targets)

    # One-hot encode categorical columns
    categorical_cols = [c for c in CATEGORICAL_COLS if c in df.columns]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    print(df.columns)

    return df
  except Exception as e:
    print(f"[preprocess_queryset] Error: {e}")
    return {"error": str(e)}