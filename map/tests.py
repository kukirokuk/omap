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
from forms import RoomUpdateForm, WorkerUpdateForm


class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = Room

    room_name = "Frontend"

    emp_number = 2

class WorkerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Worker

    first_name = "Nihls"

    last_name = "Frahm"

    email = "frahm@ukr.net"

    work_room = factory.SubFactory(RoomFactory)

class MapPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.url = reverse('map')
        
    def test_map_page_view(self):
        '''
        Check view response code and template
        '''
        request = self.factory.get(self.url)
        response = MapView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        #test template
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'map.html')

    def test_context(self):
        '''
        Check context data
        '''
        # check if rooms apper in context
        room1 = RoomFactory.create()
        response = self.client.get(self.url)
        room_context = response.context['room1']
        self.assertEqual(room_context, room1)

        room2 = RoomFactory.create()
        response = self.client.get(self.url)
        room_context = response.context['room2']
        self.assertEqual(room_context, room2)

        room3 = RoomFactory.create()
        response = self.client.get(self.url)
        room_context = response.context['room3']
        self.assertEqual(room_context, room3)

        room4 = RoomFactory.create()
        response = self.client.get(self.url)
        room_context = response.context['room4']
        self.assertEqual(room_context, room4)

        #check status code if there is excessive room
        room5 = RoomFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class DetailPageTest(TestCase):
    def setUp(self):
        self.url = reverse('room_detail', kwargs = {'pk':1})
        self.client = Client()
        self.factory = RequestFactory()       
        self.test_user = User.objects.create_user("admin", "admin@admin", "admin")
        login = self.client.login(username="admin", password="admin")
        self.assertEqual(login, True)

    def test_detail_page_view_and_context(self):
        '''
        Check view response code and template
        '''
        request = self.factory.get(self.url)
        response = MapView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        #check room instance in context
        room1 = RoomFactory.create()
        response = self.client.get(self.url)
        room_context = response.context['room']
        self.assertEqual(room_context, room1)

        #check worker instance in context if he is in the room with id=1
        worker1 = WorkerFactory.create(work_room=room1)
        response = self.client.get(self.url)
        worker_context = response.context['workers']
        self.assertEqual(worker_context.first(), worker1)

        #check worker is absent if his room does not mutch with ours
        worker1 = WorkerFactory.create()
        response = self.client.get(self.url)
        worker_context = response.context['workers']
        self.assertNotEqual(worker_context.first(), worker1)


    def test_fields_renders(self):
        '''
        Check all fields renders
        '''
        #room model fields
        room1 = RoomFactory.create()
        response = self.client.get(self.url)
        self.assertIn(room1.room_name, response.content)
        self.assertIn(str(room1.emp_number), response.content)

        #worker model fields
        worker1 = WorkerFactory.create(work_room=room1)
        response = self.client.get(self.url)
        self.assertIn(worker1.first_name, response.content)
        self.assertIn(worker1.last_name, response.content)
        self.assertIn(worker1.email, response.content)

        #test multiple worker db instances appear at the detail page
        worker2 = WorkerFactory.create(work_room=room1)
        response = self.client.get(self.url)
        self.assertIn(worker2.first_name, response.content)
        self.assertIn(worker2.last_name, response.content)
        self.assertIn(worker2.email, response.content)

    def test_auth(self):
        '''
        Check authentication works properly
        '''
        response = self.client.logout()
        room1 = RoomFactory.create()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter your login and password', response.content)


