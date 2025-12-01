# Loyalty Token Exchange System

A simple **blockchain-inspired loyalty token project** using **Solidity smart contracts** and a **Python wallet system**.  
Users can create wallets, redeem vouchers, earn tokens, and transfer them securely.

---
# Team Introduction
#### Team Member 1 : Vraj Desai (IAR/15593)
#### Team Member 2 : Manthan Parmar (IAR/15652)
#### Team Member 3 : Rishi Rao (IAR/15653)

---

## 🔧 Features

- 👛 Create & Login to Wallet
- 🔐 Password protected (SHA-256 hashing)
- 🎫 Redeem voucher codes → earn LYC tokens
- 💸 Transfer tokens to other wallet addresses
- 💾 Wallet data stored in `wallets.json`
- 🪙 ERC20-style Loyalty Token (LYC)
---

## 🧩 Smart Contracts
### **LoyaltyToken.sol**
- ERC20-like token
- Stores balances
- Handles transfers & minting
### **VoucherVerifier.sol**
- Stores predefined voucher codes
- Returns brand + token value
### **Exchange.sol**
- Verifies vouchers via VoucherVerifier
- Mints LYC tokens through LoyaltyToken
- Prevents double redemption

---
## ▶️ How It Works
1. User logs in or creates a wallet
2. Enters a voucher code
3. Contract verifies it → tokens added
4. Users can send tokens to others

---

## Run the Python App

```
git clone https://github.com/desaivraj8740/loyalty_points_exchange.git

cd loyalty_points_exchange

python exchange.py
```

---

##  Project Structure

```
LoyaltyToken.sol
Exchange.sol
VoucherVerifier.sol
exchange.py
wallets.json
README.md
```

---

## 📌 Summary

A lightweight project demonstrating how **blockchain tokens**, **voucher redemption**, and a **wallet system** work together using Python + Solidity.
