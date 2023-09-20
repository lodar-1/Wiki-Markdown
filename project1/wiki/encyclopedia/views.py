from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from . import util


class newSearch(forms.Form):
	searchphrase = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#DM 20230919
def entry(request, entry):
	#if entry=="search":
	#	return search(request)
	strEntry = util.get_entry(entry)
	if strEntry is not None:
		strEntry = markdown2.markdown(strEntry)
	else:
		strEntry = "Error: Page not foundxx"
		entry = "Error - Page not found"	
	return render(request, "encyclopedia/entry.html", {"title": entry, "entry":strEntry})

def search(request):
	if request.method == "POST":
		#form = newSearch(request.POST)
		#print(request.POST.get("q"))
		search = request.POST.get("q").strip()
		#print(form)
		if len(search):
			#search = form.cleaned_data["search"]
			entries = util.list_entries()
			bfound = False
			entrylist = []
			for entry in entries:
				if search.upper() == entry.upper():
					bfound = True
					strEntry = util.get_entry(entry)
					if strEntry is not None:
						strEntry = markdown2.markdown(strEntry)
					else:
						strEntry = f"Error: Page not found ({search})"
						entry = "Error - Page not found"	
					return render(request, "encyclopedia/entry.html", {"title": entry, "entry":strEntry})					
				else: 
					if search.upper() in entry.upper():
						#print(entry)
						entrylist.append(entry)
			if not entrylist:
				strEntry = "No results found"
				entry = "Search"
				return render(request, "encyclopedia/entry.html", {"title": entry, "entry":strEntry})
			else:
				return render(request, "encyclopedia/search.html", {"title": "Search Results", "entries":entrylist})
		else:
			strEntry = "Invalid Search Entry"
			entry = "Search"
			return render(request, "encyclopedia/entry.html", {"title": entry, "entry":strEntry})						
