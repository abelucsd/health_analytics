from uuid import UUID
from typing import Optional, List, Dict, Any
from health_metrics.models import HealthMetricGenderChoices
from ninja import Schema

class HealthMetricIn(Schema):
  age : int
  gender : Optional[HealthMetricGenderChoices]
  height : float
  weight : float
  bmi: Optional[float]

  # results
  blood_pressure : Optional[float]
  heart_rate : Optional[float] 
  cholesterol : Optional[float] 
  glucose : Optional[float] 
  insulin : Optional[float] 
  stress_level : Optional[int] 

  # lifestyle choices
  sleep_hours : float
  sleep_quality : str
  work_hours : float
  physical_activity : float
  daily_steps : int
  calorie_intake : float
  alcohol_consumption : str
  smoking_level : str
  water_intake : float
  diet_type : str
  exercise_type : str
  sunlight_exposure : str

  class Config:
    extra = "forbid"


class HealthMetricOut(Schema):
  id : UUID
  age : int
  gender : Optional[HealthMetricGenderChoices]
  height : float
  weight : float

  bmi : float

  # results
  blood_pressure : Optional[float] 
  heart_rate : Optional[float] 
  cholesterol : Optional[float] 
  glucose : Optional[float] 
  insulin : Optional[float] 
  stress_level : Optional[int] 

  # lifestyle choices
  sleep_hours : float
  sleep_quality : str
  work_hours : float
  physical_activity : float
  daily_steps : int
  calorie_intake : float
  alcohol_consumption : str
  smoking_level : str
  water_intake : float
  diet_type : str
  exercise_type : str
  sunlight_exposure : str

  ranges: Dict[str, Any] = None

  class Config:
    extra = "forbid"
    orm_mode = True


class HealthMetricListOut(Schema):
  items: List[HealthMetricOut]
  ranges: Dict[str, Any]