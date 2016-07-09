from django.shortcuts import render
from models import Room

# Create your views here.
def map(request):
    rooms = Room.objects.all()
    room1, room2, room3, room4 = rooms[0], rooms[1], rooms[2], rooms[3]

    return render(request, 'map.html', {'room1': room1, 'room2': room2,
         'room3': room3, 'room4': room4})