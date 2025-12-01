// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./LoyaltyToken.sol";
import "./VoucherVerifier.sol";

contract Exchange {
    LoyaltyToken public token;
    VoucherVerifier public verifier;
    address public owner;

    event SwapExecuted(address indexed user, string voucherCode, uint256 amount);

    constructor(address _tokenAddress, address _verifierAddress) {
        token = LoyaltyToken(_tokenAddress);
        verifier = VoucherVerifier(_verifierAddress);
        owner = msg.sender;
    }

    function swapVoucher(string memory code) external {
        // 1. Verify and redeem the voucher
        // This call will fail if the voucher is invalid or used
        uint256 value = verifier.redeemVoucher(code);

        // 2. Transfer tokens to the user
        // The Exchange contract must hold enough tokens or have minting rights
        // For this demo, we assume the Exchange holds a balance
        require(token.balanceOf(address(this)) >= value, "Exchange has insufficient liquidity");
        
        bool success = token.transfer(msg.sender, value);
        require(success, "Token transfer failed");

        emit SwapExecuted(msg.sender, code, value);
    }

    // Function to fund the exchange with tokens
    function fundExchange(uint256 amount) external {
        require(token.transferFrom(msg.sender, address(this), amount), "Funding failed");
    }
}
