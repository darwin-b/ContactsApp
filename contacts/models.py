from django.db import models


# Create your models here.

class Contact(models.Model):
    # contact_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=15,null=True)
    lname = models.CharField(max_length=30,null=True)

    class Meta:
        db_table = u"Contact"


class Address(models.Model):
    # address_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE,db_column="contact_id")
    address_type = models.CharField(max_length=15,null=True)
    address = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=25,null=True)
    state = models.CharField(max_length=25,null=True)
    zip = models.IntegerField(null=True)

    class Meta:

        db_table = u"Address"

class Phone(models.Model):
    # phone_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE,db_column="contact_id")
    phone_type = models.CharField(max_length=15,null=True)
    area_code = models.IntegerField(null=True)
    number = models.IntegerField(null=True)

    class Meta:
        db_table = u"Phone"

class Date(models.Model):
    # date_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE,db_column="contact_id")
    date_type = models.CharField(max_length=25,null=True)
    date = models.DateField(null=True)

    class Meta:
        db_table = u"Date"