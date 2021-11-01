from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from . import util

class NewEntryForm(forms.Form):
    # Users should be able to enter a title for the page.
    title = forms.CharField(label="Title")
    # In a textarea, should be able to enter the Markdown content for the page.
    markdown = forms.CharField(label="Markdown Content", widget=forms.Textarea)

class EditEntryForm(forms.Form):
    # User should be able to edit that entry’s Markdown content in a textarea
    markdown = forms.CharField(label="Markdown Content", widget=forms.Textarea )
    

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

    # Get the proper case of entry name
    entries = util.list_entries()
    for entry in entries:
        entry_lower = entry.lower()
        if title.lower() == entry_lower:
            title = entry

    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    else:
        markdown = util.get_entry(title)
        
        # Convert the Markdown into HTML
        markdowner = Markdown()
        content = markdowner.convert(markdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
def search(request):
    """
    Allow the user to type a query into the search box in 
    the sidebar to search for an encyclopedia entry.
    """

    if request.method == "GET":
        title = request.GET.get("q")

        # If the query matches the name of an encyclopedia entry, 
        # the user should be redirected to that entry’s page.
        if util.get_entry(title):
            return HttpResponseRedirect(f"/wiki/{title}")
        
        # If the query does not match the name of an encyclopedia 
        # entry, the user should instead be taken to a search 
        # results page that displays a list of all encyclopedia 
        # entries that have the query as a substring. 
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                entry_lower = entry.lower()
                if title.lower() in entry_lower:
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
def create(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the entry from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]

            # When the page is saved, if an encyclopedia entry already exists
            # with the provided title, the user should be presented with an error message.
            if util.get_entry(title):
                return render(request, "encyclopedia/create_error.html", {
                    "title": title
                })

            # Otherwise, the encyclopedia entry should be saved to disk, 
            # and the user should be taken to the new entry’s page.
            else:
                util.save_entry(title, markdown)
                return HttpResponseRedirect(f"/wiki/{title}")

        else:
            # If the form id invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method == "GET":
        markdown = util.get_entry(title)
        
        # Convert the Markdown into HTML
        markdowner = Markdown()
        content = markdowner.convert(markdown)
        
        # The textarea should be pre-populated with the existing Markdown content of the page.
        pre = EditEntryForm(initial={'markdown': content})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "markdown": pre
        })
    else:
        # Take in the data the user edited and save it as edited
        edited = EditEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if edited.is_valid():
            markdown = edited.cleaned_data["markdown"]

            # Save the changes made to that entry to disk
            util.save_entry(title, markdown)

            # Once the entry is saved, the user should be redirected back to that entry’s page.
            return HttpResponseRedirect(f"/wiki/{title}")

