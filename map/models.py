
from django.db import models


class Room(models.Model):
    """Room Model"""

    class Meta(object):
        verbose_name = u"Rooms"
        verbose_name_plural = u"Room"

    room_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Room name")

    emp_number = models.CharField(
        max_length=256,
        blank= True,
        verbose_name=u"Count of places")

    def __unicode__(self):

            return u"%s" % (self.room_name)