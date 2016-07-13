from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.test.client import RequestFactory
from django.test import Client
from django.contrib.auth.models import User

import random
import string
import factory

from views import MapView
from models import Room, Worker

def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))

class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = Room

    room_name = "Frontend"

    emp_number = 3

class WorkerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Worker

    first_name = "Benni"

    last_name = "Benassi"

    email = "benni@mail.ru"

    work_room = factory.SubFactory(RoomFactory)

class MapPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
    def test_map_page_view(self):
        '''
        Check view response code and template
        '''
        request = self.factory.get(reverse('map'))
        response = MapView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        #test template
        # self.client.login('admin', 'admin')
        response = self.client.get(reverse('map'))
        self.assertTemplateUsed(response, 'map.html')

    def test_context(self):
        '''
        Check context data
        '''
        # check if rooms apper in context
        room1 = RoomFactory.create()
        response = self.client.get(reverse('map'))
        room_context = response.context['room1']
        self.assertEqual(room_context, room1)

        room2 = RoomFactory.create()
        response = self.client.get(reverse('map'))
        room_context = response.context['room2']
        self.assertEqual(room_context, room2)

        room3 = RoomFactory.create()
        response = self.client.get(reverse('map'))
        room_context = response.context['room3']
        self.assertEqual(room_context, room3)

        room4 = RoomFactory.create()
        response = self.client.get(reverse('map'))
        room_context = response.context['room4']
        self.assertEqual(room_context, room4)

        #check status code if there is excessive room
        room5 = RoomFactory.create()
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)

class DetailPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()       
        self.test_user = User.objects.create_user("admin", "admin@admin", "admin")
        login = self.client.login(username="admin", password="admin")
        self.assertEqual(login, True)

    def test_detail_page_view(self):
        '''
        Check view response code and template
        '''
        request = self.factory.get(reverse('room_detail', kwargs = {'pk':1}))
        response = MapView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        #check room instance in context
        room1 = RoomFactory.create()
        response = self.client.get(reverse('room_detail', kwargs = {'pk':1}))
        room_context = response.context['room']
        self.assertEqual(room_context, room1)

        #check worker instance in context if he is in the room with id=1
        worker1 = WorkerFactory.create(work_room=room1)
        response = self.client.get(reverse('room_detail', kwargs = {'pk':1}))
        worker_context = response.context['workers']
        self.assertEqual(worker_context.first(), worker1)

        #check worker is absent if his room does not mutch with ours
        worker1 = WorkerFactory.create()
        response = self.client.get(reverse('room_detail', kwargs = {'pk':1}))
        worker_context = response.context['workers']
        self.assertNotEqual(worker_context.first(), worker1)


