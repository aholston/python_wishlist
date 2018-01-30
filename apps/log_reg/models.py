from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REG = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')

# Create your models here.
class UserManager(models.Manager):
    def validate(self, data):
        errors = {}
        if len(data['name']) < 3:
            errors['name'] = 'Name should be atleast 3 characters'
        if len(data['username']) < 3:
            errors['username'] = 'Username should be atleast three characters'
        if not EMAIL_REG.match(data['email']):
            errors['email'] = 'Please enter a valid email address'
        if User.objects.filter(email=data['email']):
            errors['email_use'] = 'Email already in use!'
        if data['password'] != data['pw_conf']:
            errors['password'] = 'Passwords do not match'
        if len(data['password']) < 8:
            errors['pw_length'] = 'Password should be atleast 8 characters'
        return errors

class ItemManager(models.Manager):
    def validate(self, data):
        errors = {}
        if len(data['item']) < 4:
            errors['item'] = 'Item name should be atleast four characters!'
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name='my_item')
    wished_by = models.ManyToManyField(User, related_name='wishlist')

    objects = ItemManager()
