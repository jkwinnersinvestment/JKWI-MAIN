// Service Worker for offline functionality and PWA support
const CACHE_NAME = 'jkwi-v1.0.0';
const STATIC_CACHE = 'jkwi-static-v1.0.0';
const DYNAMIC_CACHE = 'jkwi-dynamic-v1.0.0';

// Files to cache for offline access
const STATIC_FILES = [
    '/',
    '/static/css/cloud-styles.css',
    '/static/js/cloud-app.js',
    '/static/manifest.json',
    '../DESIGN%20SYSTEM/JKWI%20LOGO/JKWI%20LOGO%20PNG/JK%20WINNERS%20INVESTMENT.png'
];

// API endpoints to cache for offline access
const API_CACHE_PATTERNS = [
    /\/api\/stats/,
    /\/api\/company/,
    /\/api\/divisions/,
    /\/api\/health/
];

// Install Service Worker
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static files...');
                return cache.addAll(STATIC_FILES);
            })
            .then(() => {
                console.log('Static files cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Failed to cache static files:', error);
            })
    );
});

// Activate Service Worker
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                // Clean up old caches
                return Promise.all(
                    cacheNames
                        .filter(cacheName => 
                            cacheName.startsWith('jkwi-') && 
                            cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE
                        )
                        .map(cacheName => {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => {
                console.log('Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch handler - Network First for API, Cache First for static files
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Handle API requests
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleAPIRequest(request));
        return;
    }
    
    // Handle static files
    if (STATIC_FILES.some(file => url.pathname === file) || 
        url.pathname.startsWith('/static/')) {
        event.respondWith(handleStaticRequest(request));
        return;
    }
    
    // Handle other requests
    event.respondWith(handleOtherRequest(request));
});

// Handle API requests with network-first strategy
async function handleAPIRequest(request) {
    const url = new URL(request.url);
    
    try {
        // Try network first
        const networkResponse = await fetch(request);
        
        // Cache successful API responses
        if (networkResponse.ok && shouldCacheAPI(url.pathname)) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        // Network failed, try cache
        console.log('Network failed for API request, trying cache:', url.pathname);
        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log('Returning cached API response:', url.pathname);
            return cachedResponse;
        }
        
        // Return offline response for critical endpoints
        if (url.pathname === '/api/stats') {
            return new Response(JSON.stringify({
                totalMembers: 0,
                totalDirectors: 0,
                totalDivisions: 8,
                systemStatus: 'Offline'
            }), {
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Return generic offline response
        return new Response(JSON.stringify({
            error: 'Offline - Network unavailable',
            offline: true
        }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Handle static files with cache-first strategy
async function handleStaticRequest(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Not in cache, try network
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Failed to fetch static resource:', request.url);
        
        // Return fallback for main page
        if (request.url.endsWith('/') || request.url.includes('index.html')) {
            const cache = await caches.open(STATIC_CACHE);
            return cache.match('/');
        }
        
        throw error;
    }
}

// Handle other requests
async function handleOtherRequest(request) {
    try {
        return await fetch(request);
    } catch (error) {
        // For navigation requests, return the main page
        if (request.mode === 'navigate') {
            const cache = await caches.open(STATIC_CACHE);
            return cache.match('/');
        }
        
        throw error;
    }
}

// Check if API endpoint should be cached
function shouldCacheAPI(pathname) {
    return API_CACHE_PATTERNS.some(pattern => pattern.test(pathname));
}

// Handle background sync for offline actions
self.addEventListener('sync', event => {
    console.log('Background sync triggered:', event.tag);
    
    if (event.tag === 'jkwi-offline-sync') {
        event.waitUntil(syncOfflineData());
    }
});

// Sync offline data when connection is restored
async function syncOfflineData() {
    try {
        // Get offline queue from IndexedDB or localStorage
        const offlineQueue = await getOfflineQueue();
        
        for (const item of offlineQueue) {
            try {
                await fetch(item.url, {
                    method: item.method,
                    headers: item.headers,
                    body: item.body
                });
                
                // Remove successfully synced item
                await removeFromOfflineQueue(item.id);
            } catch (error) {
                console.error('Failed to sync offline item:', error);
            }
        }
        
        // Notify all clients that sync is complete
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'SYNC_COMPLETE',
                synced: offlineQueue.length
            });
        });
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

// Helper functions for offline queue management
async function getOfflineQueue() {
    // In a real implementation, this would use IndexedDB
    // For now, we'll return an empty array
    return [];
}

async function removeFromOfflineQueue(id) {
    // Remove item from IndexedDB
    console.log('Removing synced item:', id);
}

// Handle push notifications
self.addEventListener('push', event => {
    console.log('Push notification received');
    
    if (!event.data) {
        return;
    }
    
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/static/icon-192x192.png',
        badge: '/static/badge-72x72.png',
        vibrate: [200, 100, 200],
        data: data.data || {},
        actions: data.actions || []
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    console.log('Notification clicked');
    
    event.notification.close();
    
    const targetUrl = event.notification.data.url || '/';
    
    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        }).then(clientList => {
            // Check if there's already a window open
            for (const client of clientList) {
                if (client.url === targetUrl && 'focus' in client) {
                    return client.focus();
                }
            }
            
            // Open new window
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});

// Log service worker events
self.addEventListener('message', event => {
    console.log('Service Worker received message:', event.data);
    
    if (event.data && event.data.type) {
        switch (event.data.type) {
            case 'SKIP_WAITING':
                self.skipWaiting();
                break;
            case 'GET_VERSION':
                event.ports[0].postMessage({
                    version: CACHE_NAME
                });
                break;
        }
    }
});

console.log('JKWI Service Worker loaded successfully');
