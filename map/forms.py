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

    def clean_work_room(self):
        x = self.cleaned_data.get('work_room')
        workers_in_room = Worker.objects.filter(work_room=x)
        workers_allowed = Room.objects.filter(room_name=x).first()
        if workers_in_room.count() >= int(workers_allowed.emp_number):
            raise forms.ValidationError("Maximum workers reached")
        return x