import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
import secrets
from core.auth.auth_manager import AuthManager

def migrate_users():
    con = sqlite3.connect("data/ielts_gama.db")
    cur = con.cursor()
    rows = cur.execute("SELECT id, username, password_hash, salt, role FROM users").fetchall()
    print(f"Migrating {len(rows)} user accounts to scrypt...")

    for uid, uname, phash, salt, role in rows:
        if not phash.startswith("scrypt$"):
            # Set a unique strong randomized password for development accounts
            strong_pw = f"Gama_{role.capitalize()}_{secrets.token_hex(8)}!"
            new_salt = secrets.token_hex(16)
            new_hash = AuthManager.hash_password(strong_pw, salt=new_salt, algorithm="scrypt")
            cur.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, uid))
            print(f"  Migrated user '{uname}' ({role}) to scrypt.")
        else:
            print(f"  User '{uname}' is already using scrypt.")

    con.commit()
    con.close()
    print("[SUCCESS] All database user accounts are now secured with scrypt hashing.")

if __name__ == "__main__":
    migrate_users()
