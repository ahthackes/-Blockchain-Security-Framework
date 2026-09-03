from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional, List
from backend.blockchain_sim import Blockchain, Transaction
from backend.utils.detector import is_suspicious, anomaly_score
from backend.utils.zero_trust import verify_node_token

app = FastAPI(title="AI-Driven Advanced Blockchain Security")

BC = Blockchain(difficulty=3)

class TxIn(BaseModel):
    from_addr: str
    to_addr: str
    amount: float
    gas_price: float
    contract_call: int
    freq_per_hr: int
    hour: int
    nonce: int
    timestamp: float

def security_hook(tx_obj: Transaction, score_threshold: float = 0.2) -> bool:
    tx_dict = tx_obj.__dict__
    score = anomaly_score(tx_dict)
    return score <= score_threshold

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/tx")
def submit_tx(tx: TxIn, authorization: Optional[str] = Header(default=None)):
    # Zero-trust: require valid node token
    if not authorization or not authorization.startswith("Bearer "):
        return {"ok": False, "error":"missing token"}
    token = authorization.split(" ",1)[1]
    node_id = verify_node_token(token)
    if not node_id:
        return {"ok": False, "error":"invalid token"}

    tx_obj = Transaction(**tx.model_dump())
    # Admit tx to pool regardless; filtering happens at mining time.
    BC.add_transaction(tx_obj)
    return {"ok": True, "queued": True}

@app.post("/mine")
def mine(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        return {"ok": False, "error":"missing token"}
    token = authorization.split(" ",1)[1]
    node_id = verify_node_token(token)
    if not node_id:
        return {"ok": False, "error":"invalid token"}

    block = BC.mine_block(security_hook=security_hook)
    return {"ok": True, "block_index": block.index, "hash": block.hash, "tx_count": len(block.transactions)}

@app.get("/chain")
def chain():
    return {"length": len(BC.chain), "chain": [b.__dict__ for b in BC.chain]}
