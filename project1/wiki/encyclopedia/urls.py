from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("<str:entry>", views.entry, name="entry")
    
]
