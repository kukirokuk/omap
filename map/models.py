from django.db import models
from django_resized import ResizedImageField


class Room(models.Model):
    """Room Model"""

    class Meta(object):
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    room_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Room name")

    emp_number = models.CharField(
        max_length=256,
        blank= True,
        verbose_name=u"Count of places")

    image = ResizedImageField(size=[800, 600], upload_to='photo/', blank=True,
                              null=True)

    def __unicode__(self):

            return u"%s" % (self.room_name)

class Worker(models.Model):
    """Worker model"""

    class Meta(object):
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = ['first_name']

    first_name = models.CharField(
        max_length=30, 
        blank=False)

    last_name = models.CharField(
        max_length=30, 
        blank=False)

    email = models.EmailField(
        max_length=30,
        blank=False)

    work_room = models.ForeignKey('Room',
        blank=False,
        null=False,
        on_delete=models.PROTECT)

    def __unicode__(self):
        return "%s %s, %s" %(self.first_name, self.last_name, 
            self.work_room.room_name)