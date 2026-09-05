# RazorShield: Cost-Sensitive AI Risk Manager for RTO & Return Abuse

> **Built for the Razorpay AI Buildathon — AI Risk Manager Track**  
> *"Detect. Explain. Decide. Prevent."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.1-646CFF.svg)](https://vitejs.dev/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.7-brightgreen.svg)](https://lightgbm.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Problem Statement
E-commerce merchants in India lose over **₹20,000+ Crores annually** due to Return-to-Origin (RTO) failures and abusive return patterns, disproportionately concentrated in Cash on Delivery (COD) orders. When an order fails doorstep delivery or is repeatedly returned:
- The merchant bears **forward courier shipping fees** (₹100–₹160).
- The merchant bears **reverse logistics return fees** (₹140–₹200).
- Inventory is locked in transit for 10–21 days, suffering **depreciation, repackaging costs, and stock-outs**.
- Blanket blocking of buyers causes catastrophic **false-positive friction**, destroying customer lifetime value.

Merchants do not merely need a naive fraud classifier. They need an **AI-assisted risk decision system** that answers:
> *"How risky is this transaction, WHY is it risky, and WHAT is the economically optimal intervention?"*

---

## 2. Solution: The RazorShield Framework
RazorShield combines **calibrated machine learning**, **explainable AI (Tree SHAP)**, and a **cost-sensitive decision engine** to quantify risk and recommend mathematically justified business interventions:

```
TRANSACTION
    │
    ▼
Feature Engineering Pipeline (Ratios, Velocities, Logistics Indices)
    │
    ▼
Calibrated LightGBM GBDT (Probability: 0.00 – 1.00, Score: 0 – 100)
    │
    ▼
Explainability Layer (Tree SHAP: Positive Drivers vs Protective Buffers)
    │
    ▼
Cost-Sensitive Decision Engine (Trade-off Avoided Loss vs Intervention Cost)
    │
    ▼
AI Risk Manager Agent (Grounded, Audit-Ready Risk Narrative)
    │
    ▼
Merchant Operations Dashboard & Human-in-the-Loop Override Queue
```

---

## 3. Key Product Pillars

### 1. Honest, Measured ML Performance (Held-Out Test Split)
Trained on 50,000 synthetic transactions with realistic domain correlations and class imbalance (~9.8% positive rate). Evaluated on an **untouched held-out test split of 7,500 records**:
- **ROC-AUC**: `0.8925`
- **PR-AUC**: `0.6019`
- **Precision (@0.50 Cutoff)**: `74.32%`
- **Recall (@0.50 Cutoff)**: `36.96%` (and `66.44%` at balanced cutoff `0.20`)
- **False Positive Rate**: `1.39%` (conservative cutoff preserving customer trust)

### 2. Cost-Sensitive Decision Optimization
Interventions are recommended only when economically justified:
$$\text{Expected Avoided Loss} = P(\text{Risk}) \times (\text{Logistics Loss} + 0.15 \times \text{Order Value})$$
- **LOW Risk (0–30)** $\rightarrow$ **`APPROVE`** (Zero friction checkout).
- **MEDIUM Risk (31–70)** $\rightarrow$ **`ADDITIONAL_VERIFICATION`** (Automated WhatsApp OTP / address confirmation at ₹25 cost).
- **HIGH Risk (71–100)** $\rightarrow$ **`MANUAL_REVIEW`** (Flagged to risk operations queue at ₹65 cost).

### 3. Tree SHAP Explainability
Every prediction decomposes exact mathematical contributions:
- **Top Risk Contributors (+)**: COD payment method, pincode failure rate, device sharing across multiple accounts, rapid order bursts.
- **Top Protective Factors (-)**: Account tenure age, prepaid UPI/Card, consistent delivery history.

### 4. Bounded AI Risk Manager Agent
Operates as an explanatory and orchestrating intelligence layer.
- Strictly bounded to structured transaction data.
- **Zero hallucinations**: never fabricates delivery attempts or transaction facts.
- Generates executive audit summaries and routes cases into human review workflows.

### 5. Human-in-the-Loop & Immutable Audit Trail
- Merchant operators can review flagged orders in the **Review Queue**.
- 1-click **Human Override** captures operator identity and justification.
- Every automated decision and manual override is permanently logged to an immutable SQLite/PostgreSQL audit trail.

---

## 4. 5 Pre-Loaded Presentation Demo Scenarios

| Scenario | Customer Profile | Risk Score | Decision | Business Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | 420-day account, 24 past orders, UPI prepaid | **6 / 100 (LOW)** | `APPROVE` | Trusted loyal buyer, zero friction checkout. |
| **Scenario 2** | 65-day account, COD footwear order, moderate pincode risk | **44 / 100 (MED)** | `ADDITIONAL_VERIFICATION` | Automated WhatsApp confirmation to avoid doorstep refusal. |
| **Scenario 3** | 4-day account, 4 devices shared, 2 past RTOs, COD electronics | **86 / 100 (HIGH)** | `MANUAL_REVIEW` | High-risk multi-account abuse cluster; avoided loss ₹1,324 exceeds review cost. |
| **Scenario 4** | 2-day account, ₹18,500 jewelry order, velocity burst | **88 / 100 (HIGH)** | `MANUAL_REVIEW` | Excessive ticket size on fresh COD account; severe potential loss. |
| **Scenario 5** | 18-day account, ₹12,000 electronics, Credit Card prepaid | **22 / 100 (LOW)** | `APPROVE` | **False-Positive Candidate**: High ticket but prepaid; approved without unnecessary friction. |

---

## 5. Technology Stack
- **Machine Learning**: LightGBM 4.7, Scikit-Learn 1.3, NumPy, Pandas, Joblib.
- **Backend API**: Python 3.10, FastAPI, Pydantic v2, SQLAlchemy, Uvicorn.
- **Frontend Dashboard**: React 18, Vite 5, Tailwind CSS, Lucide React.
- **Database**: SQLite (default zero-config local), compatible with PostgreSQL.
- **Testing**: PyTest with automated test coverage across feature engineering, inference, decision logic, and human overrides.
- **Containerization**: Docker, Docker Compose multi-stage build.

---

## 6. Quick Start & Local Execution

### Option A: Direct Local Run

#### 1. Clone and Set Up Python Backend
```bash
# Clone the repository
git clone https://github.com/sakshirothe/to-do-list.git
cd "Razorshield AI"

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Regenerate synthetic dataset and train model
python data/generate_dataset.py --samples 50000
python -m ml.train
python -m ml.evaluate

# Start FastAPI server (runs database setup and demo seeding on startup)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Launch React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

### Option B: Unified Single-Port Run (Production Build)
The built frontend is pre-compiled into `frontend/dist`. Running the backend alone serves the entire unified application on port 8000:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000`** in your browser.

---

### Option C: Docker Container
```bash
docker compose up --build
```
Access the application at `http://localhost:8000`.

---

## 7. Running the Automated Test Suite
Execute the full test suite verifying features, inference bounds, cost engines, and API overrides:
```bash
pytest -v


................................................
*Built with ❤️ for the Razorpay AI Buildathon.*
