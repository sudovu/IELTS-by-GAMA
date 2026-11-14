"""
Authentication & Role-Based Access Control (RBAC) Module for IELTS by GAMA.
Hardened for Phase 17:
- Standard-compliant scrypt (N=16384, r=8, p=1) and PBKDF2-HMAC-SHA256 (600,000 iterations).
- Constant-time password verification via hmac.compare_digest.
- Transparent password-hash migration from legacy hashes.
- Protection against username enumeration via constant-time dummy verification.
- In-memory sliding-window rate limiting against credential brute-forcing.
- Server-side RBAC enforcement across Learner, Teacher, Examiner, Senior Examiner, Admin.
- Invalidation of all sessions upon password changes.
"""

import hmac
import hashlib
import secrets
import datetime
import re
import threading
from typing import Optional, Dict, Any, List, Tuple
from core.database.db_manager import DatabaseManager


class AuthManager:
    """Manages user authentication, session tokens, and RBAC authorization."""

    VALID_ROLES = {"learner", "teacher", "examiner", "senior_examiner", "admin"}
    USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-\.]{3,32}$")
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128

    # Rate limiting configuration: max 5 failed attempts in 15 minutes (900 seconds)
    MAX_FAILED_ATTEMPTS = 5
    RATE_LIMIT_WINDOW_SECONDS = 900

    _rate_limit_lock = threading.Lock()
    _failed_attempts: Dict[str, List[float]] = {}

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.last_auth_error: Optional[str] = None

    # -------------------------------------------------------------------------
    # Password Hashing & Verification
    # -------------------------------------------------------------------------

    @classmethod
    def hash_password(
        cls,
        password: str,
        salt: Optional[str] = None,
        algorithm: str = "scrypt"
    ) -> str:
        """
        Computes a secure password hash with algorithm, work factors, and salt.
        Supported algorithms:
        - scrypt: N=16384, r=8, p=1 (OWASP recommended standard)
        - pbkdf2_sha256: 600,000 iterations
        """
        if not salt:
            salt = secrets.token_hex(16)  # 16 bytes = 32 hex chars

        salt_bytes = bytes.fromhex(salt)

        if algorithm == "scrypt":
            n, r, p = 16384, 8, 1
            key = hashlib.scrypt(
                password.encode("utf-8"),
                salt=salt_bytes,
                n=n,
                r=r,
                p=p,
                maxmem=0
            )
            return f"scrypt${n}${r}${p}${salt}${key.hex()}"

        elif algorithm == "pbkdf2_sha256":
            iterations = 600000
            key = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt_bytes,
                iterations
            )
            return f"pbkdf2_sha256${iterations}${salt}${key.hex()}"

        else:
            raise ValueError(f"Unsupported algorithm '{algorithm}'")

    @classmethod
    def verify_password(cls, password: str, stored_hash: str, salt: str = "") -> Tuple[bool, bool]:
        """
        Verifies password against stored hash using constant-time comparison.
        Returns: (is_valid, needs_rehash)
        """
        if not stored_hash or not password:
            return False, False

        # Modern modular crypt format: algorithm$...
        if stored_hash.startswith("scrypt$"):
            try:
                parts = stored_hash.split("$")
                n, r, p = int(parts[1]), int(parts[2]), int(parts[3])
                salt_bytes = bytes.fromhex(parts[4])
                expected_key_hex = parts[5]
                calculated_key = hashlib.scrypt(
                    password.encode("utf-8"),
                    salt=salt_bytes,
                    n=n,
                    r=r,
                    p=p,
                    maxmem=0
                )
                is_valid = hmac.compare_digest(calculated_key.hex(), expected_key_hex)
                return is_valid, False
            except Exception:
                return False, False

        elif stored_hash.startswith("pbkdf2_sha256$"):
            try:
                parts = stored_hash.split("$")
                iterations = int(parts[1])
                salt_bytes = bytes.fromhex(parts[2])
                expected_key_hex = parts[3]
                calculated_key = hashlib.pbkdf2_hmac(
                    "sha256",
                    password.encode("utf-8"),
                    salt_bytes,
                    iterations
                )
                is_valid = hmac.compare_digest(calculated_key.hex(), expected_key_hex)
                # If verified with PBKDF2, we can upgrade to scrypt
                return is_valid, True
            except Exception:
                return False, False

        else:
            # Legacy Phase 16 salted SHA-256 (either 64-char hex with salt column or salt$hash)
            effective_salt = salt
            target_hash = stored_hash
            if "$" in stored_hash:
                parts = stored_hash.split("$")
                if len(parts) == 2 and len(parts[1]) == 64:
                    effective_salt, target_hash = parts[0], parts[1]
                elif len(parts) == 2 and len(parts[0]) == 64:
                    target_hash, effective_salt = parts[0], parts[1]

            if len(target_hash) == 64 and effective_salt:
                calc1 = hashlib.sha256((password + effective_salt).encode("utf-8")).hexdigest()
                calc2 = hashlib.sha256((effective_salt + password).encode("utf-8")).hexdigest()
                if hmac.compare_digest(calc1, target_hash) or hmac.compare_digest(calc2, target_hash):
                    return True, True
            return False, False

    # -------------------------------------------------------------------------
    # Rate Limiting
    # -------------------------------------------------------------------------

    @classmethod
    def _clean_rate_limit_window(cls, key: str, now: float):
        cutoff = now - cls.RATE_LIMIT_WINDOW_SECONDS
        attempts = cls._failed_attempts.get(key, [])
        cls._failed_attempts[key] = [t for t in attempts if t > cutoff]

    @classmethod
    def is_rate_limited(cls, key: str) -> Tuple[bool, int]:
        """Checks if key (username or IP) is currently blocked due to failed attempts."""
        if not key:
            return False, 0
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        with cls._rate_limit_lock:
            cls._clean_rate_limit_window(key, now)
            attempts = cls._failed_attempts.get(key, [])
            if len(attempts) >= cls.MAX_FAILED_ATTEMPTS:
                earliest = attempts[0]
                retry_after = int(cls.RATE_LIMIT_WINDOW_SECONDS - (now - earliest))
                return True, max(1, retry_after)
            return False, 0

    @classmethod
    def record_failed_attempt(cls, key: str):
        """Records a failed authentication attempt."""
        if not key:
            return
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        with cls._rate_limit_lock:
            cls._clean_rate_limit_window(key, now)
            if key not in cls._failed_attempts:
                cls._failed_attempts[key] = []
            cls._failed_attempts[key].append(now)

    @classmethod
    def clear_failed_attempts(cls, key: str):
        """Clears failed attempts on successful login."""
        if not key:
            return
        with cls._rate_limit_lock:
            cls._failed_attempts.pop(key, None)

    # -------------------------------------------------------------------------
    # User Registration & Provisioning
    # -------------------------------------------------------------------------

    def register_user(
        self,
        username: str,
        password: str,
        role: str = "learner",
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        authorizing_admin_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Registers a new user with strong scrypt credentials.
        Self-registration is restricted to the 'learner' role.
        Privileged roles require authorization from an active Administrator.
        """
        clean_user = username.strip().lower()
        clean_role = role.strip().lower()

        if not self.USERNAME_REGEX.match(clean_user):
            return {
                "success": False,
                "error": "Username must be 3-32 characters and contain only letters, numbers, underscores, dots, or hyphens."
            }

        if len(password) < self.MIN_PASSWORD_LENGTH:
            return {"success": False, "error": f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long."}

        if len(password) > self.MAX_PASSWORD_LENGTH:
            return {"success": False, "error": f"Password cannot exceed {self.MAX_PASSWORD_LENGTH} characters."}

        if clean_role not in self.VALID_ROLES:
            return {"success": False, "error": f"Invalid role '{role}'. Allowed: {', '.join(sorted(self.VALID_ROLES))}"}

        # Role escalation guard: Privileged roles require active admin verification
        if clean_role in {"teacher", "examiner", "senior_examiner", "admin"}:
            if not authorizing_admin_user_id:
                # Check if this is the very first user (initial admin provisioning)
                user_count_row = self.db.fetchone("SELECT COUNT(*) FROM users")
                user_count = user_count_row[0] if user_count_row else 0
                if user_count > 0 or clean_role != "admin":
                    return {
                        "success": False,
                        "error": "Privileged role creation requires authorization from an active Administrator."
                    }
            else:
                admin_row = self.db.fetchone("SELECT role FROM users WHERE id = ?", (authorizing_admin_user_id,))
                if not admin_row or admin_row[0] != "admin":
                    return {
                        "success": False,
                        "error": "Unauthorized: Only Administrators can create privileged accounts."
                    }

        existing = self.db.fetchone("SELECT id FROM users WHERE username = ?", (clean_user,))
        if existing:
            return {"success": False, "error": "Username is already registered."}

        salt = secrets.token_hex(16)
        phash = self.hash_password(password, salt=salt, algorithm="scrypt")
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

    # -------------------------------------------------------------------------
    # Authentication & Session Management
    # -------------------------------------------------------------------------

    def authenticate(
        self,
        username: str,
        password: str,
        client_ip: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticates credentials with rate limiting and constant-time execution.
        Returns: user_dict if authenticated, or None if failed.
        Sets self.last_auth_error with failure reason.
        """
        self.last_auth_error = None
        clean_user = username.strip().lower()
        rate_key = f"{client_ip}:{clean_user}" if client_ip else clean_user

        is_blocked, retry_after = self.is_rate_limited(rate_key)
        if is_blocked:
            self.last_auth_error = f"Too many failed login attempts. Account temporarily locked for {retry_after} seconds."
            return None

        row = self.db.fetchone("SELECT * FROM users WHERE username = ?", (clean_user,))
        if not row:
            # Dummy scrypt calculation to mitigate timing analysis for username enumeration
            dummy_salt = secrets.token_hex(16)
            self.hash_password("dummy_password_for_timing_safety", salt=dummy_salt)
            self.record_failed_attempt(rate_key)
            self.last_auth_error = "Invalid username or password."
            return None

        user = dict(row)
        stored_hash = user.get("password_hash", "")
        salt = user.get("salt", "")

        is_valid, needs_rehash = self.verify_password(password, stored_hash, salt)
        if not is_valid:
            self.record_failed_attempt(rate_key)
            self.last_auth_error = "Invalid username or password."
            return None

        # Authentication succeeded: clear rate limits
        self.clear_failed_attempts(rate_key)

        # Automatic Hash Migration: Upgrade legacy hashes to modern scrypt
        if needs_rehash:
            try:
                new_salt = secrets.token_hex(16)
                new_hash = self.hash_password(password, salt=new_salt, algorithm="scrypt")
                self.db.execute(
                    "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
                    (new_hash, new_salt, user["id"])
                )
            except Exception:
                pass  # Non-blocking upgrade failure

        return {
            "id": user["id"],
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "full_name": user["full_name"],
            "email": user["email"]
        }

    def create_session(self, user_id: str, duration_hours: int = 24) -> str:
        """Generates a secure cryptographic session token (64 hex chars)."""
        row = self.db.fetchone("SELECT role FROM users WHERE id = ?", (user_id,))
        role = row[0] if row else "learner"

        token = f"gamasec_{secrets.token_hex(32)}"
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = (now + datetime.timedelta(hours=duration_hours)).isoformat()

        self.db.execute(
            """INSERT INTO user_sessions (session_token, user_id, role, created_at, expires_at)
               VALUES (?, ?, ?, ?, ?)""",
            (token, user_id, role, now.isoformat(), expires)
        )
        return token

    def validate_session(self, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """Validates a session token and returns active user metadata."""
        if not token or not token.strip():
            return None

        clean_token = token.strip()
        row = self.db.fetchone(
            """SELECT s.session_token, s.user_id, s.role, s.expires_at, u.username, u.full_name, u.email
               FROM user_sessions s
               JOIN users u ON s.user_id = u.id
               WHERE s.session_token = ?""",
            (clean_token,)
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
                    # Session expired: clean up
                    self.revoke_session(clean_token)
                    return None
            except Exception:
                return None

        return {
            "token": sess["session_token"],
            "user_id": sess["user_id"],
            "username": sess["username"],
            "role": sess["role"],
            "full_name": sess["full_name"],
            "email": sess["email"]
        }

    def revoke_session(self, token: str) -> bool:
        """Revokes a specific session token."""
        if not token:
            return False
        self.db.execute("DELETE FROM user_sessions WHERE session_token = ?", (token.strip(),))
        return True

    def revoke_all_user_sessions(self, user_id: str) -> int:
        """Revokes all active sessions for a user (called upon password change or account disable)."""
        if not user_id:
            return 0
        self.db.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
        return 1

    def change_password(self, user_id: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """Safely changes password and invalidates all existing sessions."""
        if len(new_password) < self.MIN_PASSWORD_LENGTH:
            return {"success": False, "error": f"New password must be at least {self.MIN_PASSWORD_LENGTH} characters."}
        if len(new_password) > self.MAX_PASSWORD_LENGTH:
            return {"success": False, "error": f"New password cannot exceed {self.MAX_PASSWORD_LENGTH} characters."}

        row = self.db.fetchone("SELECT password_hash, salt FROM users WHERE id = ?", (user_id,))
        if not row:
            return {"success": False, "error": "User not found."}

        stored_hash, salt = row[0], row[1]
        is_valid, _ = self.verify_password(old_password, stored_hash, salt)
        if not is_valid:
            return {"success": False, "error": "Current password verification failed."}

        new_salt = secrets.token_hex(16)
        new_hash = self.hash_password(new_password, salt=new_salt, algorithm="scrypt")

        self.db.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (new_hash, new_salt, user_id)
        )

        # Invalidate all existing sessions for this user to enforce fresh login
        self.revoke_all_user_sessions(user_id)

        return {"success": True, "message": "Password updated successfully. Please sign in with your new password."}

    # -------------------------------------------------------------------------
    # Authorization & Permission Verification
    # -------------------------------------------------------------------------

    def authorize_request(
        self,
        token: Optional[str],
        allowed_roles: List[str]
    ) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Enforces server-side RBAC authorization.
        Returns: (is_authorized, user_dict, error_message)
        """
        user = self.validate_session(token)
        if not user:
            return False, None, "Authentication required. Please sign in with a valid session."

        user_role = user.get("role", "")
        # Senior examiner has examiner privileges
        if "examiner" in allowed_roles and user_role == "senior_examiner":
            return True, user, None

        if user_role not in allowed_roles:
            return False, user, f"Access Forbidden: Role '{user_role}' is not authorized. Allowed: {', '.join(allowed_roles)}"

        return True, user, None
