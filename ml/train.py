import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV

from ml.features import engineer_features, FEATURE_COLUMNS

def train_model(
    data_path: str = "data/transactions.csv",
    models_dir: str = "ml/models",
    random_state: int = 42
):
    df = pd.read_csv(data_path)

    df_dev, df_test = train_test_split(
        df, test_size=0.15, random_state=random_state, stratify=df["label"]
    )

    val_size_relative = 0.15 / 0.85
    df_train, df_val = train_test_split(
        df_dev, test_size=val_size_relative, random_state=random_state, stratify=df_dev["label"]
    )

    X_train = engineer_features(df_train)
    y_train = df_train["label"].values

    X_val = engineer_features(df_val)
    y_val = df_val["label"].values

    X_test = engineer_features(df_test)
    y_test = df_test["label"].values

    neg_count = (y_train == 0).sum()
    pos_count = (y_train == 1).sum()
    scale_pos_weight = neg_count / max(pos_count, 1)

    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "boosting_type": "gbdt",
        "n_estimators": 350,
        "learning_rate": 0.04,
        "num_leaves": 31,
        "max_depth": 6,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "scale_pos_weight": scale_pos_weight * 0.75,
        "random_state": random_state,
        "n_jobs": -1,
        "verbose": -1
    }

    base_model = lgb.LGBMClassifier(**params)
    base_model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(stopping_rounds=30, verbose=False)]
    )

    calibrated_model = CalibratedClassifierCV(estimator=base_model, method="sigmoid", cv="prefit")
    calibrated_model.fit(X_val, y_val)

    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "model.pkl")
    calibrated_model.booster_ = base_model.booster_
    joblib.dump(calibrated_model, model_path)

    test_path = os.path.join(models_dir, "test_split.csv")
    df_test.to_csv(test_path, index=False)

    metadata = {
        "model_name": "RazorShield_LightGBM_Risk_v1",
        "version": "1.0.0",
        "algorithm": "Calibrated LightGBM (Gradient Boosted Decision Trees)",
        "training_timestamp": datetime.utcnow().isoformat() + "Z",
        "train_samples": len(df_train),
        "val_samples": len(df_val),
        "test_samples": len(df_test),
        "feature_count": len(FEATURE_COLUMNS),
        "feature_names": FEATURE_COLUMNS,
        "best_iteration": int(base_model.best_iteration_) if hasattr(base_model, "best_iteration_") else 350,
        "params": {k: str(v) for k, v in params.items()}
    }

    metadata_path = os.path.join(models_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return calibrated_model, X_test, y_test

if __name__ == "__main__":
    train_model()
