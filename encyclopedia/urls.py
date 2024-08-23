from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry")
    # path("wiki/<slug:title>/", views.title, name="title")
]
