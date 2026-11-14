# Platform Validation Report: IELTS by GAMA (v1.6.0)
**Date:** November 14, 2026  
**Auditor:** Cross-Platform Application Release Engineer  
**Scope:** Web Browser PWA, Android WebView / Tablet, Apple iOS Multi-Channel Distribution

---

## 1. Executive Summary

This report evaluates platform compatibility, packaging, distribution mechanisms, and runtime behavior for **IELTS by GAMA** version `1.6.0` across:
1. **Modern Desktop & Mobile Browsers (Web / PWA)**
2. **Android Phones & Tablets (WebView / Native APK)**
3. **Apple iOS Devices (iPhone & iPad)**

---

## 2. Web & Progressive Web App (PWA) Validation (Phase 11G)

### Asset Inventory & Sync
- **Location:** `ui/static/`
- **Core Files:**
  - `index.html`: Responsive single-page application shell.
  - `app.js`: Client-side state manager, routing, local mock exams, offline evaluator.
  - `style.css`: Clean, high-contrast, distraction-free UI with CSS variable theming.
  - `manifest.webmanifest`: PWA manifest defining `display: standalone`, icons, and app metadata.
  - `sw.js`: Service Worker providing cache-first offline asset delivery.
- **Offline PWA Capability:**
  - When installed from a browser, the application loads immediately without an internet connection.
  - Service worker caches all static assets (`app.js`, `style.css`, icons, fonts).

---

## 3. Android Platform Validation (Phase 11G)

### Project Configuration
- **Location:** `platform/android/`
- **Build System:** Gradle with Android Gradle Plugin (AGP).
- **Target SDK:** Android 14 (API 34).
- **Minimum SDK:** Android 8.0 (API 26) covering 95%+ of active devices globally.
- **Synchronized Assets:** `platform/android/app/src/main/assets/www/` is kept in 100% bit-for-bit parity with `ui/static/`.
- **Hardware Profile Adaptation:** The embedded WebView integrates with local Android hardware profiles (Low-RAM, Medium, High-RAM) to throttle background intervals on budget devices.

---

## 4. Apple iOS Distribution & Installation Reality (Phase 11G & 11H)

### Technical Analysis of iOS Architecture
Apple's iOS operating system imposes cryptographic code-signing requirements that govern how applications can be installed on iPhones and iPads:

1. **Native Signed IPA (App Store / Enterprise):**
   - Direct over-the-air (OTA) installation of a native `.ipa` requires an active Apple Developer Team provisioning profile or an Enterprise Distribution Certificate registered to the device's UDID.
   - Without an enterprise certificate, raw `.ipa` files cannot be installed via Safari download.
2. **Sideloading (AltStore / Sideloadly / TrollStore):**
   - The compiled `ielts-by-gama.ipa` located in `platform/ios/dist/` (3.76 MB) is an ARM64 native Mach-O application bundle.
   - Users with AltStore, Sideloadly, or TrollStore can sign and sideload this IPA directly onto any device.
3. **Apple WebClip Configuration Profile (`.mobileconfig`):**
   - iOS supports Configuration Profiles via Apple's Mobile Device Management (MDM) framework.
   - `ielts-by-gama.mobileconfig` installs a full-screen, standalone application icon directly to the iOS Home Screen in one click from Safari.
   - It requires **no developer account, no code-signing certificate, and no App Store approval**.
   - It runs in full-screen standalone mode without Safari browser chrome or navigation bars.
4. **Safari "Add to Home Screen" (PWA):**
   - Any iOS user visiting `https://gautambhuwan.com.np/ielts/` can tap Share -> *"Add to Home Screen"*.
   - The embedded `sw.js` precaches the application, making it 100% functional offline.

### Verification of iOS Release Artifacts
All 3 distribution formats were compiled, tested, and published to the website downloads repository:

| Artifact | File Path | Size | Target Installation Method |
|:---|:---|:---:|:---|
| **Apple Configuration Profile** | `dist/ielts-by-gama.mobileconfig` | 2.1 KB | Direct 1-Click Install via Safari on iOS |
| **PWA Service Worker** | `ui/static/sw.js` | 2.4 KB | Offline caching for Safari / Chrome PWA |
| **iOS Application IPA** | `platform/ios/dist/ielts-by-gama.ipa` | 3.76 MB | Sideloading via AltStore / Sideloadly |
| **Apple OTA Manifest** | `dist/manifest.plist` | 1.8 KB | Enterprise wireless installation manifest |
| **Standalone Web Bundle** | `downloads/ielts-by-gama/ielts-by-gama-web-app.zip` | 2.9 MB | Offline extraction or self-hosted deployment |

---

## 5. Screen Fitting & Layout Validation (Phases 11G)

### Dynamic Viewport Handling
- Previous versions exhibited minor gaps or viewport cutoffs on specific display aspect ratios.
- In `v1.6.0`, layout was hardened with:
  - `min-height: 100dvh` (Dynamic Viewport Height) to eliminate mobile browser URL-bar clipping.
  - Safe-area inset padding: `padding-top: env(safe-area-inset-top)` and `padding-bottom: env(safe-area-inset-bottom)` to accommodate iPhone Dynamic Island, camera notches, and Android navigation bars.
  - Snug container fitting with CSS Grid and Flexbox wrapping.

---

## 6. Platform Sign-Off
All target platforms (Web, Android, iOS) are verified and supported with appropriate installation paths and documentation.
