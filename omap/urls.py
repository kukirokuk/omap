from django.conf.urls import url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from map.views import MapView, RoomView, RoomUpdate, RoomDelete, RoomCreate

urlpatterns = [
    url(r'^$', MapView.as_view(), name="map"),
    url(r'^room/detail/(?P<pk>\d+)$', RoomView.as_view(), name='detail'),
    url(r'^room/create/(?P<pk>\d+)$', RoomCreate.as_view(), name='room_create'),
    url(r'^room/update/(?P<pk>\d+)$', RoomUpdate.as_view(), name='update'),
    url(r'^room/delete/(?P<pk>\d+)$', RoomDelete.as_view(), name='room_delete'),


    url(r'^admin/', admin.site.urls),
]

# urlpatterns += staticfiles_urlpatterns()

from .settings import MEDIA_ROOT, DEBUG


if DEBUG:
# serve files from media folder
        urlpatterns += patterns('',
                url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': MEDIA_ROOT}))