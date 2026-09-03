"""Simple blockchain simulator with blocks, transactions, and a pluggable security hook."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
import hashlib, json, time, random

@dataclass
class Transaction:
    from_addr: str
    to_addr: str
    amount: float
    gas_price: float
    contract_call: int
    freq_per_hr: int
    hour: int
    nonce: int
    timestamp: float

@dataclass
class Block:
    index: int
    prev_hash: str
    timestamp: float
    transactions: List[Transaction]
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        b = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "txs": [t.__dict__ for t in self.transactions],
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(b).hexdigest()

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.chain: List[Block] = []
        self.tx_pool: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, "0"*64, time.time(), [], 0)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def add_transaction(self, tx: Transaction):
        self.tx_pool.append(tx)

    def mine_block(self, security_hook=None) -> Block:
        # optionally filter transactions via security hook (zero-trust + anomaly check)

        txs = self.tx_pool[:]
        if security_hook:
            txs = [t for t in txs if security_hook(t)]

        block = Block(
            index=len(self.chain),
            prev_hash=self.chain[-1].hash,
            timestamp=time.time(),
            transactions=txs
        )
        prefix = "0"*self.difficulty
        while True:
            block.hash = block.compute_hash()
            if block.hash.startswith(prefix):
                break
            block.nonce += 1
        self.chain.append(block)
        self.tx_pool = []
        return block
