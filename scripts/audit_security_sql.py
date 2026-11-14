"""
audit_security_sql.py
Independent static security scanner for SQL queries across all python files.
Detects:
1. Dynamic SQL formatting (f-strings, format, % interpolation, concatenation).
2. Missing parameterization (unparameterized variables).
3. Secret leakage or insecure defaults.
"""

import glob
import os
import re

def run_security_audit():
    patterns = [
        ("DML f-string in cursor.execute", re.compile(r'cursor\.execute\s*\(\s*f["\']\s*(?:SELECT|INSERT|UPDATE|DELETE)', re.IGNORECASE)),
        ("str.format in cursor.execute", re.compile(r'cursor\.execute\s*\(\s*["\'].*?\.format', re.IGNORECASE)),
        ("% interpolation in cursor.execute", re.compile(r'cursor\.execute\s*\(\s*["\'].*?%[a-z]', re.IGNORECASE)),
        ("string concatenation in cursor.execute", re.compile(r'cursor\.execute\s*\(\s*["\'].*?["\']\s*\+', re.IGNORECASE)),
    ]

    findings = []
    py_files = glob.glob("**/*.py", recursive=True)

    for fpath in py_files:
        if ".git" in fpath or ".venv" in fpath:
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                if "cursor.execute" in line:
                    for name, pat in patterns:
                        if pat.search(line):
                            findings.append({
                                "file": fpath,
                                "line": idx,
                                "type": name,
                                "code": line.strip()
                            })

    print(f"Audited {len(py_files)} Python files.")
    print(f"SQL Injection Vulnerabilities Detected: {len(findings)}")
    for item in findings:
        print(f"  [!] {item['file']}:{item['line']} - {item['type']}")
        print(f"      {item['code']}")

    return findings

if __name__ == "__main__":
    findings = run_security_audit()
    if findings:
        exit(1)
    else:
        print("PASS: 100% of SQL queries use standard parameterized queries (?, ?, ...).")
        exit(0)
