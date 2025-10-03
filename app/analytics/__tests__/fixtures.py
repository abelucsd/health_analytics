from typing import Dict, List
import uuid
from unittest.mock import MagicMock


class HealthMetricFactory:
  def __init__(self, **defaults: dict):
    self.defaults = defaults

  def create(self, **overrides) -> MagicMock:
    # Combine defaults with overrides
    attrs = {**self.defaults, **overrides}
    mock = MagicMock()
    mock.id = attrs.get("id") or uuid.uuid4()
    mock.age = attrs.get("age", 30)
    mock.gender = attrs.get("gender", "Male")
    mock.height = attrs.get("height", 175)
    mock.weight = attrs.get("weight", 150)
    mock.bmi = attrs.get("bmi", 22.3)
    mock.blood_pressure = attrs.get("blood_pressure", 120)
    mock.heart_rate = attrs.get("heart_rate", 70)
    mock.cholesterol = attrs.get("cholesterol", 180)
    mock.glucose = attrs.get("glucose", 90)
    mock.insulin = attrs.get("insulin", 10)
    mock.stress_level = attrs.get("stress_level", 3)
    mock.sleep_hours = attrs.get("sleep_hours", 7)
    mock.sleep_quality = attrs.get("sleep_quality", "Good")
    mock.work_hours = attrs.get("work_hours", 8)
    mock.physical_activity = attrs.get("physical_activity", 4)
    mock.daily_steps = attrs.get("daily_steps", 8000)
    mock.calorie_intake = attrs.get("calorie_intake", 2200)
    mock.alcohol_consumption = attrs.get("alcohol_consumption", "Low")
    mock.smoking_level = attrs.get("smoking_level", "None")
    mock.water_intake = attrs.get("water_intake", 2.5)
    mock.diet_type = attrs.get("diet_type", "Balanced")
    mock.exercise_type = attrs.get("exercise_type", "Cardio")
    mock.sunlight_exposure = attrs.get("sunlight_exposure", "Moderate")

    def _str():
      return f"HealthMetric(id={mock.id}, age={mock.age}, gender={mock.gender}, weight={mock.weight}, height={mock.height})"
    mock.__str__ = _str
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
        return {"data": mock.data}  # mimic the JSON response your endpoint returns