class RoomCreateEditDeletePageTest(TestCase):
    def setUp(self):
        self.create_url =reverse('room_create', kwargs = {'pk':1})
        self.update_url =reverse('room_update', kwargs = {'pk':1})
        self.delete_url =reverse('room_delete', kwargs = {'pk':1})        
        self.client = Client()
        self.factory = RequestFactory()       
        self.test_user = User.objects.create_user("admin", "admin@admin", "admin")
        login = self.client.login(username="admin", password="admin")
        self.assertEqual(login, True)
        self.data1 = {
            'room_name': 'Newroom1',
            'emp_number': 12}
        self.data2 = {
            'room_name': 'Newroom2',
            'emp_number': 13}

    def test_form_fields(self):
        '''
        Check room edit form fields renders
        '''
        #create form
        room = RoomFactory.create()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="room_name"', response.content)
        self.assertIn('name="emp_number"', response.content)
        self.assertIn('name="image"', response.content)

        #update form
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        '''
        Check form saves data
        '''
        #test create form
        response = self.client.post(self.create_url, self.data1)
        post_room = Room.objects.all().first()
        self.assertEqual(post_room.room_name, self.data1['room_name'])

        #test update form
        response = self.client.post(self.update_url, self.data2)
        post_room = Room.objects.all().first()
        self.assertEqual(post_room.room_name, self.data2['room_name'])

    def test_form_validation(self):
        '''
        Check form validation works properly
        '''
        #test form validation
        form = RoomUpdateForm(self.data1)
        self.assertTrue(form.is_valid())

        form = RoomUpdateForm({"room_name": "Room"})
        self.assertFalse(form.is_valid())

    def test_delete_worker(self):
        '''
        Check we can delete room
        '''
        #check status code of confirm delete page
        room = RoomFactory.create()
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

        #check do we delete right person
        self.assertIn("Do you want to delete %s ?" %room.room_name,response.content)

        #check we can delete room object
        response = self.client.post(self.delete_url)
        self.assertFalse(Room.objects.all())

        #check we can delete room objects if there are workers attached
        room = RoomFactory.create()
        worker = WorkerFactory.create(work_room=room)
        response = self.client.post(self.delete_url)
        self.assertTrue(Room.objects.all())


class WorkerCreateEditDeletePageTest(TestCase):
    def setUp(self):
        self.create_url = reverse('worker_create')
        self.update_url = reverse('worker_update', kwargs = {'pk':1})
        self.delete_url = reverse('worker_delete', kwargs = {'pk':1})
        self.client = Client()
        self.factory = RequestFactory()       
        self.test_user = User.objects.create_user("admin", "admin@admin", "admin")
        login = self.client.login(username="admin", password="admin")
        self.assertEqual(login, True)
        self.room = RoomFactory.create(room_name="New_room")
        self.data1 = {
            'first_name': 'Peter',
            'last_name': 'Falk',
            'email': 'peter@gmail.com',
            'work_room': self.room.id}
        self.data2 = {
            'first_name': 'Oleksandr',
            'last_name': 'Vinnichuk',
            'email': 'sasha@gmail.com',
            'work_room': self.room.id}

    def test_form_fields(self):
        '''
        Check worker edit form fields renders
        '''
        #create form
        worker = WorkerFactory.create()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="first_name"', response.content)
        self.assertIn('name="last_name"', response.content)
        self.assertIn('name="email"', response.content)
        self.assertIn('name="work_room"', response.content)

        #update form
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        '''
        Check form saves data
        '''
        #test create form
        response = self.client.post(self.create_url, self.data1)
        post_worker = Worker.objects.all().first()
        self.assertEqual(post_worker.first_name, self.data1['first_name'])

        # #test update form
        response = self.client.post(self.update_url, self.data2)
        post_worker = Worker.objects.all().first()
        self.assertEqual(post_worker.first_name, self.data2['first_name'])

    def test_form_validation(self):
        '''
        Check form validation works properly
        '''
        #test form validation
        form = WorkerUpdateForm(self.data1)
        self.assertTrue(form.is_valid())

        form = WorkerUpdateForm({"first_name": "Terence"})
        self.assertFalse(form.is_valid())

    def test_maximum_workers_number_reached(self):
        '''
        Check maximum workers protection 
        '''
        #create 3 workers when room factory default max number is 2
        worker = WorkerFactory.create(work_room=self.room)
        response = self.client.post(self.create_url, self.data1)
        response = self.client.post(self.create_url, self.data2)
        self.assertContains(response, 'Maximum workers reached')

    def test_delete_worker(self):
        '''
        Check we can delete worker
        '''
        #check status code of confirm delete page
        worker = WorkerFactory.create(work_room=self.room)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        #check do we delete right person
        self.assertIn("Do you want to delete %s %s?" %(worker.first_name, 
            worker.last_name),response.content)

        #check we can delete worker object
        response = self.client.post(self.delete_url)
        self.assertFalse(Worker.objects.all())