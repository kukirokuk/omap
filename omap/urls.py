from django.conf.urls import url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.views.static import serve

from map.views import MapView, RoomView, RoomUpdate, RoomDelete, RoomCreate
from map.views import WorkerView, WorkerCreate, WorkerUpdate, WorkerDelete

urlpatterns = [
    url(r'^$', MapView.as_view(), name="map"),
    #room urls
    url(r'^detail/(?P<pk>\d+)$', login_required(RoomView.as_view()), name='room_detail'),
    url(r'^room/create/(?P<pk>\d+)$', RoomCreate.as_view(), name='room_create'),
    url(r'^room/update/(?P<pk>\d+)$', RoomUpdate.as_view(), name='room_update'),
    url(r'^room/delete/(?P<pk>\d+)$', RoomDelete.as_view(), name='room_delete'),

    #worker urls
    url(r'^worker/detail/(?P<pk>\d+)$', WorkerView.as_view(), name='worker_detail'),
    url(r'^worker/create/$', WorkerCreate.as_view(), name='worker_create'),
    url(r'^worker/update/(?P<pk>\d+)$', WorkerUpdate.as_view(), name='worker_update'),
    url(r'^worker/delete/(?P<pk>\d+)$', WorkerDelete.as_view(), name='worker_delete'),

    url(r'^accounts/login/$', login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', logout, {'next_page': '/?status_message=Succesfull logout'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]

from .settings import MEDIA_ROOT, DEBUG


if DEBUG:
# serve files from media folder
    urlpatterns += [
            url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})]