# MASTER BUILD PROMPT — RAZORSHIELD AI

You are a senior fintech AI engineer, ML engineer, backend engineer, frontend engineer, and product designer.

Build a complete, production-style hackathon project called:

# RazorShield

### Cost-Sensitive AI Risk Manager for RTO & Return Abuse

The project is being built for the **Razorpay AI Buildathon — Build. Show. Get hired.**, specifically the **AI Risk Manager** track.

The goal is to build a working defensive AI system that detects one class of merchant loss, verifies risk, and recommends an appropriate intervention.

IMPORTANT:

* This is a defense-only system.
* Do NOT implement anything that helps users commit fraud, bypass fraud detection, evade risk systems, exploit payment systems, or perform offensive activities.
* Do NOT claim to use real Razorpay customer or transaction data.
* If real data is unavailable, create a realistic SYNTHETIC dataset and clearly label it as synthetic.
* Do not fabricate ML performance metrics. All metrics must be calculated from the actual held-out test set.

---

# 1. CORE PROBLEM

Merchants lose money because suspicious orders can result in:

* Return-to-Origin (RTO)
* abusive returns
* refunds
* operational costs
* verification costs
* inventory/logistics losses

Build an AI system that predicts the risk of an order becoming a problematic return/RTO and then determines the most economically appropriate action.

The system must answer:

> "How risky is this transaction/order, WHY is it risky, and WHAT should the merchant do?"

The system should not merely classify transactions.

It must produce:

1. Risk probability
2. Risk score
3. Risk level
4. Explanation of major risk factors
5. Recommended action
6. Estimated potential loss
7. Estimated intervention cost
8. Expected benefit of intervention
9. Audit trail

---

# 2. PRODUCT NAME

Use:

RazorShield

Tagline:

"Detect. Explain. Decide. Prevent."

Do NOT represent the product as an official Razorpay product.

Use wording such as:

"Built for the Razorpay AI Buildathon."

---

# 3. PRIMARY USER

The primary user is an e-commerce merchant / risk operations team.

They should be able to:

* monitor risk
* inspect suspicious orders
* understand why an order was flagged
* see model confidence
* approve low-risk transactions
* request verification for medium/high-risk transactions
* manually review suspicious cases
* understand estimated financial impact

---

# 4. CORE WORKFLOW

Implement this workflow:

TRANSACTION
↓
Feature Engineering
↓
ML Risk Model
↓
Risk Probability
↓
Risk Score
↓
Explainability Layer
↓
Cost-Sensitive Decision Engine
↓
Recommended Action
↓
Merchant Dashboard
↓
Audit Log

---

# 5. RISK LEVELS

Use configurable thresholds.

Default:

0–30:
LOW

31–70:
MEDIUM

71–100:
HIGH

Do NOT hard-code these throughout the application.

Store thresholds in configuration.

The system should allow thresholds to be changed later.

---

# 6. RECOMMENDED ACTIONS

LOW:

→ APPROVE

MEDIUM:

→ ADDITIONAL VERIFICATION

HIGH:

→ MANUAL REVIEW

However, do not make decisions solely from risk percentage.

The decision engine must also consider:

* estimated potential loss
* intervention cost
* false-positive cost
* merchant policy

Example:

Potential loss = ₹2,500
Verification cost = ₹30

Expected benefit of verification should be calculated.

If intervention is economically justified:

→ VERIFY

Otherwise:

→ APPROVE

Make this logic transparent.

---

# 7. DATASET

Create a synthetic dataset containing at least 50,000 realistic transaction/order records.

Do not generate random numbers without realistic relationships.

The synthetic data should contain meaningful correlations.

Suggested columns:

transaction_id
customer_id
merchant_id
order_value
payment_method
product_category
quantity
account_age_days
previous_orders
previous_returns
previous_refunds
return_rate
rto_rate
days_since_last_order
orders_last_7_days
orders_last_30_days
address_change_count
device_account_count
shipping_distance_km
pincode_risk_score
delivery_attempts
historical_customer_risk
is_weekend
hour_of_day
customer_order_frequency
payment_failure_count
previous_chargebacks
previous_rto_count
label

