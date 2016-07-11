from django import forms

from models import Room


class RoomUpdateForm(forms.ModelForm):

    class  Meta:
        model = Room
        fields = ["room_name", "emp_number", "image"] 