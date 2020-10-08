from django import forms
from .models import Contact
from .models import Address
from .models import Phone
from .models import Date


class Cf_Contact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['fname', 'mname', 'lname']
        labels = {'fname': 'First Name',
                  'mname': 'Middle Name',
                  'lname': 'Last Name',
                  }



class Cf_Address(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address', 'city', 'state', 'zip']
        labels = {'address_type': 'Address Type',
                  'address': 'Address',
                  'city': 'City',
                  'state': 'State',
                  'zip': 'Zip'}
        # help_texts = {'address_type': 'Eg: Home, Work.....'}


class Cf_Phone(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone_type', 'number', 'area_code']
        labels = {'phone_type': 'Phone Type',
                  'number': 'Number',
                  'area_code': 'Area Code',
                  }
        # help_texts = {'address_type': 'Eg: Home, Work.....'}


class Cf_Date(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['date_type', 'date']
        labels = {'date_type': 'Date Type',
                  'date': 'Date'
                  }
        # help_texts = {'address_type': 'Eg: Home, Work.....'}

class ContactForm(forms.Form):
    fname = forms.CharField(max_length=30,label="First Name")
    mname = forms.CharField(max_length=15,required=False,label="Middle Name")
    lname = forms.CharField(max_length=30,required=False,label="Last Name")

    address_type = forms.CharField(max_length=15,required=False,label="Address Type")
    Address = forms.CharField(max_length=50,required=False,label="Address")
    city = forms.CharField(max_length=25,required=False,label="City")
    state = forms.CharField(max_length=25,required=False,label="State")
    zip = forms.IntegerField(required=False,label="Zip")

    phone_type = forms.CharField(max_length=15,required=False,label="Phone Type")
    area_code = forms.IntegerField(required=False,label="Area Code")
    number = forms.IntegerField(required=False,label="Numer")

    date_type = forms.CharField(max_length=25,required=False,label="Date Type")
    date = forms.DateField(required=False,label="Date")

    # fields = ['fname','address_type', 'address', 'city', 'state', 'zip']
    # labels = {'fname' : 'First Name',
    #           'mname' : 'Middle Name',
    #           'lname' : 'Last Name',
    #
    #           'address_type': 'Address Type',
    #           'address': 'Address',
    #           'city': 'City',
    #           'state': 'State',
    #           'zip': 'Zip',
    #
    #           'phone_type' : 'Phone Type',
    #           'area_code': 'Area Code',
    #           'number': 'Number',
    #
    #           'date_type': 'Date Type',
    #           'Date' : 'Date'
    #           }

