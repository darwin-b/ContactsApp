from django.urls import path
from contacts import views


urlpatterns = [
    path("",views.add_contact,name="add_contact"),
]