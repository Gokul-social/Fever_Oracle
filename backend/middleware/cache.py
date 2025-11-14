"""
Simple caching middleware for API responses
"""

from functools import wraps
from datetime import datetime, timedelta
from typing import Dict, Any

# Simple in-memory cache (in production, use Redis)
_response_cache: Dict[str, Dict[str, Any]] = {}

def cache_response(seconds: int = 60):
    """Cache API response for specified seconds"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            if cache_key in _response_cache:
                cached = _response_cache[cache_key]
                if datetime.now() < cached['expires']:
                    return cached['response']
                else:
                    # Expired, remove from cache
                    del _response_cache[cache_key]
            
            # Call function and cache result
            response = f(*args, **kwargs)
            _response_cache[cache_key] = {
                'response': response,
                'expires': datetime.now() + timedelta(seconds=seconds)
            }
            
            # Clean up old cache entries (keep cache size manageable)
            if len(_response_cache) > 100:
                now = datetime.now()
                expired_keys = [
                    k for k, v in _response_cache.items()
                    if now >= v['expires']
                ]
                for k in expired_keys:
                    del _response_cache[k]
            
            return response
        return decorated_function
    return decorator

def clear_cache():
    """Clear all cached responses"""
    _response_cache.clear()