Target:

label

0 = normal transaction/order

1 = risky return/RTO behavior

The generated dataset must contain realistic class imbalance.

For example, risky cases can represent approximately 5–15% of the dataset.

Make the exact distribution configurable.

---

# 8. DATA GENERATION

Create a reproducible dataset generator.

Use a fixed random seed.

Create:

data/generate_dataset.py

The generator should:

* create realistic customer behavior
* create realistic merchant/order behavior
* create correlations between risk factors
* create class imbalance
* prevent impossible values
* document how labels are generated

Save:

data/transactions.csv

Also create:

data/README.md

explaining:

* synthetic nature of dataset
* columns
* label definition
* generation assumptions
* limitations

---

# 9. MACHINE LEARNING

Implement a complete ML pipeline.

Use Python.

Preferred model:

XGBoost or LightGBM.

If unavailable, use Random Forest or HistGradientBoosting as fallback.

Pipeline:

Raw data
↓
Validation
↓
Feature engineering
↓
Train/Validation/Test split
↓
Model training
↓
Hyperparameter tuning
↓
Probability calibration if appropriate
↓
Final evaluation

IMPORTANT:

Use a TRUE held-out test set.

Recommended:

70% train
15% validation
15% test

The final test set must not be used for model tuning.

---

# 10. FEATURE ENGINEERING

Create meaningful features such as:

return_rate
rto_rate
refund_rate
orders_per_week
account_activity_score
device_reuse_score
address_change_frequency
high_value_order_flag
customer_history_score
pincode_risk
payment_reliability_score

Do not leak the target into the features.

Document every feature.

---

# 11. MODEL EVALUATION

The system MUST calculate actual:

* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC
* Confusion Matrix
* False Positive Rate
* False Negative Rate

Do not only report accuracy.

Because the buildathon specifically requires honest precision and recall on a held-out test set.

Create:

ml/evaluate.py

Save evaluation results in a structured JSON file.

Example:

models/evaluation.json

The UI should load the actual evaluation results rather than hard-coded numbers.

---

# 12. THRESHOLD ANALYSIS

Implement threshold analysis.

Evaluate model performance at different thresholds:

0.10
0.20
0.30
0.40
0.50
0.60
0.70
0.80
0.90

Show:

* precision
* recall
* F1
* false-positive rate
* expected business cost

Allow the merchant to understand the trade-off between catching more risky transactions and generating more false positives.

---

# 13. FALSE-POSITIVE COST

This is a CORE requirement.

Implement a cost model.

Configurable parameters:

average_loss_per_risky_order
manual_review_cost
verification_cost
false_positive_cost
false_negative_cost

Calculate:

False Positive Cost
+
False Negative Cost
+
Intervention Cost

Then calculate:

Total Expected Cost

Compare:

WITHOUT AI

versus

WITH AI

Do not fabricate business savings.

Clearly label all financial calculations as:

"Estimated using configurable assumptions."

---

# 14. COST-SENSITIVE DECISION ENGINE

Create a dedicated module:

backend/services/decision_engine.py

It should consider:

risk_probability
estimated_loss
verification_cost
review_cost
false_positive_cost
merchant_policy

Example logic:

If:

risk_probability is high
AND
expected avoided loss > intervention cost

then:

RECOMMEND VERIFICATION / REVIEW

Otherwise:

APPROVE

Return structured output:

{
"risk_score": 91,
"risk_level": "HIGH",
"recommended_action": "MANUAL_REVIEW",
"estimated_loss": 2400,
"intervention_cost": 30,
"expected_benefit": 2370,
"reason": "Expected avoided loss significantly exceeds review cost."
}

---

# 15. EXPLAINABILITY

