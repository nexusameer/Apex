"""
Custom middleware for performance optimizations
"""
from django.utils.cache import add_never_cache_headers, patch_cache_control


class CacheControlMiddleware:
    """
    Add cache control headers for static and media files
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Cache static files for 1 year
        if request.path.startswith('/static/'):
            # Cache static files aggressively
            patch_cache_control(
                response,
                public=True,
                max_age=31536000,  # 1 year
                immutable=True
            )
        
        # Cache media files for 1 week
        elif request.path.startswith('/media/'):
            patch_cache_control(
                response,
                public=True,
                max_age=604800  # 1 week
            )
        
        # Don't cache HTML pages
        elif response.get('Content-Type', '').startswith('text/html'):
            add_never_cache_headers(response)
        
        return response


class SecurityHeadersMiddleware:
    """
    Add security headers for better performance and security
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Add referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
