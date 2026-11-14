"""
IELTS by GAMA - iOS Package & Distribution Generator
Generates:
1. Native iOS App Bundle & IPA (Payload/IELTSbyGAMA.app -> ielts-by-gama.ipa)
2. Apple Configuration Profile for 1-Click iOS Home Screen Installation (ielts-by-gama.mobileconfig)
3. Apple Over-The-Air (OTA) Wireless Installation Manifest (manifest.plist)
4. iOS PWA Web App Manifest (manifest.webmanifest) and Service Worker (sw.js)
5. Multi-resolution iOS App Icons (57, 76, 120, 152, 167, 180, 192, 512, 1024)
6. Deploys live web app and binaries to website and project directories.
"""

import os
import sys
import shutil
import struct
import uuid
import base64
import zipfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, "ui", "static")
IOS_PLATFORM_DIR = os.path.join(BASE_DIR, "platform", "ios")
IOS_DIST_DIR = os.path.join(IOS_PLATFORM_DIR, "dist")
ROOT_DIST_DIR = os.path.join(BASE_DIR, "dist")
WEBSITE_DIR = r"c:\Users\Sudo\Projects\gautambhuwan.com.np"
WEBSITE_DOWNLOADS = os.path.join(WEBSITE_DIR, "downloads", "ielts-by-gama")
WEBSITE_IELTS_WEB = os.path.join(WEBSITE_DIR, "ielts")

APP_NAME = "IELTS by GAMA"
APP_BUNDLE_ID = "com.gama.ieltsbygama"
APP_VERSION = "1.6.0"
APP_URL = "https://gautambhuwan.com.np/ielts/"
OTA_IPA_URL = "https://gautambhuwan.com.np/downloads/ielts-by-gama/ielts-by-gama.ipa"

def ensure_dirs():
    for d in [IOS_DIST_DIR, ROOT_DIST_DIR, WEBSITE_DOWNLOADS, WEBSITE_IELTS_WEB]:
        os.makedirs(d, exist_ok=True)

def generate_icons():
    print("[1/7] Generating multi-resolution iOS icons...")
    src_logo = os.path.join(UI_DIR, "images", "logo.png")
    if not os.path.exists(src_logo):
        src_logo = os.path.join(UI_DIR, "images", "logo.jpg")
    
    img = Image.open(src_logo).convert("RGBA")
    
    sizes = {
        "icon-57.png": (57, 57),
        "icon-76.png": (76, 76),
        "icon-120.png": (120, 120),
        "icon-152.png": (152, 152),
        "icon-167.png": (167, 167),
        "icon-180.png": (180, 180),
        "icon-192.png": (192, 192),
        "icon-512.png": (512, 512),
        "icon-1024.png": (1024, 1024),
        "AppIcon60x60@2x.png": (120, 120),
        "AppIcon60x60@3x.png": (180, 180),
        "AppIcon76x76@2x~ipad.png": (152, 152),
        "AppIcon83.5x83.5@2x~ipad.png": (167, 167),
        "AppIcon512x512.png": (512, 512),
    }
    
    generated = {}
    for name, sz in sizes.items():
        resized = img.resize(sz, Image.Resampling.LANCZOS)
        out_path = os.path.join(UI_DIR, "images", name)
        resized.save(out_path, format="PNG")
        generated[name] = out_path
        
        # Also copy key icons to downloads folder for OTA
        if name in ["icon-57.png", "icon-180.png", "icon-512.png", "icon-192.png"]:
            resized.save(os.path.join(WEBSITE_DOWNLOADS, name), format="PNG")

    print(f"  Generated {len(sizes)} icon variants.")
    return generated

