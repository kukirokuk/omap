"""omap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from map.views import MapView, RoomView, RoomUpdate, RoomDelete, RoomCreate

urlpatterns = [
    url(r'^$', MapView.as_view(), name="map"),
    url(r'^room/detail/(?P<pk>\d+)$', RoomView.as_view(), name='detail'),
    url(r'^room/create/(?P<pk>\d+)$', RoomCreate.as_view(), name='room_create'),
    url(r'^room/update/(?P<pk>\d+)$', RoomUpdate.as_view(), name='update'),
    url(r'^room/delete/(?P<pk>\d+)$', RoomDelete.as_view(), name='room_delete'),


    url(r'^admin/', admin.site.urls),
]
