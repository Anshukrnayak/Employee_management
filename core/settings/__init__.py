import os

# Determine which settings to use based on environment
environment = os.getenv('DJANGO_SETTINGS_MODULE', '')

if 'production' in environment:
    from .production import *
else:
    # Default to base settings
    from .base import *