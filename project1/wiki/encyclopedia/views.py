from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from . import util


class newSearch(forms.Form):
	searchphrase = forms.CharField()

class addForm(forms.Form):
	title = forms.CharField(label="title")
	comment = forms.CharField(label="comment")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#DM 20230919
def add(request):
	if request.method == "POST":
		listitems = util.list_entries()
		for li in listitems:
			if li.upper() == request.POST.get("title").strip().upper():
				return render(request, "encyclopedia/addentry.html", {"error": 'An entry with this name already exists', "stitle": request.POST.get("title").strip(), "scontent": request.POST.get("content") })
		form = addForm(request.POST) 
		if form.is_valid():
			util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
			return render(request, "encyclopedia/entry.html", {"title": form.cleaned_data["title"], "entry":form.cleaned_data["content"]})
		else:
			return render(request, "encyclopedia/addentry.html")	
	else:
		return render(request, "encyclopedia/addentry.html")

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
