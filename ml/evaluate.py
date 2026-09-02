import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc,
    confusion_matrix
)
from ml.features import engineer_features

def evaluate_model(
    model_path: str = "ml/models/model.pkl",
    test_split_path: str = "ml/models/test_split.csv",
    output_path: str = "ml/models/evaluation.json"
):
    model = joblib.load(model_path)
    df_test = pd.read_csv(test_split_path)
    y_test = df_test["label"].values
    X_test = engineer_features(df_test)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred_default = (y_prob >= 0.50).astype(int)

    precision_default = float(precision_score(y_test, y_pred_default, zero_division=0))
    recall_default = float(recall_score(y_test, y_pred_default, zero_division=0))
    f1_default = float(f1_score(y_test, y_pred_default, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))

    precisions_curve, recalls_curve, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = float(auc(recalls_curve, precisions_curve))

    cm = confusion_matrix(y_test, y_pred_default)
    tn, fp, fn, tp = cm.ravel()
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

    cost_params = {
        "average_loss_per_risky_order": 2400.0,
        "verification_cost": 25.0,
        "manual_review_cost": 65.0,
        "false_positive_cost": 220.0,
        "false_negative_cost": 2400.0
    }

    total_positives = int(tp + fn)
    baseline_loss_without_ai = total_positives * cost_params["false_negative_cost"]

    fp_cost_default = fp * cost_params["false_positive_cost"]
    fn_cost_default = fn * cost_params["false_negative_cost"]
    intervention_cost_default = (tp + fp) * cost_params["verification_cost"]
    total_cost_with_ai_default = fp_cost_default + fn_cost_default + intervention_cost_default
    net_savings_default = max(baseline_loss_without_ai - total_cost_with_ai_default, 0.0)

    threshold_analysis = []
    thresholds = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]

    for th in thresholds:
        th_pred = (y_prob >= th).astype(int)
        th_cm = confusion_matrix(y_test, th_pred)
        th_tn, th_fp, th_fn, th_tp = th_cm.ravel()

        th_prec = float(precision_score(y_test, th_pred, zero_division=0))
        th_rec = float(recall_score(y_test, th_pred, zero_division=0))
        th_f1 = float(f1_score(y_test, th_pred, zero_division=0))
        th_fpr = float(th_fp / (th_fp + th_tn)) if (th_fp + th_tn) > 0 else 0.0

        th_fp_cost = th_fp * cost_params["false_positive_cost"]
        th_fn_cost = th_fn * cost_params["false_negative_cost"]
        th_intervention_cost = (th_tp + th_fp) * cost_params["verification_cost"]
        th_total_cost = th_fp_cost + th_fn_cost + th_intervention_cost
        th_avoided_loss = th_tp * cost_params["average_loss_per_risky_order"]
        th_net_benefit = th_avoided_loss - (th_fp_cost + th_intervention_cost)

        threshold_analysis.append({
            "threshold": th,
            "precision": round(th_prec, 4),
            "recall": round(th_rec, 4),
            "f1": round(th_f1, 4),
            "false_positive_rate": round(th_fpr, 4),
            "true_positives": int(th_tp),
            "false_positives": int(th_fp),
            "true_negatives": int(th_tn),
            "false_negatives": int(th_fn),
            "expected_business_cost": round(th_total_cost, 2),
            "expected_avoided_loss": round(th_avoided_loss, 2),
            "expected_net_benefit": round(th_net_benefit, 2)
        })

    hist, bin_edges = np.histogram(y_prob, bins=10, range=(0.0, 1.0))
    prob_distribution = [
        {"bin": f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}", "count": int(hist[i])}
        for i in range(len(hist))
    ]

    evaluation_data = {
        "model_version": "1.0.0",
        "evaluation_split": "Held-out Test Set (Untouched during training & tuning)",
        "test_set_size": len(y_test),
        "actual_positives_in_test": total_positives,
        "actual_negatives_in_test": int(tn + fp),
        "metrics_summary": {
            "precision": round(precision_default, 4),
            "recall": round(recall_default, 4),
            "f1_score": round(f1_default, 4),
            "roc_auc": round(roc_auc, 4),
            "pr_auc": round(pr_auc, 4),
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
            "accuracy": round(float((tp + tn) / len(y_test)), 4)
        },
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        },
        "cost_analysis": {
            "disclaimer": "Estimated using configurable business assumptions.",
            "cost_parameters": cost_params,
            "baseline_loss_without_ai": round(baseline_loss_without_ai, 2),
            "estimated_loss_with_ai": round(total_cost_with_ai_default, 2),
            "estimated_prevented_loss": round(net_savings_default, 2),
            "false_positive_cost_incurred": round(fp_cost_default, 2),
            "intervention_cost_incurred": round(intervention_cost_default, 2),
            "roi_ratio": round(net_savings_default / max(intervention_cost_default, 1.0), 2)
        },
        "threshold_analysis": threshold_analysis,
        "prediction_distribution": prob_distribution
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(evaluation_data, f, indent=2)

    return evaluation_data

if __name__ == "__main__":
    evaluate_model()
