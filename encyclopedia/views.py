from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    1. If an entry is requested that does not exist, the user should 
    be presented with an error page indicating that their requested
    page was not found.
    
    2. If the entry does exist, the user should be presented with a page
    that displays the content of the entry.
    """
    
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })
    
    else:
        markdown = util.get_entry(title)
        
        # Convert the Markdown into HTML
        markdowner = Markdown()
        content = markdowner.convert(markdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": content
        })
def search(request):
    """
    Allow the user to type a query into the search box in 
    the sidebar to search for an encyclopedia entry.
    """
    
    # If the query matches the name of an encyclopedia entry, 
    # the user should be redirected to that entry’s page.
    if request.method == "GET":
        title = request.GET.get("q")
        return HttpResponseRedirect(f"/wiki/{title}")
