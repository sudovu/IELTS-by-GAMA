import os

dev_path = r"c:\Users\Sudo\Projects\gautambhuwan.com.np\developments.html"

with open(dev_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Download Buttons Strip
old_strip = """        <!-- Download Buttons Strip -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
          <a href="downloads/ielts-by-gama/ielts-by-gama-release.apk" class="btn btn-primary btn-sm" style="background: #6366f1; border-color: #6366f1; color: #fff; font-weight: 700; padding: 10px 18px;" download>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -2px; margin-right: 4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download Latest v1.5.3 APK (23.9 MB)
          </a>
          <a href="downloads/ielts-by-gama/ielts-by-gama-tablet-android11+.apk" class="btn btn-secondary btn-sm" download>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -2px; margin-right: 4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Tablet Edition v1.5.3 (23.9 MB)
          </a>
          <a href="downloads/ielts-by-gama/ielts-by-gama-web-app.zip" class="btn btn-secondary btn-sm" download>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -2px; margin-right: 4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Web PWA Bundle (1.30 MB)
          </a>
          <a href="https://github.com/sudovu/IELTS-by-GAMA" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">
            GitHub Source Repository &rarr;
          </a>
          <a href="#ielts-releases" class="btn btn-outline btn-sm">
            Release Archive (v1.0 – v1.5.3) &darr;
          </a>
        </div>"""

new_strip = """        <!-- Download & Direct Install Actions Strip -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; align-items: center;">
          <!-- Android Direct Download -->
          <a href="downloads/ielts-by-gama/ielts-by-gama-release.apk" class="btn btn-primary btn-sm" style="background: #6366f1; border-color: #6366f1; color: #fff; font-weight: 700; padding: 10px 18px;" download>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -2px; margin-right: 4px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download Android APK (23.9 MB)
          </a>

          <!-- iOS Direct Sideload IPA -->
          <a href="downloads/ielts-by-gama/ielts-by-gama.ipa" class="btn btn-secondary btn-sm" style="border-color: rgba(99, 102, 241, 0.45); color: #818cf8; font-weight: 700; padding: 10px 16px;" download title="Direct .IPA binary for AltStore, Sideloadly, TrollStore, Scarlet">
            🍎 Download iOS .IPA (3.7 MB)
          </a>

          <!-- iOS 1-Click Profile -->
          <a href="downloads/ielts-by-gama/ielts-by-gama.mobileconfig" class="btn btn-secondary btn-sm" style="padding: 10px 16px;" download title="1-Click Apple Configuration Profile for instant Home Screen install">
            📲 1-Click iOS Profile (.mobileconfig)
          </a>

          <!-- Wireless OTA Install -->
          <a href="itms-services://?action=download-manifest&url=https://gautambhuwan.com.np/downloads/ielts-by-gama/manifest.plist" class="btn btn-secondary btn-sm" style="padding: 10px 16px;" title="Wireless Over-The-Air install for iOS devices">
            📡 Wireless iOS Install
          </a>

          <!-- Live Web App / PWA -->
          <a href="ielts/" target="_blank" class="btn btn-secondary btn-sm" style="padding: 10px 16px; border-color: rgba(16, 185, 129, 0.4); color: #34d399; font-weight: 600;">
            🌐 Launch Live Web App (PWA) &rarr;
          </a>

          <!-- Source & Archive -->
          <a href="https://github.com/sudovu/IELTS-by-GAMA" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">
            GitHub Source &rarr;
          </a>
          <a href="#ielts-releases" class="btn btn-outline btn-sm">
            Release Archive (v1.0 – v1.5.3) &darr;
          </a>
        </div>"""

if old_strip in html:
    html = html.replace(old_strip, new_strip, 1)
    print("Updated Download & Install buttons successfully.")
else:
    # Try normalizing newlines
    html_norm = html.replace("\r\n", "\n")
    old_norm = old_strip.replace("\r\n", "\n")
    new_norm = new_strip.replace("\r\n", "\n")
    if old_norm in html_norm:
        html = html_norm.replace(old_norm, new_norm, 1)
        print("Updated Download & Install buttons successfully (newline normalized).")
    else:
        print("Warning: old_strip not found!")

# 2. Update Release Archive v1.5.3 row to include iOS binary options
old_v153_row = """              <!-- v1.5.3 -->
              <tr style="border-bottom: 1px solid var(--border); background: rgba(99, 102, 241, 0.08);">
                <td style="padding: 18px 20px; vertical-align: top;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <strong style="color: var(--text-primary); font-size: 1rem;">v1.5.3</strong>
                    <span class="status-pill" style="font-size: 0.68rem; padding: 2px 6px; border-color: rgba(99, 102, 241, 0.5);"><span class="status-dot" style="background: #818cf8;"></span> LATEST</span>
                  </div>
                </td>
                <td style="padding: 18px 20px; color: var(--text-secondary); vertical-align: top; white-space: nowrap;">October 2026</td>
                <td style="padding: 18px 20px; color: var(--text-secondary); vertical-align: top;">
                  <strong>Balanced 4-Category Segmented Filter &amp; Flawless Interactive Navigation Engine:</strong>
                  Fully equipped all 4 core category filters (<em>Strategy &amp; Core</em>, <em>4-Skills Exam</em>, <em>Advantage &amp; Drills</em>, <em>Tracking &amp; System</em>) with balanced equal flex distribution, eliminating button void gaps. Removed legacy 'All(12)' grammar filter with Conditionals default. Assigned all interactive functions across all modules (Speaking Interview, Writing Studio, Cloze Checking, Mistake Book, Data Export/Import) to window for 100% cross-platform touch reliability across Tablet, iOS, Windows, and Android. Calibrated responsive daylight typography and high-contrast light mode styling.
                </td>
                <td style="padding: 18px 20px; color: var(--text-muted); font-family: var(--font-mono); font-size: 0.82rem; vertical-align: top; white-space: nowrap;">23.9 MB</td>
                <td style="padding: 18px 20px; text-align: right; vertical-align: top; white-space: nowrap;">
                  <a href="downloads/ielts-by-gama/ielts-by-gama-release.apk" class="btn btn-primary btn-sm" style="background: #6366f1; border-color: #6366f1; color: #fff; font-weight: 700;" download>APK</a>
                </td>
              </tr>"""

new_v153_row = """              <!-- v1.5.3 -->
              <tr style="border-bottom: 1px solid var(--border); background: rgba(99, 102, 241, 0.08);">
                <td style="padding: 18px 20px; vertical-align: top;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <strong style="color: var(--text-primary); font-size: 1rem;">v1.5.3</strong>
                    <span class="status-pill" style="font-size: 0.68rem; padding: 2px 6px; border-color: rgba(99, 102, 241, 0.5);"><span class="status-dot" style="background: #818cf8;"></span> LATEST</span>
                  </div>
                </td>
                <td style="padding: 18px 20px; color: var(--text-secondary); vertical-align: top; white-space: nowrap;">October 2026</td>
                <td style="padding: 18px 20px; color: var(--text-secondary); vertical-align: top;">
                  <strong>Direct iOS Download &amp; Sideloading Ecosystem + 4-Category Segmented Filter &amp; Flawless Cross-Platform Engine:</strong>
                  Introduced direct iOS binary distribution: downloadable <strong>.IPA</strong> (3.7 MB) for AltStore, Sideloadly, TrollStore, Scarlet, or Xcode sideloading; 1-click Apple Configuration Profile (<strong>.mobileconfig</strong>) for native Home Screen installation with custom branding and standalone windowing; Apple Wireless Over-The-Air (<strong>OTA</strong>) manifest; and live offline Progressive Web App (<strong>PWA</strong>) with Service Worker caching. Equipped all 4 core category filters (<em>Strategy &amp; Core</em>, <em>4-Skills Exam</em>, <em>Advantage &amp; Drills</em>, <em>Tracking &amp; System</em>) with balanced equal flex distribution, eliminating button void gaps. Assigned all interactive functions across all modules to window for 100% cross-platform touch reliability across Tablet, iOS, Windows, and Android.
                </td>
                <td style="padding: 18px 20px; color: var(--text-muted); font-family: var(--font-mono); font-size: 0.78rem; vertical-align: top; white-space: nowrap;">
                  23.9 MB (APK)<br>
                  3.7 MB (IPA)<br>
                  64 KB (Profile)
                </td>
                <td style="padding: 18px 20px; text-align: right; vertical-align: top; white-space: nowrap;">
                  <div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end;">
                    <a href="downloads/ielts-by-gama/ielts-by-gama-release.apk" class="btn btn-primary btn-sm" style="background: #6366f1; border-color: #6366f1; color: #fff; font-weight: 700;" download>Android APK</a>
                    <a href="downloads/ielts-by-gama/ielts-by-gama.ipa" class="btn btn-secondary btn-sm" style="border-color: #818cf8; color: #818cf8; font-weight: 600;" download>iOS .IPA</a>
                    <a href="downloads/ielts-by-gama/ielts-by-gama.mobileconfig" class="btn btn-secondary btn-sm" style="font-size: 0.75rem;" download>iOS Profile</a>
                    <a href="ielts/" target="_blank" class="btn btn-secondary btn-sm" style="font-size: 0.75rem; border-color: #34d399; color: #34d399;">Web App</a>
                  </div>
                </td>
              </tr>"""

if old_v153_row in html:
    html = html.replace(old_v153_row, new_v153_row, 1)
    print("Updated Release Archive v1.5.3 row successfully.")
else:
    html_norm = html.replace("\r\n", "\n")
    old_norm = old_v153_row.replace("\r\n", "\n")
    new_norm = new_v153_row.replace("\r\n", "\n")
    if old_norm in html_norm:
        html = html_norm.replace(old_norm, new_norm, 1)
        print("Updated Release Archive v1.5.3 row successfully (newline normalized).")
    else:
        print("Warning: old_v153_row not found!")

with open(dev_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Developments.html written successfully.")
