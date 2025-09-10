import uuid
from django.db import models

# Create your models here.

class HealthMetricGenderChoices(models.TextChoices):
  MALE = "male",
  FEMALE = "female"


class HealthMetric(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  age = models.IntegerField(default=20)
  gender = models.CharField(
    max_length = 10,
    choices = HealthMetricGenderChoices.choices,
    default = HealthMetricGenderChoices.USER,
  )


  height = models.FloatField(help_text="Height in cm")
  weight = models.FloatField(help_text="Weight in lbs")
  bmi = models.FloatField()
  
  # results
  blood_pressure = models.FloatField(null=True, blank=True)
  heart_rate = models.FloatField(null=True, blank=True)
  cholesterol = models.FloatField(null=True, blank=True)
  glucose = models.FloatField(null=True, blank=True)
  insulin = models.FloatField(null=True, blank=True)
  stress_level = models.IntegerField(null=True, blank=True)

  # lifestyle choices
  sleep_hours = models.FloatField()
  sleep_quality = models.CharField(max_length=20)

  work_hours = models.FloatField()
  physical_activity = models.FloatField()
  daily_steps = models.IntegerField()

  calorie_intake = models.FloatField()
  alcohol_consumption = models.CharField(max_length=20)
  smoking_level = models.CharField(max_length=20)
  water_intake = models.FloatField()

  diet_type = models.CharField(max_length=100)
  exercise_type = models.CharField(max_length=100)
  sunlight_exposure = models.CharField(max_length=100)

  created_at = models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return f"{self.survey_code} - {self.age}y"
  

