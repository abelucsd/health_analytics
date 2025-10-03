from typing import List
from ninja import NinjaAPI, Schema
from ninja import Router
from ninja.responses import JsonResponse
from django.core.files.uploadedfile import UploadedFile
import uuid
from django.shortcuts import get_object_or_404
from health_metrics.models import HealthMetric
from analytics.xgboost.predict import run_shap
from .service import AnalyticsService


router = Router()


@router.get("/explain/{id}")
def explain_features(request, id: str, model_type: str):
  """
    Explains feature importance by running SHAP analysis on a row data.
  """
  print("[analytics.api] GET explain_features")
  try:
    id = uuid.UUID(id)
    shap_vals = AnalyticsService.explain_features(id, model_type)  
    return JsonResponse({"data": shap_vals}, status=200)
  except ValueError:
    return JsonResponse({"error": "Sample not found"}, status=404)
  except Exception:
    return JsonResponse({"error": "Internal server error"}, status=500)