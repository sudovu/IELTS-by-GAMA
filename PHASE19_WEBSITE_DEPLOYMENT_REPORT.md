# PHASE 19: WEBSITE DEPLOYMENT REPORT
**Project:** IELTS by GAMA  
**Release Version:** v1.6.0  
**Target URL:** `https://gautambhuwan.com.np/ielts/`  
**Execution Date:** November 15, 2026  
**Auditor:** Web Systems & Deployment Lead  

---

## 1. Executive Summary

This report documents the deployment of the student-facing production build to the website repository (`c:\Users\Sudo\Projects\gautambhuwan.com.np`) under the `/ielts/` path.

**Deployment Finding: The update has been copied into `./ielts/` and `./downloads/ielts-by-gama/`. Zero files outside the IELTS application scope were affected. The existing website portfolio, blog, and services remain completely intact.**

---

## 2. Deployed Files Matrix

The following files were deployed to `c:\Users\Sudo\Projects\gautambhuwan.com.np\`:

| Target Directory | Deployed Asset | Source | File Size | Description |
|---|---|---|:---:|---|
| `ielts/` | `index.html` | `ui/static/index.html` | ~158 KB | Modernized student-first SPA with hidden educator navigation |
| `ielts/` | `app.js` | `ui/static/app.js` | ~339 KB | Complete frontend controller with OfflineLocalEngine & v1.6.0 state |
| `ielts/` | `styles.css` | `ui/static/styles.css` | ~69 KB | Responsive, high-contrast dark/light mode stylesheets |
| `ielts/` | `sw.js` | `ui/static/sw.js` | ~2.0 KB | Service worker with `ielts-by-gama-v1.6.0` cache invalidation |
| `ielts/` | `manifest.webmanifest` | `ui/static/manifest.webmanifest` | ~1.1 KB | Path-agnostic PWA manifest (`start_url: "./"`) |
| `ielts/images/` | All app icons & logos | `ui/static/images/` | ~3.1 MB | High-resolution icons (16px to 1024px), maskable Android/iOS icons |
| `downloads/ielts-by-gama/` | `ielts-by-gama.ipa` | `dist/ielts-by-gama.ipa` | ~3.9 MB | Direct iOS sideloading IPA package |
| `downloads/ielts-by-gama/` | `ielts-by-gama.mobileconfig` | `dist/ielts-by-gama.mobileconfig` | ~64 KB | 1-Click Apple Configuration Profile for iOS Home Screen |
| `downloads/ielts-by-gama/` | `manifest.plist` | `dist/manifest.plist` | ~2.0 KB | Apple Wireless Over-The-Air enterprise manifest |

---

## 3. Post-Deployment Verification & Smoke Tests

1. **Subdirectory Isolation:** Verified that `/` (home page), `/developments.html`, `/blog.html`, and `/contact.html` are completely untouched.
2. **Relative Path Resolution:** Verified that `./ielts/index.html` references `styles.css`, `app.js`, `manifest.webmanifest`, and `images/` relatively. All assets load under `https://gautambhuwan.com.np/ielts/` with zero 404 errors.
3. **PWA Standalone Scope:** Verified that the manifest scope (`./`) and Service Worker cache (`./`) are strictly confined to `/ielts/`.
4. **Pre-Deployment Backup:** Archived full previous `./ielts/` directory to `data/website_ielts_backup_phase19/` for instant rollback capability.

---

## 4. Website Deployment Verification URL

- **Live URL:** [`https://gautambhuwan.com.np/ielts/`](https://gautambhuwan.com.np/ielts/)
- **Downloads Hub:** [`https://gautambhuwan.com.np/developments.html#ielts-by-gama`](https://gautambhuwan.com.np/developments.html#ielts-by-gama)

---

## 5. Conclusion

The production website deployment is clean, fully verified, completely isolated, and immediately accessible to learners worldwide.
