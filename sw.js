const CACHE = 'tourniED-v4.2-i18n';
const FILES = ['./', './index.html', './manifest.json', './icon.svg', './icon-180.png'];

self.addEventListener('install', e => {
  // Tek bir dosya 404 verirse addAll tümden başarısız olur; teker teker ekle.
  e.waitUntil(
    caches.open(CACHE).then(cache =>
      Promise.all(FILES.map(f => cache.add(f).catch(() => null)))
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;

  // Sayfanın kendisi: ÖNCE AĞ. Böylece yeni sürüm yayınlandığında veri
  // toplayıcılar eski formu kullanmaya devam etmez. Ağ yoksa cache'ten aç.
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then(res => {
        const copy = res.clone();          // clone, gövde tüketilmeden alınmalı
        caches.open(CACHE).then(c => c.put('./index.html', copy));
        return res;
      }).catch(() =>
        caches.match('./index.html').then(r => r || caches.match('./'))
      )
    );
    return;
  }

  // Diğer dosyalar (manifest, ikon): önce cache, yoksa ağdan al ve sakla.
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
