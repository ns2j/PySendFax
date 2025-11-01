SW_JS='''
var cacheName = 'pysendfax'
var filesToCache = [
  './static/images/favicon.ico',
  './static/images/icon-192x192.png',
  './static/images/icon-512x512.png'
]

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return cache.addAll(filesToCache)
    })
  )
})

self.addEventListener('fetch', function(e) {
  if (e.request.method !== "POST") {
    e.respondWith(
      caches.match(e.request).then(function(response) {
        return response || fetch(e.request)
      })
    )
    return
  }
})
'''
