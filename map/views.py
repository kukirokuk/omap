from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse

from models import Room
from forms import RoomUpdateForm

class MapView(TemplateView):
    model = Room
    template_name = "map.html"

    def get_context_data(self, *args, **kwargs):
        room1 = Room.objects.filter(pk=1).first()
        room2 = Room.objects.filter(pk=2).first()
        room3 = Room.objects.filter(pk=3).first()
        room4 = Room.objects.filter(pk=4).first()
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

class RoomCreate(CreateView):
    model = Room
    template_name = 'room_form.html'
    form_class = RoomUpdateForm

    def get_success_url(self):
        return '%s?status_message=Room created' % reverse('map')

    def form_valid(self, form):
        instance = form
        print self.kwargs['pk']
        instance.id = self.kwargs['pk']
        instance.save
        return redirect(self.get_success_url())

class RoomUpdate(UpdateView):
    model = Room 
    template_name = 'room_form.html'
    form_class = RoomUpdateForm

    def get_success_url(self):
        return '%s?status_message=Room updated' % reverse('detail', 
            kwargs={'pk': self.get_object().id})

class RoomDelete(DeleteView):
    model = Room
    template_name = 'delete.html'
    context_object_name = "room"

    def get_success_url(self):
        return '%s?status_message=Room deleted' % reverse('map')