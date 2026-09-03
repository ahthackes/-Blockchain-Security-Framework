// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * VulnerableBank demonstrates a re-entrancy vulnerability for education.
 * DO NOT deploy in production.
 */
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient");
        // Vulnerable: sending Ether before state update enables reentrancy
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
        balances[msg.sender] -= amount;
    }
}
