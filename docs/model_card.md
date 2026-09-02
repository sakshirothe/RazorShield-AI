# Model Card: RazorShield Calibrated LightGBM Risk Classifier

## 1. Model Details
- **Model Name**: RazorShield LightGBM Risk Classifier v1
- **Model Version**: `1.0.0`
- **Model Type**: Gradient Boosted Decision Trees (GBDT) with Sigmoidal Probability Calibration (`CalibratedClassifierCV`)
- **Developer**: Built for Razorpay AI Buildathon — AI Risk Manager Track
- **License**: MIT
- **Release Date**: September 2026

---

## 2. Intended Use
- **Primary Use Case**: Real-time Return-to-Origin (RTO) and return abuse risk quantification for e-commerce merchants.
- **Decision Output**: Bounded risk probability (0.0 to 1.0) and score (0 to 100), feeding into a cost-sensitive decision engine to determine intervention strategy (`APPROVE`, `ADDITIONAL_VERIFICATION`, or `MANUAL_REVIEW`).
- **Target Users**: E-commerce merchant fraud operations, risk analysts, and customer verification pipelines.

---

## 3. Out-of-Scope / Non-Intended Use
- **Autonomous Irreversible Punitive Action**: The model must **never** be used to autonomously blacklist or permanently seize user funds without human operator review.
- **Credit Scoring / Underwriting**: The model is tuned strictly for delivery and return logistics risk, not creditworthiness or loan issuance.
- **Offensive Evasion Testing**: Strictly intended for merchant defense.

---

## 4. Training & Validation Data
- **Dataset Source**: Synthetic dataset of 50,000 realistic e-commerce transactions generated with fixed random seeds (`seed=42`).
- **Data Splits**:
  - **Training Split**: 70% (34,999 records)
  - **Validation Split**: 15% (7,501 records) — used for early stopping and probability calibration.
  - **Held-Out Test Split**: 15% (7,500 records) — strictly untouched during feature selection, model training, and tuning.
- **Target Variable**: `label` (0 = Clean/Normal, 1 = Abusive RTO / doorstep refusal / return abuse). Class positive rate: 9.81%.

---

## 5. Quantitative Evaluation (Held-Out Test Set)

| Metric | Measured Value | Methodology Notes |
| :--- | :--- | :--- |
| **ROC-AUC** | **0.8925** | Measured on 7,500 untouched test records |
| **PR-AUC** | **0.6019** | Area under the Precision-Recall curve |
| **Precision (@0.50)** | **74.32%** | True positives / total flagged |
| **Recall (@0.50)** | **36.96%** | High threshold conservative baseline |
| **Precision (@0.20)**| **40.15%** | Balanced cost-effective threshold |
| **Recall (@0.20)** | **66.44%** | Captures 2/3 of risky orders |
| **False Positive Rate** | **1.39% (@0.50)** | Highly selective, minimizing friction |
| **Accuracy** | **92.56%** | Baseline overall correct classifications |

---

## 6. Explainability Methodology
- **Technique**: Tree SHAP (Shapley Additive exPlanations) computed natively via LightGBM's tree contribution algorithms (`pred_contrib=True`).
- **Output**:
  - Positive contributions (increasing risk drivers, e.g. COD + high velocity + device sharing).
  - Negative contributions (protective factors, e.g. account age + prepaid UPI + clean history).
- **Disclaimer**: Feature contributions indicate model association within the trained feature space, not causal legal proof.

---

## 7. Known Limitations & Mitigations
1. **Synthetic Data Realism**: While correlations model realistic Indian e-commerce logistics (pincodes, COD vs UPI, device clustering), real-world fraud rings evolve adversarially.
   *Mitigation*: Continuous feedback loop recording human overrides in the immutable audit log for incremental retraining.
2. **False Positives on High-Value Gifts**: Legitimate users occasionally order high-value items to a new address.
   *Mitigation*: Automated lightweight verification (WhatsApp OTP) rather than outright cancellation.
