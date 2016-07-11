from django import forms

from models import Room, Worker


class RoomUpdateForm(forms.ModelForm):

    class  Meta:
        model = Room
        fields = ["room_name", "emp_number", "image"] 

class WorkerUpdateForm(forms.ModelForm):

    class  Meta:
        model = Worker
        fields = ["first_name", "last_name", "email", "work_room"] 