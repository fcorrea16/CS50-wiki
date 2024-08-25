from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import MarkdownContent
from django import forms
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/404.html", {
            "entry": entry,
            "entry_title": title.capitalize(),
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": title.capitalize(),
            "entry": util.get_entry(title)
        })


def search(request):
    if request.method == "GET":
        param = request.GET.get("q")
        entry = util.get_entry(param)
        entry_titles = util.list_entries()
        search_results = []
        if entry == None:
            for entry_title in entry_titles:
                if param in entry_title:
                    search_results += [entry_title]
                    break
            return render(request, "encyclopedia/search.html", {
                "param": param,
                "search_results": search_results,
            })
        else:
            return HttpResponseRedirect(param)


class NewWikiEntry(forms.Form):
    new_entry_title = forms.CharField(max_length=100, label="Title ")
    new_entry_content = forms.CharField(
        widget=forms.Textarea(), label="Content")


def testeconsole(request, title, content):
    return render(request, "encyclopedia/testeconsole.html", {"title": title, "content": content})


def add(request):
    if request.method == "POST":
        form = NewWikiEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data("new_entry_title")
            content = form.cleaned_data("new_entry_content")
            title2 = form_title
            content2 = form_content
            print(title2)
            print(content2)
            # title = form.cleaned_data["new_entry_title"]
            # content = form.cleaned_data["new_entry_content"]
            util.save_entry(title, content)
            # return render(request, "encyclopedia/testeconsole.html", {"title": title, "content": content})
            return HttpResponseRedirect(reverse("wiki:index"))
        else:
            return render(request, "encyclopedia/add.html", {"form": form})
    else:
        return render(request, "encyclopedia/add.html", {"form": NewWikiEntry()})
