from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    publish_date = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    label = models.CharField(max_length=30)
    current_number = models.IntegerField()
    total_number = models.IntegerField()
    can_borrow = models.CharField(max_length=50)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    tele = models.CharField(max_length=50)
    book_number = models.IntegerField()


class Borrow(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=100)
    is_return = models.IntegerField()
    borrow_time = models.CharField(max_length=100)
    return_time = models.CharField(max_length=100)
