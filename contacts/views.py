import csv
import traceback
import requests
import django.middleware as dm

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import render

from django.db.models import Q

from .form import *
from .models import Contact,Address,Phone,Date

# Create your views here.


def add_contact(request):
    context = {}
    context["form"] = ContactForm()

    if request.method=='POST':
        print("Adding Contact...........")
        contact_id=-1
        if request.POST.get('fname'):

            # Add to Contact table
            save_contact  = Contact()
            save_contact.fname=request.POST.get('fname')
            save_contact.mname = request.POST.get('mname')
            save_contact.lname = request.POST.get('lname')
            save_contact.save()
            contact_id=save_contact.id

            # Add to Address table
            save_address = Address()
            save_address.contact_id=save_contact
            save_address.address_type = request.POST.get('address_type',"")
            save_address.address = request.POST.get('address',"")
            save_address.city = request.POST.get('city',"")
            save_address.state = request.POST.get('state',"")
            if request.POST.get("zip",None)=="":
                save_address.zip = None
            else:
                save_address.zip =request.POST.get("zip",None)
            save_address.save()

            # Add to Phone table
            save_phone = Phone()
            save_phone.contact_id=save_contact
            save_phone.phone_type = request.POST.get('phone_type',"")
            if request.POST.get("area_code",None)=="":
                save_phone.area_code = None
            else:
                save_phone.area_code =request.POST.get("area_code",None)
            if request.POST.get("number",None)=="":
                save_phone.number = None
            else:
                save_phone.number =request.POST.get("number",None)
            save_phone.save()

            # Add to Date table
            save_date = Date()
            save_date.contact_id=save_contact
            save_date.date_type = request.POST.get('date_type',"")
            if request.POST.get("date",None)=="":
                save_date.date = None
            else:
                save_date.date =request.POST.get("date",None)
            save_date.save()

        messages.success(request,"Contact successfully added")
        return render(request,'add_contact.html',context)

    else:

        # add_csv(filepath)
        return render(request, 'add_contact.html', context)


def search(request):
    context={}

    context["contact_results"]=""
    context["address_results"] = ""
    context["phone_results"] = ""
    context["date_results"] = ""
    context["result_list"]=""

    if request.method=="POST":
        search_word = request.POST.get("search_word")

        context["contact_results"]= Contact.objects.filter(
                                        Q(fname__icontains=search_word)|
                                        Q(mname__icontains=search_word) |
                                        Q(lname__icontains=search_word)
                                    )

        context["address_results"]= Address.objects.filter(
                                        Q(address__icontains=search_word) |
                                        Q(city__icontains=search_word) |
                                        Q(state__icontains=search_word)|
                                        Q(zip__icontains=search_word)
                                    )

        context["phone_results"]= Phone.objects.filter(
                                        Q(area_code__icontains=search_word) |
                                        Q(number__icontains=search_word)
                                    )

        context["date_results"]= Date.objects.filter(
                                        Q(date__icontains=search_word)
                                    )

        contact_ids = []
        for result in context["contact_results"]:
            contact_ids.append(result.id)

        for result in context["address_results"]:
            contact_ids.append(result.contact_id.id)

        for result in context["phone_results"]:
            contact_ids.append(result.contact_id.id)

        for result in context["date_results"]:
            contact_ids.append(result.contact_id.id)

        context={}
        context["formSearch"] = Search()
        results={}

        for id in contact_ids:

            res=Contact.objects.get(pk=id)
            results[id]=[res.fname,res.mname,res.lname]

            try:
                res = Address.objects.get(contact_id=id)
                results[id].append(res.address_type)
                results[id].append(res.address)
                results[id].append(res.city)
                results[id].append(res.state)
                results[id].append(res.zip)

            except:
                print("Error display search - Address")

            try:
                res=Phone.objects.get(contact_id=id)
                results[id].append(res.phone_type)
                results[id].append(res.area_code)
                results[id].append(res.number)

            except:
                print("Error display search - Phone")

            try:
                res=Date.objects.get(contact_id=id)
                results[id].append(res.date_type)
                results[id].append(res.date)

            except:
                print("Error display search - Date")

            context["result_list"]=results

        context["delete_link"]="http://localhost:8000/search/?delete_id="
        context["base_link"]="http://localhost:8000/update/?contact_id="
        return render(request,'search_results.html',context)

    else:

        if "delete_id" in request.GET:
            print("Delete id : ",request.GET.get("delete_id"))
            delete(request.GET.get("delete_id"))
            messages.success(request,"Deleted Successfully")

        context= {"formSearch": Search()}
        return render(request, 'search_results.html', context)

