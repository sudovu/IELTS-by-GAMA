# PHASE 15 — MOBILE, ANDROID & PWA/iOS PLATFORM VALIDATION REPORT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** Cross-Platform Application Release Engineer  

---

## 1. Asset Synchronization & Web Parity

The application assets were audited to ensure complete parity across Desktop Web, Android WebView, and PWA/iOS:

- **Source Web Directory:** `ui/static/`
- **Android Asset Mirror:** `platform/android/app/src/main/assets/www/`
- **iOS App Bundle Mirror:** `platform/ios/dist/ielts-by-gama.ipa` (Payload/IELTSbyGAMA.app/www/)
- **Live Deployment Mirror:** `c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts`

All files (`index.html`, `app.js`, `styles.css`, `sw.js`, `manifest.webmanifest`, images) are strictly synchronized across all four targets.

---

## 2. Platform Reality & iOS Distribution Assessment

An independent technical inspection was performed on the iOS build artifacts in `platform/ios/dist/`:

### 2.1 Artifact Inventory
1. `ielts-by-gama.ipa` (**3.78 MB**): Standard iOS application archive containing `Payload/IELTSbyGAMA.app`.
2. `ielts-by-gama.mobileconfig`: Apple WebClip Configuration Profile with `PrecomposedIcon: true`, `FullScreen: true`, and `PayloadIdentifier: com.gama.ieltsbygama`.
3. `manifest.plist`: Apple Wireless Over-The-Air (OTA) installation manifest referencing `https://gautambhuwan.com.np/downloads/ielts-by-gama/ielts-by-gama.ipa`.
4. `manifest.webmanifest`: Progressive Web App manifest for Safari "Add to Home Screen".
5. `sw.js`: Service Worker caching shell assets for offline standalone operation.

### 2.2 Honest Code Signing & Installation Realities
- **Native IPA Signing Status:**  
  The `.ipa` package contains a synthesized ARM64 Mach-O binary and web assets. **It is NOT signed with an Apple Developer Enterprise or Developer Program certificate.**  
  *Installation Reality:* It cannot be installed directly via Safari or OTA on a standard, non-jailbroken iPhone without sideloading utilities (such as AltStore, Sideloadly, TrollStore, or Xcode device pairing with a personal Apple ID).
- **WebClip Profile (`.mobileconfig`):**  
  Can be installed directly on any iOS device via Safari (`Settings -> Profile Downloaded -> Install`). Places an icon directly on the iOS Home Screen that opens the application in full-screen standalone mode without browser chrome.
- **PWA ("Add to Home Screen"):**  
  Fully functional on iOS Safari. Service worker caches app assets for offline execution.
- **Android APK / WebView:**  
  Can run directly in standard WebView with local assets (`file:///android_asset/www/index.html`) or via localhost embedded server.

---

## 3. Responsive UI & Touch Interaction Audit

| UI Component | Desktop (1920x1080) | Tablet (768x1024) | Mobile (375x667) | Usability Status |
|:---|:---:|:---:|:---:|:---:|
| **Exam Lobby** | Grid layout (4 cards/row) | 2 cards/row | 1 card/row | **PASS** |
| **Exam Split Workspace** | Side-by-side (50% / 50%) | Stacked layout | Full-width vertical tabs | **PASS** |
| **Question Navigator** | Sticky right drawer | Horizontal bar | Collapsible bottom drawer | **PASS** |
| **Countdown Timer** | Top right fixed badge | Top center banner | Sticky top pill | **PASS** |
| **Audio Playback Controls** | Fixed button group | Large touch targets | Minimum 44px tap targets | **PASS** |
| **Writing Input Area** | Expanded textarea | Responsive height | Dynamic viewport height (`100dvh`) | **PASS** |

---

## 4. Platform Testing Disclosure

- **Physical Device Disclosure:** Testing was conducted via Chromium device emulation (iPhone SE, iPad Air, Pixel 7) and Windows local runtime. Real physical iPhone hardware installation of the unsigned `.ipa` was not performed; sideloading via AltStore/Sideloadly remains required for native binary testing.
