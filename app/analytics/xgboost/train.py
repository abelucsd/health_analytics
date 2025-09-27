from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error, r2_score
import shap
import pandas as pd
import numpy as np
from .preprocess import preprocess



def run_xgboost():
  '''
    return:      
      model (object): XGBoost Model      
  '''
  model = xgb.XGBRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
  )

  return model


def train(model, X_train, X_test, y_train, y_test):
  """
    Trains according to the model.
    Returns:
      dict:
        model (object): Trained model.
        rmse (float): Root Mean Squared Error on the test set.
        r2 (float): R-squared score on the test set.
  """
  # train step
  model.fit(X_train, y_train)

  # evaluate
  y_pred = model.predict(X_test)

  rmse = root_mean_squared_error(y_test, y_pred, squared=False)
  r2 = r2_score(y_test, y_pred)

  print(f"RMSE: {rmse: .2f}")
  print(f"R^2: {r2:.2f}")

  return {
    "model": model,
    "rmse": rmse,
    "r2": r2,
  }


def run_shap(model, X_test):
  """
  Run SHAP explainability on a trained model.
  Returns feature importances in a JSON format.
  """  
  explainer = shap.Explainer(model)
  shap_values = explainer(X_test)

  # Export numerical SHAP values as JSON
  feature_importance = pd.DataFrame({
    "feature": X_test.columns,
    "importance": np.abs(shap_values.values).mean(axis=0)
  }).sort_values(by="importance", ascending=False)

  # Convert to JSON serializable dict
  return feature_importance.to_dict(orient="records")
  

def run_lifestyle_analysis():  

  # lifestyle dataset
  X, y = preprocess()

  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
  )

  model = run_xgboost()

  result = train(model, X_train, X_test, y_train, y_test)

  shap_importance_json = run_shap(model, X_test)

  return {
    "rmse": result["rmse"],
    "r2": result["r2"],
    "feature_importance": shap_importance_json
  }
