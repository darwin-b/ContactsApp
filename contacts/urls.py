from django.urls import path
from contacts import views


urlpatterns = [
    path("",views.add_contact,name="add_contact"),
    path("search/", views.search, name="search"),
    path("update/", views.update, name="update"),
]