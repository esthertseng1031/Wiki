import markdown
from django.shortcuts import render
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
        text = util.get_entry(title)
        
        # Convert the Markdown into HTML
        html = markdown.markdown(text)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": html
        })