Use SHAP or an equivalent explainability method.

For every prediction, show:

Top positive risk factors
Top negative/protective factors

Example:

Risk Score: 91/100

Top contributors:

Previous return rate       +24
Account age                +18
Device reuse               +15
Pincode risk               +12
Order value                 +9

Do NOT claim that SHAP values are causal explanations.

Label them:

"Model contributing factors."

---

# 16. AI AGENT LAYER

Create an AI Risk Manager Agent on top of the ML system.

The agent should NOT replace the ML model.

The architecture should be:

ML Model
↓
Structured Risk Result
↓
AI Risk Manager Agent
↓
Explanation + Recommendation + Workflow

The agent receives structured information such as:

risk_score
risk_level
risk_factors
estimated_loss
intervention_cost
merchant_policy

The agent should generate a concise risk assessment.

Example:

"This order is classified as high risk primarily because the account is new, the customer's historical return rate is high, and the device is associated with multiple accounts. Estimated potential loss is ₹2,400 while manual verification costs approximately ₹30. Manual verification is therefore recommended."

The agent must NEVER invent transaction information.

It must only use provided structured data.

---

# 17. AGENT ACTIONS

Implement bounded actions.

Allowed:

* analyze transaction
* explain risk
* recommend verification
* recommend manual review
* approve low-risk order
* create review task
* record decision
* generate risk summary

Every action must be logged.

The agent should not autonomously perform irreversible financial actions.

Use human-in-the-loop for high-impact decisions.

---

# 18. TRANSACTION ANALYZER

Create an interface where the merchant can enter/select a transaction.

Display:

Transaction ID
Amount
Customer
Payment method
Account age
Previous returns
Previous refunds
Device information
Shipping information

Then:

[ANALYZE RISK]

Show:

Risk Score
Risk Level
Recommended Action
Estimated Loss
Intervention Cost
Expected Benefit

Then show:

"Why was this flagged?"

---

# 19. WHAT-IF SIMULATOR

Add a feature:

"What-If Risk Simulator"

Allow the user to change:

* order value
* account age
* previous returns
* address changes
* device reuse
* payment method
* pincode risk

Then recalculate risk.

Example:

Original:

Risk = 91%

Change previous returns:

4 → 0

New:

Risk = 62%

The UI should clearly indicate:

"This is a model simulation, not a historical transaction."

---

# 20. DASHBOARD

Build a polished merchant dashboard.

Include:

Total transactions
High-risk transactions
Medium-risk transactions
Low-risk transactions
Estimated loss
Estimated avoided loss
Review queue
False-positive cost

Charts:

Risk distribution
Risk trend over time
High-risk categories
Payment-method risk
Pincode risk
Model performance
Confusion matrix
Precision/Recall trade-off
Expected cost by threshold

---

# 21. REVIEW QUEUE

Create:

Risk Review Queue

Columns:

Transaction
Amount
Risk Score
Risk Level
Top Risk Factor
Recommended Action
Status

Statuses:

PENDING
APPROVED
VERIFICATION_REQUIRED
MANUAL_REVIEW
RESOLVED

Clicking an item should open the complete risk analysis.

---

# 22. AUDIT LOG

Every AI decision must create an audit record.

Store:

transaction_id
timestamp
risk_score
risk_level
model_version
recommended_action
decision_status
risk_factors
decision_reason
human_override
final_action

Create an audit log screen.

Example:

Transaction RX92831

Model Version:
v1.0.0

Risk:
91%

Recommendation:
MANUAL REVIEW

Human Decision:
APPROVED

Reason:
Customer verified successfully.

---

# 23. HUMAN OVERRIDE

The merchant/operator must be able to override AI recommendations.

Example:

AI:

MANUAL REVIEW

Human:

APPROVE

Require an optional reason.

Store this in the audit log.

This demonstrates human-in-the-loop safety.

---

# 24. MODEL MONITORING

Create a Model Health section.

Show:

