from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['fname'] = "First name should be at least 2 characters!"
        elif len(postData['lname']) < 2:
            errors['lname'] = "Last name should be at least 2 characters!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_address'] = "Invalid email address!"
        elif len(postData['phone']) != 10:
            errors['phone'] = "Invalid phone number!"
        elif len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters!"
        elif postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Confirm password doesn't match. Please confirm!" 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    # 1st user is system admin - can create internal users to edit/add features in page.
    # internal or external user has different access to features
    # 1-admin 2-employee 3-customer
    user_type = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def fullname(self):
        return f'{self.first_name} {self.last_name}'
