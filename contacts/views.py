import csv

from django.contrib import messages
from django.shortcuts import render

from django.db.models import Q

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
                save_phone.number = request.POST.get('number', None)
                save_phone.save()

            save_date = Date()
            if request.POST.get('date_type')and contact_id!=-1:
                save_date.contact_id=save_contact
                save_date.date_type = request.POST.get('date_type')
                save_date.date = request.POST.get('date',None)
                save_date.save()
        messages.success(request,"Contact successfully added")

        return render(request,'add_contact.html',context)
    else:

        # add_csv(filepath)

        return render(request, 'add_contact.html', context)

def search(request):
    context={}
    context["formSearch"]= Search()
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

        print("Search results in Contact: ")
        for result in context["contact_results"]:
            contact_ids.append(result.id)


        print("Search Results in Address: ")
        for result in context["address_results"]:
            contact_ids.append(result.contact_id.id)

        for result in context["phone_results"]:
            contact_ids.append(result.contact_id.id)

        for result in context["date_results"]:
            contact_ids.append(result.contact_id.id)

        # print("Ids : ", contact_ids)

        links= {}
        results={}

        for id in contact_ids:

            res=Contact.objects.get(pk=id)
            results[id]=[res.fname,res.mname,res.lname]

            links[id] = "http://localhost:8000/update/?contact_id="+str(id) + "&fname=" + res.fname + \
                       "&mname=" + res.mname + \
                       "&lname=" + res.lname

            try:
                res = Address.objects.get(contact_id=id)
                results[id].append(res.address_type)
                results[id].append(res.address)
                results[id].append(res.city)
                results[id].append(res.state)
                results[id].append(res.zip)

                links[id]= links[id]+"&address_type=" + res.address_type + "&address=" + res.address+ "&city=" + res.city + "&state=" + res.state+ "&zip="+str(res.zip)

            except :
                links[id] = links[id]+"&address_type=" + "&address=" + "&city="+"&state="+"&zip="

            try:
                res=Phone.objects.get(contact_id=id)
                results[id].append(res.phone_type)
                results[id].append(res.area_code)
                results[id].append(res.number)

                links[id] = links[id] + "&phone_type=" + res.phone_type + "&area_code=" + str(res.area_code) + "&number=" + str(res.number)

            except :
                links[id] = links[id] + "&phone_type=" + "&area_code=" + "&number="

            try:
                res=Date.objects.get(contact_id=id)
                results[id].append(res.date_type)
                results[id].append(res.date)

                links[id] = links[id] + "&date_type=" + res.date_type + "&date=" + str(res.date)
            except :
                links[id] = links[id] + "&date_type=" + "&date_type="

            context["result_list"]=results
            context["update_links"]=links

        return render(request,'search_results.html',context)

    else:
        return render(request, 'search_results.html', context)

def update(request):
    context ={}

    if request.method=='POST':
        print("hi")
        id = request.GET.get('contact_id')
        print(id)
        try:
            contact = Contact.objects.get(pk=id)
            contact.fname=request.POST.get('fname')
            contact.mname = request.POST.get('mname')
            contact.lname = request.POST.get('lname')
            contact_id=contact.id

            address = Address.objects.get(contact_id=contact_id)
            address.address_type = request.POST.get('address_type')
            address.address = request.POST.get('address',"")
            address.city = request.POST.get('city', "")
            address.state = request.POST.get('state', "")
            address.zip = request.POST.get('zip', None)
            address.save()

            phone = Phone.objects.get(contact_id=contact_id)
            phone.phone_type = request.POST.get('phone_type')
            phone.area_code = request.POST.get('area_code', None)
            phone.number = request.POST.get('number', None)
            phone.save()

            date = Date.objects.get(contact_id=contact_id)
            date.date_type = request.POST.get('date_type')
            date.date = request.POST.get('date', None)
            date.save()

            messages.success(request,"Contact updated")
        except:
            messages.success(request, "Contact update failed")

        context['form'] = ContactForm()
        return render(request,'add_contact.html',context)

    else:
        id=request.GET.get('contact_id')

        if not request.GET._mutable:
            request.GET._mutable = True

        contact = Contact.objects.get(pk=id)
        request.GET['fname'] = contact.fname
        request.GET['mname']  = contact.mname
        request.GET['lname']  = contact.lname
        contact_id=contact.id

        address = Address.objects.get(contact_id=contact_id)
        request.GET['address_type'] = address.address_type
        request.GET['address']  = address.address
        request.GET['city']  = address.city
        request.GET['state'] = address.state
        request.GET['zip'] = address.zip


        phone = Phone.objects.get(contact_id=contact_id)
        request.GET['phone_type'] = phone.phone_type
        request.GET['area_code']  = phone.area_code
        request.GET['number']  = phone.number

        date = Date.objects.get(contact_id=contact_id)
        request.GET['date_type'] = date.date_type
        request.GET['date']  = date.date

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



