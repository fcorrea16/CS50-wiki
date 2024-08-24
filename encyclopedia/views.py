from django.shortcuts import render
from django.http import HttpResponseRedirect

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
