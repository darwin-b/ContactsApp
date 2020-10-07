from django.shortcuts import render

# Create your views here.

def add_contact(request):
    return render(request,'add_contact.html',{})