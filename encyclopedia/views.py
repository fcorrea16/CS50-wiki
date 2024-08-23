from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# def entry(request, title):
#     return render(request, "encyclopedia/entry.html", {
#         "entry_title": title.capitalize(),
#         "entry": util.get_entry(title),

#     })


def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/404.html", {
            "entry": entry,
            "entry_title": title.capitalize(),
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "entry": util.get_entry(title)

        })
