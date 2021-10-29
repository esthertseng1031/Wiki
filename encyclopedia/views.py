from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    If an entry is requested that does not exist, the user should 
    be presented with an error page indicating that their requested
    page was not found.
    """
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })

