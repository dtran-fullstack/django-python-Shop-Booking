from django.db import models
from login_app.models import *


class ActivityManager(models.Manager):
    def validator(self,postData):
        errors = {}
        if postData['services'] == "":
            errors['services'] = "Can't be empty!"
        if postData['amount'] == 0:
            errors['amount'] = "Can't be empty!"
        if postData['tip'] < 0:
            errors['tip'] = "Invalid!"
        return errors

class ServiceManager(models.Manager):
    def validator(self,postData):
        errors = {}
        return errors

class PostManager(models.Manager):
    def validator(self,postData):
        errors = {}
        # if postData['photo'] == None:
        #     errors['photo'] == "Invalid! Missing the file."
        return errors

class Activity(models.Model):
    amount = models.FloatField(default=0.00)
    tip = models.FloatField(default=0.00)
    employee = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActivityManager()

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ServiceManager()

class Post(models.Model):
    image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    employee = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()