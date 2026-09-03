import jwt, time
from typing import Optional

# In production, keep this secret in a vault
SECRET = "super-secret-zero-trust-key"
ISSUER = "absf-node"

def issue_node_token(node_id: str, ttl_sec: int = 3600) -> str:
    payload = {
        "sub": node_id,
        "iss": ISSUER,
        "iat": int(time.time()),
        "exp": int(time.time()) + ttl_sec
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_node_token(token: str) -> Optional[str]:
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"], options={"require": ["exp", "iat", "iss"]})
        if data.get("iss") != ISSUER:
            return None
        return data.get("sub")
    except Exception:
        return None
