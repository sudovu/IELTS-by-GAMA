"""
Security Audit Script for Git History and Tracked Files
Phase 19: Production Release & GitHub Synchronization
"""

import os
import re
import subprocess
import sys

def run_git(cmd):
    p = subprocess.run(f"git {cmd}", capture_output=True, text=True, shell=True)
    return p.stdout.strip()

def main():
    print("=== Scanning Tracked Files ===")
    tracked_files = run_git("ls-files").splitlines()
    print(f"Total tracked files: {len(tracked_files)}")

    secret_patterns = [
        ("AWS/GCP/Generic API Key", re.compile(r'(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|private[_-]?key)\s*[:=]\s*["\']([a-zA-Z0-9_\-\.]{16,})["\']')),
        ("OpenAI Key", re.compile(r'sk-[a-zA-Z0-9]{20,}')),
        ("GitHub Personal Access Token", re.compile(r'gh[pousr]_[A-Za-z0-9_]{36,}')),
        ("Hardcoded Password", re.compile(r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'](?!test|admin|learner|example|sample|pass|correct|scrypt|\$)[a-zA-Z0-9!@#$%^&*()_+]{8,}["\']')),
        ("Local Windows User Path", re.compile(r'[Cc]:[\\/]Users[\\/][a-zA-Z0-9_\-\.]+')),
        ("Private Key Block", re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----'))
    ]

    suspicious_findings = []

    for fpath in tracked_files:
        if not os.path.exists(fpath):
            continue
        # Skip binary files
        if fpath.endswith((".png", ".jpg", ".jpeg", ".ico", ".ipa", ".keystore", ".jar", ".zip")):
            continue

        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for label, pattern in secret_patterns:
                    matches = pattern.findall(content)
                    if matches:
                        # Filter out known safe unit test strings or documentation references
                        filtered_matches = []
                        for m in matches:
                            m_str = str(m)
                            # Ignore mock passwords in tests
                            if "test_" in fpath or "tests/" in fpath:
                                if any(x in m_str.lower() for x in ["pass", "correcthorse", "adminsec", "studentpass"]):
                                    continue
                            # Ignore documentation references
                            if fpath.endswith(".md") and "C:\\Users\\" in m_str:
                                # Report as local path finding
                                filtered_matches.append((label, m_str[:50]))
                                continue
                            filtered_matches.append((label, m_str[:50]))
                        if filtered_matches:
                            suspicious_findings.append((fpath, filtered_matches))
        except Exception as e:
            print(f"Error reading {fpath}: {e}")

    print(f"\nSuspicious findings in tracked files: {len(suspicious_findings)}")
    for fpath, finds in suspicious_findings:
        print(f"File: {fpath}")
        for label, val in finds:
            print(f"  - [{label}]: {val}")

    print("\n=== Checking for Database Files in Working Directory ===")
    db_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
        for f in files:
            if f.endswith((".db", ".sqlite", ".db-wal", ".db-shm")):
                db_files.append(os.path.join(root, f))
    print(f"Found {len(db_files)} database files in workspace:")
    for db in db_files:
        print(f"  {db}")

if __name__ == "__main__":
    main()
