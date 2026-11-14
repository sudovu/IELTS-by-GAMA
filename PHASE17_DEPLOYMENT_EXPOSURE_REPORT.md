# Phase 17 Deployment Exposure & Environmental Boundary Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Release Engineering Team  

---

## 1. Executive Summary

A critical objective of Phase 17 was to investigate potential deployment exposure, inspect external synchronization paths, and verify whether internal application secrets, learner data, or administrative tools had been leaked or deployed publicly.

The investigation examined the external local directory `c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts` and the associated GitHub Pages repository. The audit confirmed that **no database files, no Python server code, no environment variables, and no server credentials were ever present or exposed**. Furthermore, changes to the local folder were uncommitted and had **never been pushed to any remote Git repository**. To prevent unintentional synchronization in the future, the build tooling was permanently hardened with an explicit deployment gate.

---

## 2. External Directory Investigation (`gautambhuwan.com.np\ielts`)

### 2.1 Filesystem Inventory
An exhaustive directory traversal of `c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts` was conducted:

```
c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts\
├── index.html       (Static PWA shell)
├── app.js           (Client-side UI application script)
├── styles.css       (Presentation stylesheets)
├── sw.js            (Client-side Service Worker for offline asset caching)
├── manifest.json    (PWA web app manifest)
├── icons/           (Application icon assets)
└── images/          (Diagnostic and lesson diagrams)
```

### 2.2 Sensitivity & Exposure Analysis
1. **Database Files (`*.db`, `*.sqlite`, `*.sqlite3`):** **ABSENT**. Zero database files exist in the external folder.
2. **Server-Side Code (`*.py`):** **ABSENT**. Zero Python files, backend modules, or server scripts exist in the directory.
3. **Environment & Secrets (`.env`, config keys):** **ABSENT**. Zero API tokens, administrative passwords, or encryption keys are present.
4. **Git Repository Status:**
   - Navigated to `c:\Users\Sudo\Projects\gautambhuwan.com.np`.
   - Branch: `main`.
   - Tracking status: `Your branch is up to date with 'origin/main'`.
   - Git log confirmed that no Phase 16 commits had been pushed to GitHub Pages. The files in the `ielts/` subfolder existed solely in the uncommitted local working copy.

---

## 3. Build Tool Hardening (`build_ios_distribution.py`)

### 3.1 Uncontrolled Synchronization Defect
Inspection of `scripts/build_ios_distribution.py` revealed that earlier versions unconditionally copied compiled web assets into `c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts` whenever the build script was executed locally.

### 3.2 Implemented Remediation
In `scripts/build_ios_distribution.py`:
- Added an explicit `deploy_external: bool = False` configuration flag.
- Bound external directory synchronization to an explicit command-line argument: `--deploy-external`.
- By default, executing `python scripts/build_ios_distribution.py` outputs build artifacts exclusively to the internal workspace directory:
  `c:\Users\Sudo\Projects\IELTS by GAMA\build\ios_distribution\`
- Any attempt to copy assets outside the workspace without `--deploy-external` is automatically bypassed with an informational notice.

---

## 4. Deployment Boundary Definition

| Boundary Zone | Allowed Deployments | Current State |
| :--- | :--- | :--- |
| **Local Development** | Embedded Python HTTP server (`ui/server.py`) on `127.0.0.1:8080` / `8899` | **Active & Verified** |
| **Internal Supervised Pilot** | Controlled local network or private VPN instances with authorized examiner logins | **Ready for Preparation** |
| **Public Web Deployment** | Public GitHub Pages, Netlify, or unrestricted internet hosting | **STRICTLY PROHIBITED** |

**Mandatory Release Policy:**  
Public internet deployment remains prohibited during Phase 17. The application is an assessment-assisted practice tool whose scoring calibration must first be validated through supervised pilot cohorts. Public deployment before human calibration would violate assessment validity standards.
