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