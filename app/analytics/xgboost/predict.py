import logging
import os
import uuid
import shap
import pandas as pd
import numpy as np
import xgboost as xgb
from .preprocess import preprocess_queryset


logger = logging.getLogger("analytics")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)

def run_shap(id: uuid.UUID, model_type: str):
  """
  Run SHAP explainability on a trained model.
  Returns feature importances in a JSON format.
  """
  try:
    # Load the model
    logger.debug("[run_shap] Loading the model")    
    booster = xgb.Booster()
    booster.load_model(os.path.join(MODEL_PATH, f"xgb_model_{model_type}.json"))    

    logger.debug("[run_shap] Setting SHAP")    
    # Setup SHAP
    explainer = shap.TreeExplainer(booster)

    logger.debug("[run_shap] Preprocess the database row")    
    # Preprocess row data
    row = preprocess_queryset(id, booster.feature_names)

    logger.debug("[run_shap] Execute SHAP analysis")    
    # Execute shap analysis
    shap_values = explainer.shap_values(row)
    
    logger.debug("[run_shap] Set feature_importance data.")    
    feature_importance = pd.DataFrame({
      "feature": row.columns,
      "importance": np.abs(shap_values).flatten()
    })
    
    # sort descending according to feature importance.
    feature_importance = feature_importance.sort_values(by="importance", ascending=False)

    logger.debug("[run_shap] Complete")    

    # To JSON format
    return feature_importance.to_dict(orient="records")
  except Exception as e:  
    logger.error("[run_shap] Error", exc_info=True)
    return {"error": str(e)}