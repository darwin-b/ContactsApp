from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .form import *
from .models import Contact,Address,Phone,Date

# Create your views here.


def add_contact(request):
    context = {}
    # context['Cf_Contact']= Cf_Contact()
    # context['Cf_Address'] = Cf_Address()
    # context['Cf_Phone'] = Cf_Phone()
    # context['Cf_Date'] = Cf_Date()

    context["form"] = ContactForm()
    # return render(request, "home.html", context)

    if request.method=='POST':
        print("hi")
        contact_id=-1
        if request.POST.get('fname'):
            save_contact  = Contact()
            save_contact.fname=request.POST.get('fname')
            save_contact.mname = request.POST.get('mname')
            save_contact.lname = request.POST.get('lname')
            save_contact.save()
            contact_id=save_contact.id

            if request.POST.get('address_type') and contact_id!=-1:
                print("contact id : ",contact_id)
                save_address = Address()
                save_address.contact_id=save_contact
                save_address.address_type = request.POST.get('address_type')
                save_address.address = request.POST.get('address',"")
                save_address.city = request.POST.get('city',"")
                save_address.state = request.POST.get('state',"")
                save_address.zip = request.POST.get('zip',None)
                save_address.save()

            if request.POST.get('phone_type')and contact_id!=-1:
                save_phone = Phone()
                save_phone.contact_id=save_contact
                save_phone.phone_type = request.POST.get('phone_type')
                save_phone.area_code = request.POST.get('area_code',None)
                if request.POST.get('number'):
                    save_phone.number = None
                else:
                    save_phone.number = request.POST.get('number',None)
                save_phone.save()

            save_date = Date()
            if request.POST.get('date_type')and contact_id!=-1:
                save_date.contact_id=save_contact
                save_date.date_type = request.POST.get('date_type')
                save_date.date = request.POST.get('date',None)
                save_date.save()
        return render(request,'add_contact.html',context)
    else:
        return render(request, 'add_contact.html', context)

