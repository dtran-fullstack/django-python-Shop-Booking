from django.db import models
from login_app.models import *
import datetime

class EventManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if postData['date'] < str(datetime.date.today()):
            errors['date'] = "Invalid Date! Appointment can't be in the past!"
        return errors

class Event(models.Model):
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    customers = models.ManyToManyField(User, related_name="book_events")
    employees = models.ManyToManyField(User, related_name="has_events")
    # 1-confirmed | 2-declined | 3-pending | 9-completed
    status = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()