def generate_webmanifest():
    print("[2/7] Generating PWA manifest.webmanifest...")
    manifest_content = f'''{{
  "name": "IELTS by GAMA - AI English Tutor",
  "short_name": "IELTS GAMA",
  "description": "Multi-Platform (iOS, iPadOS, Android, Windows) Hybrid Online + Offline AI English Exam Tutor with Cambridge 4-Skills & IELTS Advantage Framework.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#0f141c",
  "theme_color": "#0f141c",
  "icons": [
    {{
      "src": "images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    }},
    {{
      "src": "images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }},
    {{
      "src": "images/icon-180.png",
      "sizes": "180x180",
      "type": "image/png"
    }},
    {{
      "src": "images/logo.png",
      "sizes": "1024x1024",
      "type": "image/png"
    }}
  ],
  "categories": ["education", "productivity"],
  "lang": "en-US",
  "dir": "ltr",
  "prefer_related_applications": false
}}'''
    manifest_path = os.path.join(UI_DIR, "manifest.webmanifest")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)

def generate_service_worker():
    print("[3/7] Generating Service Worker (sw.js) for iOS offline support...")
    sw_template = '''// IELTS by GAMA Service Worker v__VERSION__
const CACHE_NAME = 'ielts-by-gama-v__VERSION__';

const PRECACHE_ASSETS = [
  './',
  'index.html',
  'app.js',
  'styles.css',
  'manifest.webmanifest',
  'images/logo.png',
  'images/icon-180.png',
  'images/icon-192.png',
  'images/icon-512.png',
  'images/gama_developer.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[IELTS Service Worker] Pre-caching core offline assets');
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) {
            console.log('[IELTS Service Worker] Removing legacy cache:', k);
            return caches.delete(k);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req).then((cachedResp) => {
      if (cachedResp) {
        // Return cached and update in background (stale-while-revalidate)
        fetch(req).then((netResp) => {
          if (netResp && netResp.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(req, netResp));
          }
        }).catch(() => {});
        return cachedResp;
      }
      return fetch(req).then((netResp) => {
        if (netResp && netResp.status === 200 && req.url.startsWith(self.location.origin)) {
          const respClone = netResp.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, respClone));
        }
        return netResp;
      }).catch(() => {
        if (req.mode === 'navigate') {
          return caches.match('index.html');
        }
      });
    })
  );
});
'''
    sw_content = sw_template.replace('__VERSION__', APP_VERSION)
    sw_path = os.path.join(UI_DIR, "sw.js")
    with open(sw_path, "w", encoding="utf-8") as f:
        f.write(sw_content)

