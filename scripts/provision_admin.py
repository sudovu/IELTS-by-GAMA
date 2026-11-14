#!/usr/bin/env python3
"""
Secure Initial Administrator Provisioning Tool for IELTS by GAMA.
Used exclusively by system administrators during initial server setup.
Does NOT store plaintext passwords or hardcode credentials in source.
Enforces scrypt password hashing and input validation.
"""

import sys
import os
import getpass
import argparse

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.database.db_manager import DatabaseManager
from core.auth.auth_manager import AuthManager


def provision_admin(username: str, password: str, full_name: str, email: str) -> bool:
    db = DatabaseManager()
    auth = AuthManager(db)

    clean_user = username.strip().lower()
    if not auth.USERNAME_REGEX.match(clean_user):
        print(f"[ERROR] Invalid username '{clean_user}'. Must be 3-32 chars (alphanumeric, _, -, .).")
        return False

    if len(password) < auth.MIN_PASSWORD_LENGTH:
        print(f"[ERROR] Password must be at least {auth.MIN_PASSWORD_LENGTH} characters long.")
        return False

    # Check if admin already exists
    existing = db.fetchone("SELECT id, role FROM users WHERE username = ?", (clean_user,))
    if existing:
        print(f"[WARN] User '{clean_user}' already exists with role '{existing[1]}'. Updating password to scrypt...")
        salt = auth.hash_password(password, algorithm="scrypt")
        # Split out salt hex
        parts = salt.split("$")
        salt_hex = parts[4]
        db.execute(
            "UPDATE users SET password_hash = ?, salt = ?, role = 'admin' WHERE id = ?",
            (salt, salt_hex, existing[0])
        )
        auth.revoke_all_user_sessions(existing[0])
        print(f"[SUCCESS] Administrator '{clean_user}' credentials updated and existing sessions invalidated.")
        return True

    res = auth.register_user(
        username=clean_user,
        password=password,
        role="admin",
        full_name=full_name,
        email=email,
        authorizing_admin_user_id=None  # Allowed because no admin existed
    )

    if res.get("success"):
        print(f"[SUCCESS] Initial Administrator '{clean_user}' successfully provisioned with scrypt hashing.")
        print(f"          User ID: {res['user_id']}")
        return True
    else:
        print(f"[ERROR] Provisioning failed: {res.get('error')}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Provision the initial IELTS by GAMA Administrator.")
    parser.add_argument("--username", default="admin", help="Admin username (default: admin)")
    parser.add_argument("--full-name", default="System Administrator", help="Full name")
    parser.add_argument("--email", default="admin@gama.internal", help="Admin email")
    parser.add_argument("--password", default=None, help="Admin password (prompts securely if omitted)")

    args = parser.parse_args()

    password = args.password
    if not password:
        env_pw = os.environ.get("GAMA_INITIAL_ADMIN_PASSWORD")
        if env_pw:
            password = env_pw
        else:
            password = getpass.getpass(f"Enter secure password for Administrator '{args.username}': ")
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                print("[ERROR] Passwords do not match.")
                sys.exit(1)

    success = provision_admin(args.username, password, args.full_name, args.email)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
