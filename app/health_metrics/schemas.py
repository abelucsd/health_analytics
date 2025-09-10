from uuid import UUID
from typing import Optional
from health_metrics.models import HealthMetricsGenderChoices
from ninja import Schema

class HealthMetricsIn(Schema):
  age = int
  gender = Optional[HealthMetricsGenderChoices] = HealthMetricsGenderChoices.MALE
  height = float
  weight = float

  # results
  blood_pressure = Optional[float] = None
  heart_rate = Optional[float] = None
  cholesterol = Optional[float] = None
  glucose = Optional[float] = None
  insulin = Optional[float] = None
  stress_level = Optional[int] = None

  # lifestyle choices
  sleep_hours = float
  sleep_quality = str
  work_hours = float
  physical_activity = float
  daily_steps = int
  calorie_intake = float
  alcohol_consumption = str
  smoking_level = str
  water_intake = float
  diet_type = str
  exercise_type = str
  sunlight_exposure = str

  class Config:
    extra = "forbid"


class HealthMetricsOut(Schema):
  id = UUID
  age = int
  gender = str
  height = float
  weight = float

  bmi = float

  # results
  blood_pressure = Optional[float] = None
  heart_rate = Optional[float] = None
  cholesterol = Optional[float] = None
  glucose = Optional[float] = None
  insulin = Optional[float] = None
  stress_level = Optional[int] = None

  # lifestyle choices
  sleep_hours = float
  sleep_quality = str
  work_hours = float
  physical_activity = float
  daily_steps = int
  calorie_intake = float
  alcohol_consumption = str
  smoking_level = str
  water_intake = float
  diet_type = str
  exercise_type = str
  sunlight_exposure = str

  class Config:
    extra = "forbid"