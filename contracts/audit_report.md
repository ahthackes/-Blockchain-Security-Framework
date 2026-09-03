# Smart Contract Audit (Mini)

## Scope
- `VulnerableBank.sol` — intentionally vulnerable example
- `SecureWallet.sol` — fixed variant with reentrancy guard

## Findings
1. **Reentrancy (Critical)** in `VulnerableBank.withdraw()`:
   - Ether is sent before state update.
   - Fix: checks-effects-interactions pattern + `nonReentrant` guard.

2. **Lack of Pausable / Rate Limits (Low)**:
   - Consider modules to pause withdrawals on anomalies.

## Recommendations
- Use OpenZeppelin ReentrancyGuard when possible.
- Add owner/DAO-controlled circuit breaker.
