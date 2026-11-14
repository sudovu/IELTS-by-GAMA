# Phase 17 Consent & Right-to-Erasure Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Executive Summary

In compliance with modern privacy regulations (including GDPR Articles 7 and 17, and CCPA/CPRA), IELTS by GAMA enforces explicit informed consent before admitting any candidate material into evaluation benchmarks, alongside an automated right-to-erasure (Right to be Forgotten) mechanism that purges candidate content, nullifies assessment bands, physically deletes audio assets, and logs non-identifying audit records.

---

## 2. Informed Consent Enforcement Gate

Candidate essays and speech recordings cannot be automatically ingested into benchmark or research datasets without an active, recorded consent event:

### 2.1 Enrollment Pre-Condition
In `core/benchmark/benchmark_manager.py: enroll_benchmark_submission()`:
```python
if not has_consent:
    return {
        "success": False,
        "error": "Consent violation: Explicit candidate informed consent is required to enroll content into the benchmark dataset."
    }
```
Attempting to enroll any candidate submission with `has_consent=False` immediately halts processing, preventing unauthorized data aggregation.

### 2.2 Consent Metadata Tracking
When consent is verified, the record is stored in `benchmark_records` with full audit metadata:
- `consent_status`: `'consented'`
- `consent_timestamp`: ISO 8601 UTC timestamp of consent grant
- `consent_purpose`: Declared purpose (e.g., `'internal_assessment_calibration'`)
- `dataset_version`: Application version at enrollment (`1.6.0`)

---

## 3. Right-to-Erasure Workflow (`withdraw_consent`)

When a candidate requests the withdrawal of their data or exercises their right to erasure, the application executes `core/benchmark/benchmark_manager.py: withdraw_consent(benchmark_id)`:

```
[Candidate Erasure Request]
         │
         ▼
[Lookup Benchmark Record in SQLite]
         │
         ├──► [1. Overwrite Text Content] ──► "[CONTENT_WITHDRAWN_AND_PURGED]"
         │
         ├──► [2. Nullify Assessment Bands] ──► consensus_human_band = NULL
         │                                      consensus_criteria_json = NULL
         │
         ├──► [3. Physical Disk Erasure] ──► os.remove(recording_ref.wav)
         │
         ├──► [4. Update Status] ──────────► consent_status = 'withdrawn'
         │                                   recording_ref = NULL
         │
         └──► [5. Audit Log Entry] ────────► system_settings: erasure_audit_<id>
```

### 3.1 Content Purging
- The essay text or transcript in `anonymized_content` is overwritten with the immutable marker:
  `[CONTENT_WITHDRAWN_AND_PURGED]`
- All associated scores (`consensus_human_band`, `consensus_criteria_json`) are reset to `NULL`.

### 3.2 Physical Media Deletion
- If the submission contains an associated audio recording (`recording_ref`), the system verifies the file path on the filesystem.
- If the file exists, it is permanently deleted via `os.remove()`.
- The database reference is set to `NULL`.

### 3.3 Non-Identifying Audit Logging
To demonstrate compliance with regulatory erasure requests without retaining candidate data, a non-identifying record is inserted into `system_settings`:
- **Key:** `erasure_audit_<benchmark_id>`
- **Value:** `{"action": "consent_withdrawn", "timestamp": "<ISO_UTC>", "reason": "<Reason>"}`
- This log confirms the execution of the erasure without retaining the underlying candidate work.

---

## 4. Verification Evidence

The entire consent gate and erasure cycle was validated under automated test `tests/test_phase17_security_hardening.py`:
- `test_14_benchmark_consent_gate`: Passed.
- `test_16_benchmark_withdrawal_and_erasure`: Passed. Physical `.wav` audio artifact verified absent from disk post-withdrawal, text verified purged, and scores verified `NULL`.
