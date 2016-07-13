from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.test.client import RequestFactory

import random
import string
import factory

from views import MapView
from models import Room

def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))

class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = Room

    room_name = "Frontend"

    emp_number = 3

class MapPageTest(TestCase):
    '''
     Check our view for home page
    '''

    def setUp(self):
        self.factory = RequestFactory()
        
    def test_map_page_view(self):
        '''
        Check test view response code and template
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
