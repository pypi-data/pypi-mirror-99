"""Caching functions for the Github Auth module."""

import hashlib
import pickle  # noqa: S403
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, TypeVar

from cachetools import TTLCache
from dogpile.cache import CacheRegion, make_region, register_backend
from dogpile.cache.api import NO_VALUE, BackendFormatted, BackendSetType, CacheBackend, CachedValue
from dogpile.cache.util import compat

R = TypeVar('R')


def get_cache_region():
    return make_region(function_key_generator=cache_key_generator)


# This is a copy of the default key generator from dogpile, but
# with additional hashing to avoid using sensitive values as cache keys
def cache_key_generator(namespace: Optional[str], fn: Callable[..., Any], to_str: Callable[[object], str] = str):
    if namespace is None:
        namespace = f'{fn.__module__}:{fn.__name__}'  # noqa: WPS609 - direct magic attribute usage
    else:
        namespace = f'{fn.__module__}:{fn.__name__}|{namespace}'  # noqa: WPS609 - direct magic attribute usage

    # Remove the `self` argument, since it'll always change
    fn_args = compat.inspect_getargspec(fn)
    has_self = fn_args[0] and (fn_args[0][0] in {'self', 'cls'})  # type: ignore

    def generate_key(*args: object, **kw: object) -> str:
        if kw:
            raise ValueError('The dogpile.cache default key creation function does not accept keyword arguments.')
        if has_self:
            args = args[1:]

        # Encode the args since they may be sensitive
        arg_key = hashlib.sha224(''.join(map(to_str, args)).encode('utf-8')).hexdigest()
        return f'{namespace}|{arg_key}'

    return generate_key


_default_cache_backend = 'memory'
# Expiration is dogpile's expiration TTL
_default_expiration = 300

_default_cache_size = 100

# The Cache TTL is the underlying backend TTL, which should
# be greater than dogpile's
# https://dogpilecache.sqlalchemy.org/en/latest/api.html#memcached-backends
_default_cache_ttl = _default_expiration * 1.5  # noqa: WPS432

# This gives us shortcuts to the actual modules
_backend_map = {
    _default_cache_backend: _default_cache_backend,
    'memcache': 'dogpile.cache.memcached',
}

# Default settings
_default_backend_args = {
    'memory': {'maxsize': _default_cache_size, 'ttl': _default_cache_ttl},
    'memcache': {'url': '127.0.0.1', 'distributed_lock': True},
}


def configure_cache_region(cache_region: CacheRegion, settings: Dict[str, Any], prefix: str):
    backend_key = f'{prefix}.backend'
    expiration_key = f'{prefix}.expiration'

    # Determine the backend
    backend = settings.get(backend_key, _default_cache_backend)
    expiration = int(settings.get(expiration_key, _default_expiration))

    # Find all the args that make sense for the backend
    backend_arg_prefix = f'{prefix}.{backend}.'
    backend_args = {
        k[len(backend_arg_prefix) :]: v for k, v in settings.items() if k.startswith(backend_arg_prefix)  # noqa: E203
    }

    resolved_args = {**_default_backend_args[backend], **backend_args}

    # Configure the cache region
    cache_region.configure(
        _backend_map[backend], expiration_time=expiration, arguments=resolved_args, replace_existing_backend=True,
    )


if TYPE_CHECKING:  # pragma: no cover
    StringIndexedTTLCache = TTLCache[str, CachedValue]
else:
    StringIndexedTTLCache = TTLCache


class TTLBackend(CacheBackend):
    _cache_path = 'cache_path'
    cache: StringIndexedTTLCache
    persisted_cache_path: Optional[str]

    def __init__(self, arguments: Dict[str, Any]):
        p_cache_path = arguments.pop(self._cache_path, None)

        if isinstance(p_cache_path, str):
            self.persisted_cache_path = p_cache_path
        else:
            self.persisted_cache_path = None

        # A potentially persisted cache for all items to keep in cache
        self.cache = TTLCache(**arguments)

        if self.persisted_cache_path:
            Path(self.persisted_cache_path).parent.mkdir(parents=True, exist_ok=True)

            try:
                # If we find a cache file and no argument was modified, then we retrieve the cache in file
                with open(self.persisted_cache_path, 'rb') as f:
                    pickled_cache = pickle.load(f)  # noqa: S301 - pickle usage
                    if all(getattr(self.cache, arg_key) == getattr(pickled_cache, arg_key) for arg_key in arguments.keys()):
                        self.cache = pickled_cache  # noqa: WPS220 - deep nesting

            except (FileNotFoundError, EOFError):
                pass

    def get(self, key: str) -> BackendFormatted:
        val = self.cache.get(key, NO_VALUE)
        if isinstance(val, NO_VALUE.__class__):
            return val
        return val

    def set(self, key: str, value: BackendSetType) -> None:  # noqa: WPS125, A003
        if not isinstance(value, CachedValue):  # pragma: no cover
            value = CachedValue(value, {})

        self.cache[key] = value
        if self.persisted_cache_path:
            self.persist_cache()

    def delete(self, key: str) -> None:
        sentinel = object()
        if self.cache.pop(key, sentinel) is not sentinel and self.persisted_cache_path:
            self.persist_cache()

    def persist_cache(self) -> None:
        assert self.persisted_cache_path
        with open(self.persisted_cache_path, 'wb') as f:
            pickle.dump(self.cache, f)


register_backend(_default_cache_backend, __name__, TTLBackend.__name__)
