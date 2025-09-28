from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.account.urls')),
    path('', include('apps.leads.urls')),
    path('', include('apps.clients.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('api/', include('apps.api.urls')),
]

# Health check endpoint
urlpatterns += [
    path('health/', lambda request: HttpResponse('OK')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Debug toolbar
    try:
        import debug_toolbar

        urlpatterns = [
                          path('__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
    except ImportError:
        pass