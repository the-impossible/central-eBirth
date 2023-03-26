from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('eBirth_basic.urls', namespace='basic')),
    path('auth/', include('eBirth_auth.urls', namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Central E-Birth Registration and Certificate Issuing System"
admin.site.site_title = "Central E-Birth Registration and Certificate Issuing System"
admin.site.index_title = "Welcome to Central E-Birth Registration and Certificate Issuing System"