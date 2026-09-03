import pandas as pd
import time
from backend.utils.detector import anomaly_score

import matplotlib.pyplot as plt

import os
import sys
sys.path.append(os.getcwd())

import streamlit as st

st.set_page_config(page_title="Advanced Blockchain Security Dashboard", layout="wide")
st.title("🔒 Advanced Blockchain Security — Anomaly Monitor")

st.markdown("""
This dashboard scores transactions using an IsolationForest model.
Higher score = more anomalous (potentially malicious).
""")

uploaded = st.file_uploader("Upload transactions CSV (or use bundled sample)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/sample_transactions.csv")

features = ["amount","freq_per_hr","gas_price","contract_call","hour"]
df["anomaly_score"] = df.apply(lambda r: anomaly_score(r.to_dict()), axis=1)

st.subheader("Summary")
st.write(df[features + ["anomaly_score"]].describe())

st.subheader("Top Suspicious Transactions")
topk = df.sort_values("anomaly_score", ascending=False).head(20)
st.dataframe(topk)

st.subheader("Distribution of Anomaly Scores")
plt.figure()
df["anomaly_score"].hist(bins=40)
st.pyplot(plt.gcf())
