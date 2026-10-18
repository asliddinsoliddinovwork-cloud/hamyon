/* Hamyon — oflayn ishlash uchun service worker.
   Yangi versiya chiqarganda VERSION qiymatini o'zgartiring. */
const VERSION = 'hamyon-2.4.2';
const ASSETS = ['./', 'index.html', 'manifest.webmanifest', 'icons/apple-touch-icon.png', 'icons/icon-192.png', 'icons/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  // Sahifa (?add=out kabi parametrlar bilan ham) — keshdan darhol, fonda yangilash
  const key = req.mode === 'navigate' ? 'index.html' : req;
  e.respondWith(caches.open(VERSION).then(async cache => {
    const cached = await cache.match(key, { ignoreSearch: req.mode === 'navigate' });
    const fresh = fetch(req).then(res => { if (res.ok) cache.put(key, res.clone()); return res; }).catch(() => cached);
    return cached || fresh;
  }));
});
