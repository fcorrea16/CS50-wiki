from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": title.capitalize()
    })

    # def entry(request, title):
    #     return render(request, "encyclopedia/entry.html", {
    #         # "entry": title
    #         # "entry": util.get_entry(title)
    #         "title": util.get_entry(title)
