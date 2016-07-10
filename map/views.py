from django.shortcuts import render, get_object_or_404
from models import Room
from django.views.generic import TemplateView, DetailView


class MapView(TemplateView):
    model = Room
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        rooms = Room.objects.all()
        room1, room2, room3, room4 = rooms[0], rooms[1], rooms[2], rooms[3]

        return {'room1': room1, 'room2': room2,
             'room3': room3, 'room4': room4}


class RoomView(DetailView):
    template_name = 'detail.html'
    model = Room
    context_object_name = "room"

    def get_object(self):
        object = super(RoomView, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object
