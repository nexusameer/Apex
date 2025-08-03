# Add these optimizations to your Django settings.py

# ===============================
# PERFORMANCE OPTIMIZATIONS
# ===============================

# Static files compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Install: pip install whitenoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... your other middleware
]

# Cache control headers
WHITENOISE_MAX_AGE = 31536000  # 1 year for static files

# Database connection optimization
DATABASES = {
    'default': {
        # ... your database config
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Template caching (for production)
if not DEBUG:
    TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [(
                'django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            )],
        },
    }]

# Session optimization
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Security headers that also improve performance
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Gzip compression
USE_GZIP = True

# Static files optimization
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files optimization
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cache configuration (add this if you have Redis/Memcached)
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'mindrelief',
        'TIMEOUT': 300,
    }
}
"""

# Additional optimizations
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
USE_I18N = False  # Disable if not using internationalization
USE_L10N = False  # Disable if not using localization
