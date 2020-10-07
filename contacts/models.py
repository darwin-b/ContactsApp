from django.db import models


# Create your models here.


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=15)
    lname = models.CharField(max_length=30)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=15)
    Address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zip = models.IntegerField(max_length=9)


class Phone(models.Model):
    phone_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=15)
    area_code = models.IntegerField(max_length=3)
    number = models.IntegerField(max_length=10)


class Date(models.Model):
    date_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date_type = models.CharField(max_length=25)
    date = models.DateField()
