import json
import os
import random
import hashlib
import time
import getpass

# ==========================================
# Persistence Layer
# ==========================================
WALLETS_FILE = "wallets.json"


# ==========================================
# Password helpers
# ==========================================

def hash_password(password: str) -> str:
    """Return a simple SHA-256 hash of the password (demo only)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ==========================================
# Wallet model
# ==========================================

class Wallet:
    def __init__(self, owner_name, address=None, balance=0.0, password_hash=None):
        self.owner_name = owner_name
        self.address = address or f"0x{random.getrandbits(160):040x}"
        self.balance = float(balance)
        self.password_hash = password_hash  # sha256 hash string or None

    def to_dict(self):
        return {
            "owner_name": self.owner_name,
            "address": self.address,
            "balance": self.balance,
            "password_hash": self.password_hash,
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Backward compatible: older JSON will not have "password_hash"
        return cls(
            owner_name=data.get("owner_name"),
            address=data.get("address"),
            balance=data.get("balance", 0.0),
            password_hash=data.get("password_hash"),
        )

    # ---------- password methods ----------

    def set_password(self, password: str):
        self.password_hash = hash_password(password)

    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return self.password_hash == hash_password(password)


# ==========================================
# Wallet manager
# ==========================================

class WalletManager:
    def __init__(self, filename=WALLETS_FILE):
        self.filename = filename
        self.wallets = {}  # name -> Wallet
        self.load_wallets()

    def load_wallets(self):
        if not os.path.exists(self.filename):
            self.wallets = {}
            return
        with open(self.filename, "r") as f:
            data = json.load(f)
        self.wallets = {name: Wallet.from_dict(info) for name, info in data.items()}
        print(f"[System] Loaded {len(self.wallets)} wallets from disk.")

    def save_wallets(self):
        data = {name: w.to_dict() for name, w in self.wallets.items()}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
        print("[System] Wallets saved.")

    def get_wallet_by_name(self, name: str):
        return self.wallets.get(name)

    def get_wallet_by_address(self, address: str):
        for w in self.wallets.values():
            if w.address == address:
                return w
        return None

    def create_wallet(self, owner_name: str, password: str):
        if owner_name in self.wallets:
            raise ValueError("Wallet already exists with this username.")

        # As you requested, initial balance is always 0.0 LYC for new wallet
        wallet = Wallet(owner_name=owner_name, balance=0.0)
        wallet.set_password(password)
        self.wallets[owner_name] = wallet
        self.save_wallets()

        print(f"[System] New wallet created for {owner_name}.")
        print(f"Wallet Address: {wallet.address}")
        print(f"Initial Balance: {wallet.balance:.1f} LYC")
        return wallet

    # ---------- authentication helpers ----------

    def _force_set_password_if_missing(self, wallet: Wallet):
        """If this is an old wallet with no password, force the user to create one."""
        if wallet.password_hash:
            return
        print(f"[Security] Wallet '{wallet.owner_name}' has no password yet.")
        print("[Security] Please set a password now.")
        while True:
            pwd1 = getpass.getpass("New password: ")
            pwd2 = getpass.getpass("Confirm password: ")
            if pwd1 != pwd2:
                print("Passwords do not match. Try again.")
            elif not pwd1:
                print("Password cannot be empty.")
            else:
                wallet.set_password(pwd1)
                self.save_wallets()
                print("Password set successfully.")
                break

    def authenticate(self, owner_name: str, purpose: str = "login"):
        wallet = self.get_wallet_by_name(owner_name)
        if not wallet:
            print("❌ Wallet not found.")
            return None

        # Upgrade old wallet without password
        self._force_set_password_if_missing(wallet)

        for _ in range(3):
            pwd = getpass.getpass(f"Enter password to {purpose}: ")
            if wallet.verify_password(pwd):
                print("✅ Password verified.")
                return wallet
            else:
                print("Wrong password, try again.")
        print("Too many incorrect attempts. Access denied.")
        return None


# ==========================================
# Voucher verifier (coupon codes)
# ==========================================

class VoucherVerifier:
    def __init__(self):
        # Coupon codes / vouchers (same as your project)
        self.vouchers = {
            "Startbucks_90_off": ("Starbucks", 50),
            "lenscart_try_me": ("Lenskart", 30),
            "Amazon_Festive": ("Amazon", 100),
            "Flipkart_BigBillion": ("Flipkart", 90),
            "Zomato_Gold": ("Zomato", 40),
            "Swiggy_Super": ("Swiggy", 40),
            "Myntra_Fashion": ("Myntra", 60),
            "Ajio_Trends": ("Ajio", 55),
            "Uber_Ride": ("Uber", 25),
            "Ola_Share": ("Ola", 20),
        }
        self.redeemed = set()

    def verify_and_redeem(self, code: str):
        print(f"[Exchange] Initiating swap for voucher code: {code}...")
        if code not in self.vouchers:
            print("[VoucherVerifier] Invalid voucher code.")
            return None
        if code in self.redeemed:
            print("[VoucherVerifier] Voucher already redeemed.")
            return None

        self.redeemed.add(code)
        brand, value = self.vouchers[code]
        print(f"[VoucherVerifier] Voucher {code} verified and redeemed.")
        print(f"[LoyaltyToken] Brand: {brand}, Value: {value} LYC")
        return brand, value


# ==========================================
# Utility
# ==========================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# User session menu (after login)
# ==========================================

def user_session(manager: WalletManager, verifier: VoucherVerifier, wallet: Wallet):
    """Menu for actions once a user is logged in."""
    while True:
        print("\n----------------------------------------")
        print(f"User: {wallet.owner_name} | Balance: {wallet.balance:.1f} LYC")
        print("----------------------------------------")
        print("1. Swap Voucher")
        print("2. Check Wallet Details")
        print("3. Transfer Tokens")
        print("4. Logout")
        choice = input("Choose an option: ").strip()

        # 1. Swap Voucher
        if choice == "1":
            code = input("\nEnter voucher code: ").strip()
            result = verifier.verify_and_redeem(code)
            if result:
                brand, value = result
                wallet.balance += value
                print("[Exchange] Swap Complete!")
                manager.save_wallets()

        # 2. Check Wallet Details
        elif choice == "2":
            print("\n[Wallet Details]")
            print(f"Owner   : {wallet.owner_name}")
            print(f"Address : {wallet.address}")
            print(f"Balance : {wallet.balance:.1f} LYC")

        # 3. Transfer Tokens
        elif choice == "3":
            print()
            recipient_addr = input("Enter recipient wallet address: ").strip()
            recipient = manager.get_wallet_by_address(recipient_addr)
            if not recipient:
                print("Recipient wallet not found.")
                continue

            try:
                amt_str = input("Enter amount to transfer: ").strip()
                amount = float(amt_str)
            except ValueError:
                print("Invalid amount.")
                continue

            if amount <= 0:
                print("Amount must be positive.")
                continue
            if wallet.balance < amount:
                print("Insufficient balance.")
                continue

            # Ask for password again before transfer
            auth_wallet = manager.authenticate(wallet.owner_name,
                                               purpose="confirm this transfer")
            if not auth_wallet:
                continue

            wallet.balance -= amount
            recipient.balance += amount
            print(
                f"[LoyaltyToken] Transfer: {amount:.1f} LYC "
                f"from {wallet.address[:6]}... to {recipient.address[:6]}..."
            )
            manager.save_wallets()

        # 4. Logout back to main menu
        elif choice == "4":
            print("Logging out...")
            time.sleep(0.7)
            break

        else:
            print("Invalid option.")

        time.sleep(0.7)


# ==========================================
# Main entry menu (Login / Create / Exit)
# ==========================================

def main():
    clear_screen()
    print("=========================================")
    print("  Blockchain-powered Loyalty Points Exchange")
    print("=========================================")

    manager = WalletManager()
    verifier = VoucherVerifier()

    while True:
        print("\n========== Main Menu ==========")
        print("1. Login to existing wallet")
        print("2. Create new wallet")
        print("3. Exit")
        main_choice = input("Choose an option: ").strip()

        # ---- Login ----
        if main_choice == "1":
            username = input("Enter your username: ").strip()
            wallet = manager.authenticate(username, purpose="login")
            if wallet:
                user_session(manager, verifier, wallet)

        # ---- Create wallet ----
        elif main_choice == "2":
            username = input("Choose a username (wallet owner): ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            if manager.get_wallet_by_name(username):
                print("Wallet already exists with that username.")
                continue

            while True:
                pwd1 = getpass.getpass("Set wallet password: ")
                pwd2 = getpass.getpass("Confirm wallet password: ")
                if pwd1 != pwd2:
                    print("Passwords do not match. Try again.")
                elif not pwd1:
                    print("Password cannot be empty.")
                else:
                    break

            wallet = manager.create_wallet(username, pwd1)
            # After creating, directly go into session
            user_session(manager, verifier, wallet)

        # ---- Exit ----
        elif main_choice == "3":
            print("Saving and exiting...")
            manager.save_wallets()
            break

        else:
            print("Invalid option.")

        time.sleep(0.7)


if __name__ == "__main__":
    main()