Model version
Training date
Test set size
Precision
Recall
F1
ROC-AUC
PR-AUC
False Positive Rate

Also show:

Prediction distribution

Design the architecture so that model versioning is possible.

---

# 25. API

Use FastAPI.

Create APIs:

POST /api/analyze

POST /api/simulate

GET /api/transactions

GET /api/transactions/{id}

GET /api/dashboard

GET /api/model/metrics

GET /api/reviews

POST /api/reviews/{id}/decision

GET /api/audit

GET /api/health

Use Pydantic models.

Validate all inputs.

Return clean JSON.

---

# 26. DATABASE

Use PostgreSQL if possible.

SQLite may be used for local development.

Tables:

transactions
risk_predictions
reviews
audit_logs
model_versions
merchant_settings

Create database migrations/schema.

Do not store secrets in source code.

---

# 27. FRONTEND

Build a modern professional fintech dashboard.

Preferred:

React + Vite + Tailwind CSS.

Design goals:

* clean
* professional
* minimal
* data-dense
* easy to understand
* responsive

Do NOT copy Razorpay's exact branding.

Use an original visual identity.

Use:

RazorShield

as the product brand.

---

# 28. MAIN UI PAGES

Create:

1. Dashboard
2. Transaction Analyzer
3. Risk Review Queue
4. Transaction Details
5. What-If Simulator
6. Model Performance
7. Cost Analysis
8. Audit Log
9. Settings

---

# 29. LANDING / DEMO SCREEN

Create a strong initial screen showing:

RazorShield

"AI Risk Manager for Merchant Loss Prevention"

Short description:

"Predict risk. Explain decisions. Optimize intervention."

CTA:

Analyze Transaction

Secondary:

View Risk Dashboard

---

# 30. COST ANALYSIS PAGE

Show:

Historical estimated loss
AI-assisted estimated loss
False-positive cost
Intervention cost
Estimated prevented loss

Include a configurable assumptions panel.

Clearly label:

"Illustrative estimate based on synthetic data and configurable business assumptions."

---

# 31. SECURITY

Implement:

* environment variables
* no hard-coded API keys
* input validation
* safe error handling
* API rate limiting if practical
* CORS configuration
* no sensitive real customer information
* no secrets committed to GitHub

Create:

.env.example

---

# 32. TESTING

Create tests for:

* feature engineering
* model inference
* risk scoring
* decision engine
* cost calculations
* API endpoints
* invalid input
* human override
* audit logging

The project should have a working test suite.

---

# 33. DOCKER

Create:

Dockerfile

docker-compose.yml

Services:

frontend
backend
database

The project should be runnable locally with a simple command.

---

# 34. README

Create an excellent GitHub README.

Include:

# RazorShield

## Problem

## Solution

## Why this matters

## Architecture

## AI/ML approach

## Dataset

## Feature engineering

## Model

## Evaluation methodology

## Precision & Recall

## False-positive cost

## Cost-sensitive decision engine

## AI Agent

## Explainability

## Human-in-the-loop

## Screenshots

## Demo

## Tech stack

## Installation

## Running locally

## API documentation

## Limitations

## Future work

IMPORTANT:

Clearly state that the dataset is synthetic.

Clearly distinguish:

* measured model metrics
* estimated business metrics

---

# 35. ARCHITECTURE DIAGRAM

Create a professional architecture diagram showing:

Frontend
↓
FastAPI
↓
Risk Orchestrator
↓
Feature Engine
↓
ML Model
↓
Explainability
↓
Cost-Sensitive Decision Engine
↓
AI Agent
↓
Database
↓
Audit Log

Also show:

Human Reviewer

connected to:

Review Queue

---

# 36. MODEL CARD

Create:

docs/model_card.md

Include:

Model purpose
Training data
Synthetic-data limitations
Features
Target definition
Evaluation methodology
Metrics
Known limitations
Potential biases
Intended use
Non-intended use
Safety considerations

