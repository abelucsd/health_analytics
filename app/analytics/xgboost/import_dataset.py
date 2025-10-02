import os
import kagglehub
import pandas as pd
import glob


def import_dataset():
  # 1. Download latest version
  path = kagglehub.dataset_download("mahdimashayekhi/disease-risk-from-daily-habits")

  print("Path to dataset files:", path)

  # 2. Look for the CSV inside the folder
  # csv_files = glob.glob(os.path.join(path, "*.csv"))
  # if not csv_files:
  #     raise FileNotFoundError(f"No CSV files found in {path}")

  # 2. Load into pandas
  df = pd.read_csv(f"{path}\health_lifestyle_classification.csv")

  return df