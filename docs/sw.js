var CACHE = 'schedule-v1';

self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) {
    return Promise.all(['/', '/static/manifest.json', '/static/icons/icon-192.png'].map(function (u) {
      return cache.add(u).catch(function () {});
    }));
  }));
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

// Сначала сеть (чтобы расписание было свежим), без интернета отдаём последнюю сохранённую копию.
self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  event.respondWith(
    fetch(req).then(function (res) {
      if (res && res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || (req.mode === 'navigate' ? caches.match('/') : undefined);
      });
    })
  );
});
