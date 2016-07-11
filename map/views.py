from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView, ListView
from django.core.urlresolvers import reverse

from models import Room, Worker
from forms import RoomUpdateForm, WorkerUpdateForm
from django.http import Http404

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

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['workers'] = Worker.objects.filter(work_room_id = self.kwargs['pk'])
        return context

class RoomCreate(CreateView):
    model = Room
    template_name = 'room_form.html'
    form_class = RoomUpdateForm

    def get_success_url(self):
        return '%s?status_message=Room created' % reverse('map')

    def form_valid(self, form):
        instance = form.save()
        instance.id = self.kwargs['pk']
        instance.save()
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

# Worker views

class WorkerView(DetailView):
    template_name = 'worker_detail.html'
    model = Worker
    context_object_name = "worker"

    def get_object(self):
        object = super(WorkerView, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object

class WorkerCreate(CreateView):
    model = Worker
    template_name = 'worker_form.html'
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return '%s?status_message=Worker created' % reverse('map')

    # def form_valid(self, form):
        # instance = form.save()
        # room = Room.objects.filter(pk=self.kwargs['pk'])[0]
        # print self.kwargs['pk']
        # instance.id = self.kwargs['pk']
        # instance.save()
        # return redirect(self.get_success_url())

class WorkerUpdate(UpdateView):
    model = Worker 
    template_name = 'worker_form.html'
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return '%s?status_message=Worker updated' % reverse('map')