def update(request):
    context ={}
    id = request.GET.get('contact_id')

    if request.method=='POST':

        update_flag=True
        contact_id=id
        contact=""

        try:
            try:
                contact_local = Contact.objects.get(pk=id)
                contact_local.fname = request.POST.get('fname')
                contact_local.mname = request.POST.get('mname')
                contact_local.lname = request.POST.get('lname')
                contact_id = contact_local.id
                contact=contact_local
            except:
                update_flag=False

            try:
                address = Address.objects.get(contact_id=contact_id)
                address.address_type = request.POST.get('address_type',"")
                address.address = request.POST.get('address',"")
                address.city = request.POST.get('city', "")
                address.state = request.POST.get('state', "")
                if request.POST.get("zip", None) == "":
                    address.zip = None
                else:
                    address.zip = request.POST.get("zip", None)
                address.save()

            except ObjectDoesNotExist:
                print("Address Field No values Updation")
            except:
                update_flag = False

            try:
                phone = Phone.objects.get(contact_id=contact_id)
                phone.phone_type = request.POST.get('phone_type',"")
                if request.POST.get("area_code", None) == "":
                    phone.area_code = None
                else:
                    phone.area_code = request.POST.get("area_code", None)
                if request.POST.get("number", None) == "":
                    phone.number = None
                else:
                    phone.number = request.POST.get("number", None)
                phone.save()

            except ObjectDoesNotExist:
                print("Phone Field No values Updation")
            except:
                update_flag=False

            try:
                date = Date.objects.get(contact_id=contact_id)
                date.date_type = request.POST.get('date_type',"")
                if request.POST.get("date", None) == "":
                    date.date = None
                else:
                    date.date = request.POST.get("date", None)
                date.save()

            except ObjectDoesNotExist:
                print("Date Field No values Updation")
            except:
                update_flag=False

            # saving to DB ny checking all flags
            if(update_flag) :
                try:
                    contact.save()
                    messages.success(request,"Contact updated")

                    context['form'] = ContactForm()
                    return render(request, 'add_contact.html', context)

                except Exception:
                    raise Exception("Contact Update failed Exception Raised")

        except Exception:

            traceback.print_exc()
            messages.success(request, "Contact update failed")

            # trying to load same update page with fields filled on eception
            return reload(id,request)

    else:
       return reload(id,request)

def reload(id,request):
    # id = request.GET.get('contact_id')
    context={}

    if not request.GET._mutable:
        request.GET._mutable = True

    contact = Contact.objects.get(pk=id)
    request.GET['fname'] = contact.fname
    request.GET['mname'] = contact.mname
    request.GET['lname'] = contact.lname
    contact_id = contact.id

    try:
        address = Address.objects.get(contact_id=contact_id)
        request.GET['address_type'] = address.address_type
        request.GET['address'] = address.address
        request.GET['city'] = address.city
        request.GET['state'] = address.state
        request.GET['zip'] = address.zip
    except ObjectDoesNotExist:
        print("Address Field No values - reload")

    try:
        phone = Phone.objects.get(contact_id=contact_id)
        request.GET['phone_type'] = phone.phone_type
        request.GET['area_code'] = phone.area_code
        request.GET['number'] = phone.number
    except ObjectDoesNotExist:
        print("Phone Field No values - reload")

    try:
        date = Date.objects.get(contact_id=contact_id)
        request.GET['date_type'] = date.date_type
        request.GET['date'] = date.date
    except ObjectDoesNotExist:
        print("Date Field No values - reload")

    context['form'] = UppdateForm(request.GET)
    return render(request,'update.html',context)

def add_csv(file_path):
    with open(file_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            p = Contact(fname=row['first_name'],mname=row['middle_name'],lname=row['last_name'])
            p.save()
        #
        # for row in reader:
        #     p = Address(address_type=row[""])
        #     p.save()
        #
        # for row in reader:
        #     p = Contact(fname=row['first_name'],mname=row['middle_name'],lname=row['last_name'])
        #     p.save()

def delete(id):

    # ---------------------write deleting database entry given ID -------------------#
    print(id)


