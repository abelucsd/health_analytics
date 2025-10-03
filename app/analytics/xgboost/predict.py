import os
import uuid
import shap
import pandas as pd
import numpy as np
import xgboost as xgb
from .preprocess import preprocess_queryset


MODEL_PATH = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.abspath(MODEL_PATH)

def run_shap(id: uuid.UUID, model_type: str):
  """
  Run SHAP explainability on a trained model.
  Returns feature importances in a JSON format.
  """
  try:
    # Load the model
    print("Loading the model")
    booster = xgb.Booster()
    booster.load_model(os.path.join(MODEL_PATH, f"xgb_model_{model_type}.json"))    

    print("Setting SHAP")
    # Setup SHAP
    explainer = shap.TreeExplainer(booster)

    print("Preprocess the database row")
    # Preprocess row data
    row = preprocess_queryset(id, booster.feature_names)  

    print("Execute SHAP analysis")
    # Execute shap analysis
    shap_values = explainer.shap_values(row)
    

    print("Set feature_importance data.")
    feature_importance = pd.DataFrame({
      "feature": row.columns,
      "importance": np.abs(shap_values).flatten()
    })
    
    # sort descending according to feature importance.
    feature_importance = feature_importance.sort_values(by="importance", ascending=False)

    print("Complete")    

    # To JSON format
    return feature_importance.to_dict(orient="records")
  except Exception as e:  
    print(f"[run_shap] Error: {e}")
    return {"error": str(e)}