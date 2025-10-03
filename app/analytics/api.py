import logging
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
logger = logging.getLogger("analytics")


@router.get("/explain/{id}")
def explain_features(request, id: str, model_type: str):
  """
    Explains feature importance by running SHAP analysis on a row data.
  """
  print("[analytics.api] GET explain_features")
  try:
    logger.info("API GET /explain/%s", id)
    id = uuid.UUID(id)
    shap_vals = AnalyticsService.explain_features(id, model_type)  
    logger.info("API GET /explain/%s 200 OK", id)
    return shap_vals
  except ValueError as e:
    logger.error("Error", exc_info=True)
    return JsonResponse({"error": "Sample not found"}, status=404)
  except Exception as e:
    logger.error("Error", exc_info=True)
    return JsonResponse({"error": "Internal server error"}, status=500)