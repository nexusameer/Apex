// Service Worker for aggressive mobile performance
const CACHE_NAME = 'mind-relief-v1';
const STATIC_CACHE_URLS = [
  '/static/assets/css/main.css',
  '/static/assets/vendor/bootstrap/css/bootstrap.min.css',
  '/static/assets/js/main.js',
  '/static/assets/vendor/bootstrap/js/bootstrap.bundle.min.js',
  '/static/assets/img/health/showcase-1-lcp.webp',
  '/static/assets/img/health/showcase-1-mobile.webp',
  '/static/assets/img/logo.png',
  '/static/assets/img/favicon.png'
];

// Install event - cache critical resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(STATIC_CACHE_URLS);
      })
  );
  self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache first
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});
