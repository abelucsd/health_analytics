from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from ninja.files import File
from django.core.files.uploadedfile import UploadedFile
import uuid
from django.shortcuts import get_object_or_404
from app.health_metrics.models import HealthMetric
from xgboost.predict import run_shap
import uuid


router = Router()


@router.get("/explain/{id}")
def explain_features(request, id: int, model_type: str):
  """
    Explains feature importance by running SHAP analysis on a row data.
  """  
  shap_vals = run_shap(id, model_type)
  pass


@router.get("")
def get(request):
  pass