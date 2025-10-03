import pytest
from typing import Dict, List
import uuid
from unittest.mock import MagicMock


@pytest.mark.django_db
class HealthMetricFactory:
  def __init__(self):
    self.defaults = {
      "age": 30,
      "gender": "Male",
      "height": 175,
      "weight": 150,
      "bmi": 22.3,
      "blood_pressure": 120,
      "heart_rate": 70,
      "cholesterol": 180,
      "glucose": 90,
      "insulin": 10,
      "stress_level": 3,
      "sleep_hours": 7,
      "sleep_quality": "Good",
      "work_hours": 8,
      "physical_activity": 4,
      "daily_steps": 8000,
      "calorie_intake": 2200,
      "alcohol_consumption": "Low",
      "smoking_level": "None",
      "water_intake": 2.5,
      "diet_type": "Balanced",
      "exercise_type": "Cardio",
      "sunlight_exposure": "Moderate",
    }


  def create(self, db=False, **overrides):
    # Combine defaults with overrides
    attrs = {**self.defaults, **overrides}

    if db:
      # Create real DB object
      from health_metrics.models import HealthMetric  
      health_metric_object = HealthMetric.objects.create(**attrs)      
      return health_metric_object
    
    else:        
      mock = MagicMock()        
      mock.id = attrs.get("id") or uuid.uuid4()      
      for key, value in attrs.items():
        setattr(mock, key, value)
      mock.__str__ = lambda: f"HealthMetric(id={mock.id}, age={mock.age})"
      mock.__repr__ = mock.__str__
      return mock
    
  def __str__(self):
    return f"Create the HealthMetric by calling create()"

  def __repr__(self):
    return f"Create the HealthMetric by calling create()"
  

class ShapValuesFactory:
  """
  Factory for generating mock SHAP values for tests.
  """
  DEFAULT_VALUES: List[Dict] = [
    {"feature": "weight", "importance": 14.695508003234863},
    {"feature": "height", "importance": 2.053356885910034},
    {"feature": "calorie_intake", "importance": 0.05890132859349251},
    {"feature": "daily_steps", "importance": 0.058394089341163635},
    {"feature": "age", "importance": 0.05697285011410713},
    {"feature": "sunlight_exposure_Moderate", "importance": 0.04197191447019577},
    {"feature": "water_intake", "importance": 0.038066066801548004},
    {"feature": "sleep_quality_Poor", "importance": 0.0363009013235569},
    {"feature": "work_hours", "importance": 0.03248170018196106},
    {"feature": "sleep_quality_Good", "importance": 0.027571188285946846},
    {"feature": "physical_activity", "importance": 0.02242468297481537},
    {"feature": "sleep_hours", "importance": 0.020718136802315712},
    {"feature": "exercise_type_Strength", "importance": 0.01751999743282795},
    {"feature": "alcohol_consumption_Occasionally", "importance": 0.015048571862280369},
    {"feature": "sleep_quality_Fair", "importance": 0.012916279956698418},
    {"feature": "gender_Male", "importance": 0.01206173188984394},
    {"feature": "smoking_level_Light", "importance": 0.010031787678599358},
    {"feature": "diet_type_Vegetarian", "importance": 0.008515799418091774},
    {"feature": "exercise_type_Cardio", "importance": 0.008262376300990582},
    {"feature": "gender_Female", "importance": 0.008181905373930931},
    {"feature": "diet_type_Keto", "importance": 0.008018013089895248},
    {"feature": "sunlight_exposure_Low", "importance": 0.006903063505887985},
    {"feature": "diet_type_Vegan", "importance": 0.006587192416191101},
    {"feature": "sunlight_exposure_High", "importance": 0.0035927006974816322},
    {"feature": "exercise_type_Mixed", "importance": 0.003420100314542651},
    {"feature": "diet_type_Omnivore", "importance": 0.002827789867296815},
    {"feature": "alcohol_consumption_Regularly", "importance": 0.002607239643111825},
    {"feature": "smoking_level_Non-smoker", "importance": 0.0018268561689183116},
    {"feature": "sleep_quality_Excellent", "importance": 0.0010355501435697079},
    {"feature": "smoking_level_Heavy", "importance": 0.00010722569277277216},
  ]

  @classmethod
  def create(cls, values: List[Dict] = None) -> Dict:
    """
    Returns a mock SHAP values object with `.data` containing a list of feature importance.
    """
    mock = MagicMock()
    mock.data = values or cls.DEFAULT_VALUES
    return mock.data