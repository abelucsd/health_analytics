import pytest
import uuid
from health_metrics.models import HealthMetric
from health_metrics.schemas import HealthMetricIn

@pytest.fixture
@pytest.mark.django_db
def clean_db():
  HealthMetric.objects.all().delete()
  yield
  HealthMetric.objects.all().delete()


@pytest.fixture
@pytest.mark.django_db
def health_metric_factory(mocker):
  class FakeQuerySet(list):
    def first(self):
      return self[0] if self else None
    
    def __repr__(self):
      return f"<QuerySet {list.__repr__(self)}>"
    
  class HealthMetricFactory:    
    def create(self, save_to_db=False, **kwargs):
      defaults = {
        "id": str(uuid.uuid4()),         # UUID as string
        "age": 30,                       # typical adult
        "gender": "male",                # or "Female"/"Other"
        "height": 175.0,                 # cm
        "weight": 150.0,                  # kg
        "bmi": 22.25,

        # results
        "blood_pressure": 120.0,         # systolic mmHg (normal ~120/80)
        "heart_rate": 72.0,              # bpm (normal 60–100)
        "cholesterol": 180.0,            # mg/dL (desirable <200)
        "glucose": 90.0,                 # mg/dL fasting (normal 70–99)
        "insulin": 10.0,                 # µIU/mL (normal ~2–25)
        "stress_level": 3,               # scale 1–10 (low–moderate)

        # lifestyle choices
        "sleep_hours": 7.5,              # hrs/day (7–9 healthy)
        "sleep_quality": "Good",         # Poor / Fair / Good / Excellent
        "work_hours": 8.0,               # hrs/day
        "physical_activity": 4.0,        # hrs/week (moderate 3–5)
        "daily_steps": 8000,             # steps/day (7k–10k ideal)
        "calorie_intake": 2200.0,        # kcal/day (avg adult male)
        "alcohol_consumption": "Low",    # None / Low / Moderate / High
        "smoking_level": "None",         # None / Light / Moderate / Heavy
        "water_intake": 2.5,             # liters/day (2–3L healthy)
        "diet_type": "Balanced",         # Balanced / Vegan / Keto / etc.
        "exercise_type": "Cardio",       # Cardio / Strength / Mixed
        "sunlight_exposure": "Moderate"  # Low / Moderate / High
      }
      defaults.update(kwargs)
      obj = HealthMetric(**defaults)
      if save_to_db:
        # obj = HealthMetric.objects.create(**defaults)
        obj.save()
        if "created_at" in kwargs:
          obj.created_at = kwargs["created_at"]
          obj.save(update_fields=["created_at"])          
      return obj
      # return HealthMetric(**defaults)
        
    def queryset(self):      
      return FakeQuerySet([self.create()])

    def list(self):
      return [self.create()]
    
  return HealthMetricFactory()


@pytest.fixture
@pytest.mark.django_db
def mock_record_data():
  class MockRecordData():
    def __init__(self):
      self.data = {        
        "age": 30,                       # typical adult
        "gender": "male",                # or "Female"/"Other"
        "height": 175.0,                 # cm
        "weight": 150.0,                  # kg
        "bmi": 22.25,

        # results
        "blood_pressure": 120.0,         # systolic mmHg (normal ~120/80)
        "heart_rate": 72.0,              # bpm (normal 60–100)
        "cholesterol": 180.0,            # mg/dL (desirable <200)
        "glucose": 90.0,                 # mg/dL fasting (normal 70–99)
        "insulin": 10.0,                 # µIU/mL (normal ~2–25)
        "stress_level": 3,               # scale 1–10 (low–moderate)

        # lifestyle choices
        "sleep_hours": 7.5,              # hrs/day (7–9 healthy)
        "sleep_quality": "Good",         # Poor / Fair / Good / Excellent
        "work_hours": 8.0,               # hrs/day
        "physical_activity": 4.0,        # hrs/week (moderate 3–5)
        "daily_steps": 8000,             # steps/day (7k–10k ideal)
        "calorie_intake": 2200.0,        # kcal/day (avg adult male)
        "alcohol_consumption": "Low",    # None / Low / Moderate / High
        "smoking_level": "None",         # None / Light / Moderate / Heavy
        "water_intake": 2.5,             # liters/day (2–3L healthy)
        "diet_type": "Balanced",         # Balanced / Vegan / Keto / etc.
        "exercise_type": "Cardio",       # Cardio / Strength / Mixed
        "sunlight_exposure": "Moderate"  # Low / Moderate / High
      }
    
    def mock_payload(self) -> HealthMetricIn:
      return self.data.copy()

    def mock_record_in(self):
      return HealthMetricIn(**self.data)
    
    def mock_record(self):
      return HealthMetric(id=uuid.uuid4(), **self.data)
          
  return MockRecordData()