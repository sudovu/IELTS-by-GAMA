# PHASE 19: WEBSITE DEPLOYMENT AUDIT REPORT
**Project:** IELTS by GAMA  
**Current Application Version:** 1.6.0  
**Website Target:** `https://gautambhuwan.com.np/ielts/`  
**Local Workspace:** `c:\Users\Sudo\Projects\gautambhuwan.com.np`  
**Execution Date:** November 15, 2026  
**Auditor:** Web Systems & Release Engineer  

---

## 1. Executive Summary

This audit inspected the target deployment repository (`c:\Users\Sudo\Projects\gautambhuwan.com.np`), its existing subdirectory structure under `/ielts/`, asset routing, HTTPS configuration, Service Worker scopes, and download distribution paths.

**Audit Finding: The website repository is structurally healthy. All assets are located under the dedicated `/ielts/` subdirectory, ensuring zero collision with main website pages (such as `index.html`, `developments.html`, `blog.html`).**

---

## 2. Directory & Path Verification

The target website is organized with clean separation of concerns:

| Web Route / Path | Local Directory | Contents | Isolation Status |
|---|---|---|:---:|
| `https://gautambhuwan.com.np/` | Root `.` | Main portfolio, blog, and services | Completely isolated from IELTS |
| `https://gautambhuwan.com.np/ielts/` | `./ielts/` | IELTS SPA: `index.html`, `app.js`, `styles.css`, `sw.js`, `manifest.webmanifest`, `images/` | Isolated in `/ielts/` |
| `https://gautambhuwan.com.np/downloads/ielts-by-gama/` | `./downloads/ielts-by-gama/` | Android APKs, iOS IPA, mobileconfig, manifest.plist | Dedicated release directory |

---

## 3. Subdirectory Routing & Relative Path Audit

A critical defect common in SPA deployments to subdirectories is using root-relative paths (`/styles.css`, `/app.js`), which break when hosted under `/ielts/`.

### Verified Path Configurations in `./ielts/`:
1. **HTML Link References:**
   - `<link rel="stylesheet" href="styles.css">` $\to$ Resolves to `https://gautambhuwan.com.np/ielts/styles.css`.
   - `<script src="app.js"></script>` $\to$ Resolves to `https://gautambhuwan.com.np/ielts/app.js`.
   - `<link rel="manifest" href="manifest.webmanifest">` $\to$ Resolves to `https://gautambhuwan.com.np/ielts/manifest.webmanifest`.
   - `<img src="images/logo.png">` $\to$ Resolves to `https://gautambhuwan.com.np/ielts/images/logo.png`.
2. **PWA Manifest Scope:**
   - `"start_url": "./"` $\to$ Launches at current subdirectory `/ielts/`.
   - `"scope": "./"` $\to$ Restricts PWA service worker scope to `/ielts/` without intercepting root portfolio requests.
3. **Service Worker Pre-Cache:**
   - Relative asset array: `['./', 'index.html', 'app.js', 'styles.css', 'manifest.webmanifest', 'images/...']`.
   - Automatically scopes cache to `/ielts/`.

---

## 4. HTTPS & Security Headers

1. **HTTPS Enforcement:** GitHub Pages automatically enforces HTTPS with an automated Let's Encrypt SSL certificate on `gautambhuwan.com.np`.
2. **HSTS & TLS:** Served over HTTP/2 with TLS 1.3 encryption.
3. **MIME Types:** `.webmanifest`, `.png`, `.js`, and `.css` are served with correct MIME content-type headers.

---

## 5. Website Audit Conclusion

The `/ielts/` subdirectory architecture is safe, clean, path-agnostic, and ready for public student traffic.
