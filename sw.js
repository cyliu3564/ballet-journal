const CACHE_NAME = 'ballet-app-v49';

// No-op service worker - does NOT intercept fetch requests
// Only exists for PWA installability and version tracking
// Prevents cache-related white screen issues

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  // Clean up old caches from previous versions
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// No fetch handler - all requests go directly to the network
// This avoids the "Returned response is null" error entirely

self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
