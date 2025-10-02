from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from ninja.files import File
from django.core.files.uploadedfile import UploadedFile
import uuid
from django.shortcuts import get_object_or_404
from app.health_metrics.models import HealthMetric

router = Router()


@router.get("/explain/{id}")
def explain_features(request):
  """
    Explains feature importance by running SHAP analysis on a row data.
  """
  health_metrics = HealthMetric.objects.get(id=id)
  pass


@router.get("")
def get(request):
  pass