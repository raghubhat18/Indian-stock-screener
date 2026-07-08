const CACHE_NAME = 'niftypulse-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json'
];

// Install event - caches the basic files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

// Fetch event - serves from cache if offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
