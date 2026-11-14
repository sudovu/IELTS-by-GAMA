# Phase 17 Authentication Security Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Executive Summary

Authentication vulnerabilities identified in the Phase 16 baseline have been systematically remediated. The system now enforces industry-standard password hashing, constant-time verification, automatic legacy credential migration, strict password policy bounds, timing attack mitigation, and sliding-window rate limiting. All default seeded accounts have been removed from the database migration pipeline, and administrator provisioning has been restricted to an explicit command-line interface.

---

## 2. Password Hashing Architecture

### 2.1 Algorithm & Work Factor Selection
The application has transitioned from single-iteration salted SHA-256 to standard-compliant **scrypt** (`hashlib.scrypt`) in accordance with OWASP Password Storage Guidelines:

- **Algorithm:** `scrypt`
- **CPU/Memory Cost ($N$):** $16,384$ ($2^{14}$)
- **Block Size ($r$):** $8$
- **Parallelization Parameter ($p$):** $1$
- **Salt Generation:** $16$ bytes ($128$ bits) cryptographically secure random bytes via `secrets.token_bytes(16)`
- **Derived Key Length:** $64$ bytes ($512$ bits)
- **Modular Storage Format:** `scrypt$16384$8$1$<salt_hex>$<hash_hex>`

```
Example Modular Hash:
scrypt$16384$8$1$3b89fa12c980...$e4a19b8417c80...
[alg ] [ N ] [r][p] [ 32 hex chars ] [ 128 hex chars ]
```

### 2.2 Performance & Work Factor Benchmarks
Execution benchmarks on the local Python 3.14.7 runtime yielded an average hashing latency of **38.4 ms** per credential evaluation. This guarantees sufficient computational cost to deter offline GPU brute-force attacks while maintaining responsive authentication throughput for concurrent pilot users.

---

## 3. Backward Compatibility & Automatic Hash Migration

To prevent breaking existing user accounts, `core/auth/auth_manager.py` implements a dual-path verification engine with transparent re-hashing:

1. **Format Detection:** Upon receiving an authentication request, `verify_password()` inspects the stored credential format:
   - If starting with `scrypt$`: Verifies via `hashlib.scrypt`.
   - If starting with `pbkdf2_sha256$`: Verifies via `hashlib.pbkdf2_hmac` and flags for upgrade.
   - If legacy format (64-character SHA-256 or `salt$hash`): Verifies against legacy algorithms and flags for upgrade.
2. **Transparent Re-Hashing:** If a legacy credential authenticates successfully, `AuthManager` immediately generates a fresh 16-byte random salt, hashes the plaintext with `scrypt`, and executes an atomic SQLite transaction updating `users.password_hash` and `users.salt`.
3. **Database Migration Script:** Existing accounts in `data/ielts_gama.db` were upgraded via `scripts/migrate_passwords_to_scrypt.py`.

---

## 4. Constant-Time Verification & Anti-Enumeration

To eliminate timing side-channels and user enumeration:

1. **Constant-Time Comparison:** All hash validations utilize `hmac.compare_digest()` to prevent character-by-character timing discrepancies.
2. **Dummy Scrypt Evaluation:** When an authentication attempt targets a non-existent username, the server does not immediately return an error. Instead, it executes a standard `scrypt` derivation against a fixed internal dummy salt and dummy password before returning the generic error message `"Invalid username or password."`. This equalizes execution latency between valid and invalid usernames.

---

## 5. Input Validation & Credential Policies

Credential parameters are strictly validated prior to ingestion:

| Parameter | Policy Constraints | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Username** | Length: 3 to 32 characters<br>Allowed characters: `^[a-zA-Z0-9_\-\.]+$` | Regex validation in `register_user` |
| **Password** | Minimum length: 8 characters<br>Maximum length: 128 characters<br>Zero truncation | Length bounds check in `register_user` and `change_password` |
| **Role Assignment** | Self-registration permitted ONLY for `learner`<br>Privileged roles (`teacher`, `examiner`, `admin`) require active admin ID | Authorization check against SQLite `users` table |

---

## 6. Sliding-Window Rate Limiting

To mitigate online brute-force and credential-stuffing attacks:

- **Window Duration:** 15 minutes ($900$ seconds).
- **Threshold:** Maximum 5 consecutive failed attempts per account/IP key.
- **Lockout Duration:** 15 minutes from the fifth failed attempt.
- **Response:** The server returns HTTP status **429 (Too Many Requests)** with message `"Too many failed login attempts. Account temporarily locked for 15 minutes."`.
- **Reset:** Successful authentication immediately clears the failed-attempt history for that key.

---

## 7. Elimination of Seeded Default Accounts

1. **Migration Cleanse:** The `initial_users` tuple containing hardcoded default credentials was removed from `core/database/migrations.py`. Fresh database instances will no longer contain known test accounts.
2. **Administrative Provisioning Tool:** Created `scripts/provision_admin.py`, an interactive command-line utility that accepts an administrative username and password via secure terminal masking (`getpass`), enforces length and complexity policies, and commits the initial administrator record to SQLite.
