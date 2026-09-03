# AI-Driven Advanced Blockchain Security

A research-grade, implementation-ready project that fuses **AI anomaly detection** with a **zero-trust blockchain node policy** and **secure smart-contract patterns**.

## Features
- IsolationForest-based anomaly scoring on transaction features
- Zero-trust node auth using JWT (PyJWT)
- Simple blockchain simulator with pluggable security hook
- Streamlit dashboard for monitoring
- Example vulnerable vs. secure Solidity contracts

## Structure
```
backend/
  api/app.py             # FastAPI service
  blockchain_sim.py      # Toy blockchain + mining
  models/*.pkl           # Trained IsolationForest + scaler
  utils/detector.py      # Scoring utilities
  utils/zero_trust.py    # JWT-based zero-trust
  requirements.txt
contracts/
  VulnerableBank.sol
  SecureWallet.sol
  audit_report.md
dashboard/
  streamlit_app.py
data/
  sample_transactions.csv
docs/
  report.pdf
  abstract.txt
  presentation.pdf
```

## Quickstart

### 1) Create venv & install deps
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2) Run API
```bash
uvicorn backend.api.app:app --reload
```

### 3) Run Dashboard
```bash
streamlit run dashboard/streamlit_app.py
```

### 4) Try Mining (Zero-Trust demo)
```python
from backend.utils.zero_trust import issue_node_token
print(issue_node_token("node-1"))
```
Use the token as `Authorization: Bearer <token>` for `/tx` and `/mine` endpoints.

## Notes
- The dataset is synthetic but representative.
- Extend features (graph features, timing windows) for better accuracy.
- Integrate with real chains via web3.py if desired.


## Docker (API + Dashboard)

```bash
# From project root
docker compose up --build
# API → http://localhost:8000/health
# Dashboard → http://localhost:8501
```

## Postman

1. Import `docs/postman/Advanced-Blockchain-Security.postman_collection.json`.

2. Import environment `docs/postman/ABSF-Local.postman_environment.json` and select it.

3. Use the **Issue Token (Pre-request)** request once to populate `{{authToken}}`.

4. Call **/tx**, then **/mine**, then **/chain**.

