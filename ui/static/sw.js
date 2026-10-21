// IELTS by GAMA Service Worker v1.5.3
const CACHE_NAME = 'ielts-by-gama-v1.5.3';

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
