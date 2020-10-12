from django import forms
from .models import Contact
from .models import Address
from .models import Phone
from .models import Date


class ContactForm(forms.Form):
    fname = forms.CharField(max_length=30,label="First Name")
    mname = forms.CharField(max_length=15,required=False,label="Middle Name")
    lname = forms.CharField(max_length=30,required=False,label="Last Name")

    address_type = forms.CharField(max_length=15,required=False,label="Address Type")
    address = forms.CharField(max_length=50,required=False,label="Address")
    city = forms.CharField(max_length=25,required=False,label="City")
    state = forms.CharField(max_length=25,required=False,label="State")
    zip = forms.IntegerField(required=False,label="Zip")

    phone_type = forms.CharField(max_length=15,required=False,label="Phone Type")
    area_code = forms.IntegerField(required=False,label="Area Code")
    number = forms.IntegerField(required=False,label="Numer")

    date_type = forms.CharField(max_length=25,required=False,label="Date Type")
    date = forms.DateField(required=False,label="Date")


class Search(forms.Form):
    search_word = forms.CharField(max_length=25,required=True,label="Search")


class UppdateForm(forms.Form):

    # contact_id = forms.IntegerField(required=False, label="Contact_id",disabled=False)
    fname = forms.CharField(max_length=30, label="First Name")
    mname = forms.CharField(max_length=15, required=False, label="Middle Name")
    lname = forms.CharField(max_length=30, required=False, label="Last Name")

    address_type = forms.CharField(max_length=15, required=False, label="Address Type")
    address = forms.CharField(max_length=50, required=False, label="Address")
    city = forms.CharField(max_length=25, required=False, label="City")
    state = forms.CharField(max_length=25, required=False, label="State")
    zip = forms.IntegerField(required=False, label="Zip")

    phone_type = forms.CharField(max_length=15, required=False, label="Phone Type")
    area_code = forms.IntegerField(required=False, label="Area Code")
    number = forms.IntegerField(required=False, label="Numer")

    date_type = forms.CharField(max_length=25, required=False, label="Date Type")
    date = forms.DateField(required=False, label="Date")