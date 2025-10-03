import logging
import uuid
from analytics.xgboost.predict import run_shap


logger = logging.getLogger("analytics")


class AnalyticsService:
  @staticmethod
  def explain_features(id: uuid.UUID, model_type: str):
    """
      Use SHAP analysis to explain the feature importance.      
    """
    logger.debug("[explain_features] id:%s, model_type:%s", id, model_type)
    shap_vals = run_shap(id, model_type)  
    logger.debug("[explain_features] id:%s, model_type:%s success", id, model_type)
    return shap_vals