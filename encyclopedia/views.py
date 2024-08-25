from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import secrets
from django.core.exceptions import ValidationError

from . import util

markdown_conversion = Markdown()


def validator_title_unique(text):
    if util.get_entry(text) is not None:
        raise ValidationError("post already exists")


class NewWikiEntry(forms.Form):
    new_entry_title = forms.CharField(max_length=100, validators=[
                                      validator_title_unique], label="Title ")
    new_entry_content = forms.CharField(
        widget=forms.Textarea(), label="Content")


class EditWikiEntry(forms.Form):
    edit_entry_title = forms.CharField(
        max_length=100, label="Title ", initial="xx")
    edit_entry_content = forms.CharField(
        widget=forms.Textarea(), label="Content", initial="yy")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_entry": secrets.choice(util.list_entries())
    })


def entry(request, title):
    entry = util.get_entry(title)
    entry_html = markdown_conversion.convert(entry)
    if entry == None:
        return render(request, "encyclopedia/404.html", {
            "entry": entry_html,
            "entry_title": title,
            "random_entry": secrets.choice(util.list_entries())
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry_html,
            "entry_title": title,
            "random_entry": secrets.choice(util.list_entries())
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
            if search_results == []:
                search_results = 0
            return render(request, "encyclopedia/search.html", {
                "param": param,
                "search_results": search_results,
                "entry": entry,
                "random_entry": secrets.choice(util.list_entries())
            })
        else:
            return HttpResponseRedirect(param)


def add(request):
    if request.method == "POST":
        form = NewWikiEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["new_entry_content"]
            title = form.cleaned_data["new_entry_title"]
            word = "# "
            if word in title:
                title = title.lstrip(word)
            content_title = f"# {title}\n\n" + content
            util.save_entry(title, content_title)
            return HttpResponseRedirect("/wiki/" + title)
        else:
            return render(request, "encyclopedia/add.html", {"form": form})
    else:
        return render(request, "encyclopedia/add.html", {"form": NewWikiEntry()})


def edit(request):
    edit_title = request.GET.get("title")
    edit_form = EditWikiEntry(initial={'edit_entry_title': request.GET.get(
        "title"), 'edit_entry_content': util.get_entry(edit_title)})
    return render(request, "encyclopedia/edit.html", {
        "form": edit_form
    })
