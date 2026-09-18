from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # with this line up here, i am telling django i want to expose an endpoint(MEDIA_URL)
    # and any request that goes to that endpoint should be routed to the file system at the MEDIA_ROOT address

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
