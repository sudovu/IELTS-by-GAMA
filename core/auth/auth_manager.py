"""
Authentication & Role-Based Access Control (RBAC) Module for IELTS by GAMA.
Supports: Learner, Teacher, Examiner, Administrator.
Implements secure salted password hashing, persistent session tokens, and strict role enforcement.
"""

import hashlib
import secrets
import datetime
from typing import Optional, Dict, Any, List, Tuple
from core.database.db_manager import DatabaseManager


class AuthManager:
    """Manages user authentication, session tokens, and RBAC authorization."""

    VALID_ROLES = {"learner", "teacher", "examiner", "admin"}

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """Computes salted SHA-256 hash."""
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def register_user(
        self,
        username: str,
        password: str,
        role: str = "learner",
        full_name: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """Registers a new user with salted credentials."""
        clean_user = username.strip().lower()
        clean_role = role.strip().lower()

        if clean_role not in self.VALID_ROLES:
            return {"success": False, "error": f"Invalid role '{role}'. Allowed: {', '.join(sorted(self.VALID_ROLES))}"}

        if len(password) < 6:
            return {"success": False, "error": "Password must be at least 6 characters long."}

        existing = self.db.fetchone("SELECT id FROM users WHERE username = ?", (clean_user,))
        if existing:
            return {"success": False, "error": f"Username '{clean_user}' is already registered."}

        salt = secrets.token_hex(8)
        phash = self.hash_password(password, salt)
        user_id = f"usr_{secrets.token_hex(8)}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.db.execute(
            """INSERT INTO users (id, username, password_hash, salt, role, full_name, email, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, clean_user, phash, salt, clean_role, full_name or clean_user, email, now)
        )

        return {
            "success": True,
            "user_id": user_id,
            "username": clean_user,
            "role": clean_role,
            "full_name": full_name or clean_user
        }

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticates credentials and returns user record if valid."""
        clean_user = username.strip().lower()
        row = self.db.fetchone("SELECT * FROM users WHERE username = ?", (clean_user,))
        if not row:
            return None

        user = dict(row)
        expected_hash = self.hash_password(password, user["salt"])
        if user["password_hash"] != expected_hash:
            return None

        # Return user without sensitive hashes
        return {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "full_name": user["full_name"],
            "email": user["email"]
        }

    def create_session(self, user_id: str, duration_hours: int = 24) -> str:
        """Generates a secure cryptographic session token."""
        row = self.db.fetchone("SELECT role FROM users WHERE id = ?", (user_id,))
        role = row[0] if row else "learner"

        token = f"gamasec_{secrets.token_hex(24)}"
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = (now + datetime.timedelta(hours=duration_hours)).isoformat()

        self.db.execute(
            """INSERT INTO user_sessions (session_token, user_id, role, created_at, expires_at)
               VALUES (?, ?, ?, ?, ?)""",
            (token, user_id, role, now.isoformat(), expires)
        )
        return token

    def validate_session(self, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """Validates a session token and returns active user info."""
        if not token or not token.strip():
            return None

        row = self.db.fetchone(
            """SELECT s.session_token, s.user_id, s.role, s.expires_at, u.username, u.full_name, u.email
               FROM user_sessions s
               JOIN users u ON s.user_id = u.id
               WHERE s.session_token = ?""",
            (token.strip(),)
        )
        if not row:
            return None

        sess = dict(row)
        expires_at_str = sess.get("expires_at", "")
        if expires_at_str:
            try:
                expires_dt = datetime.datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                if now_dt > expires_dt:
                    # Session expired
                    self.revoke_session(token)
                    return None
            except Exception:
                pass

        return {
            "token": sess["session_token"],
            "user_id": sess["user_id"],
            "username": sess["username"],
            "role": sess["role"],
            "full_name": sess["full_name"],
            "email": sess["email"]
        }

    def revoke_session(self, token: str) -> bool:
        """Revokes a session token."""
        if not token:
            return False
        self.db.execute("DELETE FROM user_sessions WHERE session_token = ?", (token,))
        return True

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves public user metadata."""
        row = self.db.fetchone("SELECT id, username, role, full_name, email, created_at FROM users WHERE id = ?", (user_id,))
        return dict(row) if row else None

    def list_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Lists users matching a specified role."""
        rows = self.db.fetchall("SELECT id, username, role, full_name, email FROM users WHERE role = ?", (role,))
        return [dict(r) for r in rows]

    def authorize_request(
        self,
        token: Optional[str],
        allowed_roles: List[str]
    ) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Enforces RBAC authorization.
        Returns: (is_authorized, user_dict, error_message)
        """
        user = self.validate_session(token)
        if not user:
            return False, None, "Authentication required. Please sign in with a valid session."

        if user["role"] not in allowed_roles:
            return False, user, f"Access Forbidden: Role '{user['role']}' is not authorized. Allowed: {', '.join(allowed_roles)}"

        return True, user, None
