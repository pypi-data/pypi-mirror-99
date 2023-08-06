###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import atexit

from .cache import (LruCacheMetaclass, strhash, methodcache, getTileCache,
                    isTileCacheSetup, CacheProperties)
try:
    from .memcache import MemCache
except ImportError:
    MemCache = None
from .cachefactory import CacheFactory, pickAvailableCache
from cachetools import cached, Cache, LRUCache


@atexit.register
def cachesClear(*args, **kwargs):
    """
    Clear the tilesource caches and the load model cache.  Note that this does
    not clear memcached (which could be done with tileCache._client.flush_all,
    but that can affect programs other than this one).
    """
    for name in LruCacheMetaclass.namedCaches:
        with LruCacheMetaclass.namedCaches[name][1]:
            LruCacheMetaclass.namedCaches[name][0].clear()
    if isTileCacheSetup():
        tileCache, tileLock = getTileCache()
        if isinstance(tileCache, LRUCache):
            try:
                with tileLock:
                    tileCache.clear()
            except Exception:
                pass


def cachesInfo(*args, **kwargs):
    """
    Report on each cache.

    :returns: a dictionary with the cache names as the keys and values that
        include 'maxsize' and 'used', if known.
    """
    info = {}
    for name in LruCacheMetaclass.namedCaches:
        with LruCacheMetaclass.namedCaches[name][1]:
            cache = LruCacheMetaclass.namedCaches[name][0]
            info[name] = {
                'maxsize': cache.maxsize,
                'used': cache.currsize
            }
    if isTileCacheSetup():
        tileCache, tileLock = getTileCache()
        if isinstance(tileCache, LRUCache):
            try:
                with tileLock:
                    info['tileCache'] = {
                        'maxsize': tileCache.maxsize,
                        'used': tileCache.currsize
                    }
            except Exception:
                pass
    # It would be nice to include memcached, but pylibmc's client.get_stats()
    # doesn't seem to work.
    return info


__all__ = ('CacheFactory', 'getTileCache', 'isTileCacheSetup', 'MemCache',
           'strhash', 'LruCacheMetaclass', 'pickAvailableCache', 'cached',
           'Cache', 'LRUCache', 'methodcache', 'CacheProperties')