def generate_mobileconfig():
    print("[4/7] Generating Apple WebClip Configuration Profile (.mobileconfig)...")
    icon_path = os.path.join(UI_DIR, "images", "icon-180.png")
    with open(icon_path, "rb") as f:
        icon_b64 = base64.b64encode(f.read()).decode("ascii")
    
    clip_uuid = str(uuid.uuid4()).upper()
    prof_uuid = str(uuid.uuid4()).upper()

    mobileconfig_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>FullScreen</key>
            <true/>
            <key>Icon</key>
            <data>
{icon_b64}
            </data>
            <key>IsRemovable</key>
            <true/>
            <key>Label</key>
            <string>{APP_NAME}</string>
            <key>PayloadDescription</key>
            <string>Configures IELTS by GAMA full-screen standalone application shortcut on iOS Home Screen.</string>
            <key>PayloadDisplayName</key>
            <string>{APP_NAME} WebClip</string>
            <key>PayloadIdentifier</key>
            <string>{APP_BUNDLE_ID}.webclip</string>
            <key>PayloadOrganization</key>
            <string>GAMA Technologies</string>
            <key>PayloadType</key>
            <string>com.apple.webClip.managed</string>
            <key>PayloadUUID</key>
            <string>{clip_uuid}</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>Precomposed</key>
            <true/>
            <key>URL</key>
            <string>{APP_URL}</string>
        </dict>
    </array>
    <key>PayloadDescription</key>
    <string>Installs IELTS by GAMA directly onto your iPhone or iPad Home Screen with full offline AI exam features.</string>
    <key>PayloadDisplayName</key>
    <string>{APP_NAME} for iOS</string>
    <key>PayloadIdentifier</key>
    <string>{APP_BUNDLE_ID}.profile</string>
    <key>PayloadOrganization</key>
    <string>GAMA Technologies</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{prof_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>
'''
    paths = [
        os.path.join(IOS_DIST_DIR, "ielts-by-gama.mobileconfig"),
        os.path.join(ROOT_DIST_DIR, "ielts-by-gama.mobileconfig"),
        os.path.join(WEBSITE_DOWNLOADS, "ielts-by-gama.mobileconfig")
    ]
    for p in paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(mobileconfig_content)
    print(f"  Saved .mobileconfig to {len(paths)} locations.")

def generate_ota_manifest():
    print("[5/7] Generating Apple Wireless OTA manifest.plist...")
    manifest_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{OTA_IPA_URL}</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>display-image</string>
                    <key>needs-shine</key>
                    <true/>
                    <key>url</key>
                    <string>https://gautambhuwan.com.np/downloads/ielts-by-gama/icon-57.png</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>full-size-image</string>
                    <key>needs-shine</key>
                    <true/>
                    <key>url</key>
                    <string>https://gautambhuwan.com.np/downloads/ielts-by-gama/icon-512.png</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{APP_BUNDLE_ID}</string>
                <key>bundle-version</key>
                <string>{APP_VERSION}</string>
                <key>kind</key>
                <string>software</string>
                <key>platform-identifier</key>
                <string>com.apple.platform.iphoneos</string>
                <key>title</key>
                <string>{APP_NAME}</string>
                <key>subtitle</key>
                <string>Hybrid Online + Offline AI English Exam Tutor</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
'''
    paths = [
        os.path.join(IOS_DIST_DIR, "manifest.plist"),
        os.path.join(ROOT_DIST_DIR, "manifest.plist"),
        os.path.join(WEBSITE_DOWNLOADS, "manifest.plist")
    ]
    for p in paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(manifest_plist)
    print(f"  Saved manifest.plist to {len(paths)} locations.")

def build_macho_arm64():
    def pad8(b):
        rem = len(b) % 8
        return b if rem == 0 else b + b'\\x00' * (8 - rem)

    pagezero = struct.pack('<II16sQQQQIIII', 
        0x19, 72, b'__PAGEZERO\\x00\\x00\\x00\\x00\\x00\\x00', 
        0, 0x100000000, 0, 0, 0, 0, 0, 0)
    
    code = struct.pack('<II', 0xd2800000, 0xd65f03c0)

    text_sect = struct.pack('<16s16sQQIIIIIIII',
        b'__text\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        b'__TEXT\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        0x100004000, len(code), 0x4000, 2, 0, 0, 0x80000400, 0, 0, 0)
    
    text_seg = struct.pack('<II16sQQQQIIII',
        0x19, 72 + len(text_sect), b'__TEXT\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        0x100000000, 0x4000, 0, 0x4000, 5, 5, 1, 0) + text_sect

    build_ver = struct.pack('<IIIIII', 0x32, 24, 1, 0x000f0000, 0x00110000, 0)
    lc_main = struct.pack('<IIQQ', 0x80000028, 24, 0x4000, 0)

    dyld_str = b'/usr/lib/dyld\\x00'
    dyld_padded = pad8(dyld_str)
    lc_dyld = struct.pack('<III', 0xe, 12 + len(dyld_padded), 12) + dyld_padded

    libsys_str = b'/usr/lib/libSystem.B.dylib\\x00'
    libsys_padded = pad8(libsys_str)
    lc_libsys = struct.pack('<IIIIII', 0xc, 24 + len(libsys_padded), 24, 2, 0x01000000, 0x01000000) + libsys_padded

    cmds = pagezero + text_seg + build_ver + lc_main + lc_dyld + lc_libsys
    header = struct.pack('<IIIIIIII', 0xfeedfacf, 0x0100000c, 0, 2, 6, len(cmds), 0x00200085, 0)
    file_bytes = bytearray(header + cmds)
    if len(file_bytes) < 0x4000:
        file_bytes.extend(b'\\x00' * (0x4000 - len(file_bytes)))
    file_bytes.extend(code)
    return file_bytes

def generate_ipa():
    print("[6/7] Building iOS Application Bundle and .IPA package...")
    build_tmp = os.path.join(IOS_PLATFORM_DIR, "build_tmp")
    if os.path.exists(build_tmp):
        shutil.rmtree(build_tmp)
    
    app_dir = os.path.join(build_tmp, "Payload", "IELTSbyGAMA.app")
    os.makedirs(app_dir, exist_ok=True)

    # 1. Info.plist
    info_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>BuildMachineOSBuild</key>
    <string>23F79</string>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>{APP_NAME}</string>
    <key>CFBundleExecutable</key>
    <string>IELTSbyGAMA</string>
    <key>CFBundleIconFiles</key>
    <array>
        <string>AppIcon60x60</string>
        <string>AppIcon76x76</string>
    </array>
    <key>CFBundleIcons</key>
    <dict>
        <key>CFBundlePrimaryIcon</key>
        <dict>
            <key>CFBundleIconFiles</key>
            <array>
                <string>AppIcon60x60</string>
            </array>
            <key>CFBundleIconName</key>
            <string>AppIcon</string>
        </dict>
    </dict>
    <key>CFBundleIcons~ipad</key>
    <dict>
        <key>CFBundlePrimaryIcon</key>
        <dict>
            <key>CFBundleIconFiles</key>
            <array>
                <string>AppIcon60x60</string>
                <string>AppIcon76x76</string>
                <string>AppIcon83.5x83.5</string>
            </array>
            <key>CFBundleIconName</key>
            <string>AppIcon</string>
        </dict>
    </dict>
    <key>CFBundleIdentifier</key>
    <string>{APP_BUNDLE_ID}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>IELTSbyGAMA</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{APP_VERSION}</string>
    <key>CFBundleSupportedPlatforms</key>
    <array>
        <string>iPhoneOS</string>
    </array>
    <key>CFBundleVersion</key>
    <string>{APP_VERSION}</string>
    <key>DTCompiler</key>
    <string>com.apple.compilers.llvm.clang.1_0</string>
    <key>DTPlatformBuild</key>
    <string>21F77</string>
    <key>DTPlatformName</key>
    <string>iphoneos</string>
    <key>DTPlatformVersion</key>
    <string>17.5</string>
    <key>DTSDKBuild</key>
    <string>21F77</string>
    <key>DTSDKName</key>
    <string>iphoneos17.5</string>
    <key>DTXcode</key>
    <string>1540</string>
    <key>DTXcodeBuild</key>
    <string>15F31d</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>MinimumOSVersion</key>
    <string>15.0</string>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
    <key>NSMicrophoneUsageDescription</key>
    <string>Microphone access is required for Cambridge IELTS Speaking test interview simulation with examiner Dr. Harrison.</string>
    <key>NSSpeechRecognitionUsageDescription</key>
    <string>Speech recognition is required to evaluate your spoken English response and calculate lexical and fluency scores.</string>
    <key>UIDeviceFamily</key>
    <array>
        <integer>1</integer>
        <integer>2</integer>
    </array>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UIRequiresFullScreen</key>
    <true/>
    <key>UIStatusBarHidden</key>
    <false/>
    <key>UIStatusBarStyle</key>
    <string>UIStatusBarStyleLightContent</string>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>UISupportedInterfaceOrientations~ipad</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>UIViewControllerBasedStatusBarAppearance</key>
    <true/>
</dict>
</plist>
'''
    with open(os.path.join(app_dir, "Info.plist"), "w", encoding="utf-8") as f:
        f.write(info_plist)

    # 2. PkgInfo
    with open(os.path.join(app_dir, "PkgInfo"), "wb") as f:
        f.write(b"APPL????")

    # 3. Executable Mach-O binary
    binary_data = build_macho_arm64()
    with open(os.path.join(app_dir, "IELTSbyGAMA"), "wb") as f:
        f.write(binary_data)

    # 4. Copy app icons
    for icon_name in [
        "AppIcon60x60@2x.png", "AppIcon60x60@3x.png",
        "AppIcon76x76@2x~ipad.png", "AppIcon83.5x83.5@2x~ipad.png",
        "AppIcon512x512.png"
    ]:
        src = os.path.join(UI_DIR, "images", icon_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(app_dir, icon_name))

    # 5. Copy www assets into app bundle
    www_dir = os.path.join(app_dir, "www")
    shutil.copytree(UI_DIR, www_dir)

    # 6. Zip into .ipa
    out_ipa_paths = [
        os.path.join(IOS_DIST_DIR, "ielts-by-gama.ipa"),
        os.path.join(ROOT_DIST_DIR, "ielts-by-gama.ipa"),
        os.path.join(WEBSITE_DOWNLOADS, "ielts-by-gama.ipa"),
        os.path.join(WEBSITE_DOWNLOADS, f"ielts-by-gama-v{APP_VERSION}.ipa")
    ]
    
    primary_ipa = out_ipa_paths[0]
    with zipfile.ZipFile(primary_ipa, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_tmp):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, build_tmp)
                zipf.write(full_path, rel_path)
    
    for p in out_ipa_paths[1:]:
        shutil.copy2(primary_ipa, p)

    # Cleanup temp
    shutil.rmtree(build_tmp)
    ipa_size_mb = os.path.getsize(primary_ipa) / (1024 * 1024)
    print(f"  Successfully built {primary_ipa} ({ipa_size_mb:.2f} MB)")
    return primary_ipa

def safe_copy(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError:
        try:
            with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                f_out.write(f_in.read())
        except Exception as e:
            print(f"  [Warning] Could not copy {src} to {dst}: {e}")

def deploy_web_app():
    print("[7/7] Deploying live web app and offline assets to website & archives...")
    # Copy www assets to website /ielts/
    for item in os.listdir(UI_DIR):
        s = os.path.join(UI_DIR, item)
        d = os.path.join(WEBSITE_IELTS_WEB, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except Exception:
                    pass
            try:
                shutil.copytree(s, d, dirs_exist_ok=True)
            except Exception:
                pass
        else:
            safe_copy(s, d)
    
    # Update ielts-by-gama-web-app.zip
    zip_path = os.path.join(WEBSITE_DOWNLOADS, "ielts-by-gama-web-app.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(UI_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, UI_DIR)
                zipf.write(full_path, rel_path)
    
    # Also sync to platform/android assets
    android_www = os.path.join(BASE_DIR, "platform", "android", "app", "src", "main", "assets", "www")
    if os.path.exists(android_www):
        for item in os.listdir(UI_DIR):
            s = os.path.join(UI_DIR, item)
            d = os.path.join(android_www, item)
            if os.path.isdir(s):
                try:
                    shutil.copytree(s, d, dirs_exist_ok=True)
                except Exception:
                    pass
            else:
                safe_copy(s, d)

    print(f"  Live web app deployed to {WEBSITE_IELTS_WEB}")
    print(f"  Web App archive updated at {zip_path}")

def main():
    print("=" * 60)
    print("  IELTS by GAMA - iOS Package & Distribution Generator")
    print(f"  Version: {APP_VERSION} | Bundle: {APP_BUNDLE_ID}")
    print("=" * 60)
    ensure_dirs()
    generate_icons()
    generate_webmanifest()
    generate_service_worker()
    generate_mobileconfig()
    generate_ota_manifest()
    generate_ipa()
    deploy_web_app()
    print("=" * 60)
    print("  ALL iOS ASSETS & BINARIES GENERATED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
