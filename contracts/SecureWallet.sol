// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * SecureWallet fixes re-entrancy by using the checks-effects-interactions pattern
 * and a simple reentrancy guard.
 */
contract SecureWallet {
    mapping(address => uint256) public balances;
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "Reentrancy");
        locked = true;
        _;
        locked = false;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount; // effects first
        (bool ok, ) = msg.sender.call{value: amount}(""); // interaction after effects
        require(ok, "send failed");
    }
}
