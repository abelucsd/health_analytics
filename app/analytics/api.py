from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from django.core.files.uploadedfile import UploadedFile
import uuid
from django.shortcuts import get_object_or_404
from health_metrics.models import HealthMetric
from analytics.xgboost.predict import run_shap
import uuid


router = Router()


@router.get("/explain/{id}")
def explain_features(request, id: str, model_type: str):
  """
    Explains feature importance by running SHAP analysis on a row data.
  """
  print("[analytics.api] GET explain_features")
  id = uuid.UUID(id)
  shap_vals = run_shap(id, model_type)
  pass


@router.get("")
def get(request):
  pass