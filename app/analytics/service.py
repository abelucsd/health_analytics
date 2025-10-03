import uuid
from analytics.xgboost.predict import run_shap


class AnalyticsService:
  @staticmethod
  def explain_features(id: uuid.UUID, model_type: str):
    """
      Use SHAP analysis to explain the feature importance.      
    """
    shap_vals = run_shap(id, model_type)  
    return shap_vals