---

# 37. DEMO MODE

Add a demo mode with several pre-generated scenarios:

Scenario 1:
Low-risk customer

Scenario 2:
Medium-risk customer

Scenario 3:
High-risk customer

Scenario 4:
High-value suspicious transaction

Scenario 5:
False-positive example

This allows the 5-minute presentation to work reliably.

---

# 38. IMPORTANT DEMO FLOW

The demo should take approximately 3 minutes.

Demo:

1. Open dashboard.
2. Show overall risk metrics.
3. Select suspicious transaction.
4. Click Analyze.
5. Show risk score.
6. Show contributing factors.
7. Show estimated financial impact.
8. Show recommended action.
9. Open review queue.
10. Override AI recommendation.
11. Show audit log.
12. Open model performance.
13. Show precision, recall and F1.
14. Open cost analysis.
15. Show false-positive cost.

---

# 39. DESIGN PRINCIPLE

The project should communicate:

"This is not just a fraud classifier."

It is:

"An AI-assisted risk decision system."

The key product loop is:

DETECT
↓
EXPLAIN
↓
QUANTIFY
↓
DECIDE
↓
VERIFY
↓
LEARN

---

# 40. DO NOT DO THESE THINGS

Do NOT:

* claim the model is production-ready
* claim real Razorpay data
* fabricate performance
* hard-code fake metrics
* use only accuracy
* build an offensive fraud tool
* provide fraud evasion capabilities
* automatically block customers without safeguards
* allow the LLM to make unrestricted financial decisions
* expose secrets
* create meaningless random synthetic data
* add an LLM just for the sake of saying "AI Agent"

---

# 41. ENGINEERING QUALITY

Prioritize:

* modular architecture
* clean code
* typed APIs
* reusable components
* error handling
* logging
* testing
* reproducibility
* documentation
* explainability
* safety
* measurable performance

Do not build everything in one file.

---

# 42. FINAL DELIVERABLES

At the end, the repository must contain:

frontend/
backend/
ml/
data/
tests/
docs/

plus:

README.md
Dockerfile
docker-compose.yml
.env.example
requirements.txt

The system must be runnable locally.

---

# 43. DEVELOPMENT PROCESS

Do NOT try to generate the entire application blindly in one step.

Build in phases:

PHASE 1:
Dataset + ML pipeline

PHASE 2:
Evaluation + cost model

PHASE 3:
FastAPI backend

PHASE 4:
Database

PHASE 5:
Risk Agent

PHASE 6:
React dashboard

PHASE 7:
Review queue + audit

PHASE 8:
Testing

PHASE 9:
Docker

PHASE 10:
README + architecture + demo mode

After completing each phase:

* run tests
* verify functionality
* fix errors
* then continue

---

# 44. SUCCESS CRITERIA

The project is successful only if:

✓ A transaction can be analyzed end-to-end

✓ The ML model generates a real risk probability

✓ Precision and recall are calculated on an untouched held-out test set

✓ False-positive cost is calculated

✓ Risk factors can be explained

✓ The system recommends an economically justified action

✓ A human can override the recommendation

✓ Every decision is audited

✓ The AI agent cannot invent transaction facts

✓ The project runs locally

✓ The dashboard works

✓ The README explains the methodology honestly

✓ The system demonstrates genuine AI/ML engineering rather than a static mockup

---

# 45. FINAL PRODUCT POSITIONING

The final project should communicate this idea:

"Merchants don't only need to know which transactions are risky. They need to know which risky transactions are worth intervening on."

RazorShield therefore combines:

ML Risk Prediction
+
Explainable AI
+
Cost-Sensitive Decision Making
+
Agentic Risk Analysis
+
Human-in-the-Loop Verification
+
Auditability

Build the project with this principle throughout.

Start with PHASE 1: dataset generation, feature engineering, ML training, and evaluation.

Do not move to the frontend until the ML pipeline produces real, reproducible results.
