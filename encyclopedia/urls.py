from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add",  views.add, name="add"),
    path("test", views.testeconsole, name="test"),
    path("<str:title>", views.entry, name="entry"),
]
