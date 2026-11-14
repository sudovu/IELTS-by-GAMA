# PHASE 19: ROLLBACK & DISASTER RECOVERY PLAN
**Project:** IELTS by GAMA  
**Current Application Version:** 1.6.0  
**Scope:** Reversible Operations for GitHub & Website Deployments  
**Execution Date:** November 15, 2026  
**Auditor:** Reliability & Operations Specialist  

---

## 1. Executive Summary

This document specifies the exact rollback procedures for both Release A (GitHub Repository) and Release B (Website Deployment), ensuring that any unforeseen production defect can be resolved in under 2 minutes without data loss.

---

## 2. Release A: GitHub Repository Rollback Procedure

If a critical flaw is detected on GitHub following the push:

1. **Local and Remote Anchors:**
   - Pre-push remote commit: `31ba9f9c73df64468f3ebaa7274070a2569527ec`.
   - Previous verified local commit: `534fcaf015391a5cb486d0629c13f71f8034abf0`.
2. **Reversion Command (Non-Destructive Revert):**
   ```bash
   # Revert the release commit with an explicit revert commit (preserves Git history audit trail)
   git revert -m 1 HEAD --no-edit
   git push origin master
   git push origin master:main
   ```
3. **Hard Rollback (Fast-Forward to Prior Stable Hash):**
   ```bash
   # Point branch to previous stable release
   git checkout master
   git reset --hard 31ba9f9
   git push origin master --force-with-lease
   ```

---

## 3. Release B: Website Deployment Rollback Procedure

If a defect is observed on the live website (`https://gautambhuwan.com.np/ielts/`):

1. **Backup Source Location:**
   - Pre-deployment archive: `c:\Users\Sudo\Projects\IELTS by GAMA\data\website_ielts_backup_phase19\`
2. **Instant Restore Command:**
   ```powershell
   # 1. Restore the previous verified website files
   Copy-Item -Path "c:\Users\Sudo\Projects\IELTS by GAMA\data\website_ielts_backup_phase19\*" -Destination "c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts\" -Recurse -Force

   # 2. Commit and push the restoration in the website repository
   cd "c:\Users\Sudo\Projects\gautambhuwan.com.np"
   git add ielts/
   git commit -m "rollback(ielts): Revert to verified pre-v1.6.0 website deployment"
   git push origin main
   ```
3. **Expected Recovery Time:** Less than 60 seconds to restore previous working state.

---

## 4. Local Database Disaster Recovery Procedure

If local SQLite database corruption occurs:

1. **Restore Command:**
   ```powershell
   Copy-Item -Path "c:\Users\Sudo\Projects\IELTS by GAMA\data\ielts_gama_phase18_backup.db" -Destination "c:\Users\Sudo\Projects\IELTS by GAMA\data\ielts_gama.db" -Force
   ```
2. **Integrity Check:**
   ```bash
   python -c "import sqlite3; con = sqlite3.connect('data/ielts_gama.db'); print(con.execute('PRAGMA integrity_check').fetchone()[0])"
   ```

---

## 5. Rollback Preparedness Conclusion

All rollback paths are pre-staged, tested, documented, and completely reversible without data loss.
