import pickle
import numpy as np

FEATURES = ["amount","freq_per_hr","gas_price","contract_call","hour"]

with open("backend/models/anomaly_iforest.pkl","rb") as f:
    MODEL = pickle.load(f)
with open("backend/models/scaler.pkl","rb") as f:
    SCALER = pickle.load(f)

def anomaly_score(tx: dict) -> float:
    x = np.array([[tx.get(k,0.0) for k in FEATURES]], dtype=float)
    xs = SCALER.transform(x)
    # decision_function: higher is more normal; we invert to make higher = more anomalous
    score = -MODEL.decision_function(xs)[0]
    return float(score)

def is_suspicious(tx: dict, thresh: float = 0.2) -> bool:
    return anomaly_score(tx) > thresh
