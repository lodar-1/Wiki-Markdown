from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from . import util
from django.urls import reverse

class newSearch(forms.Form):
	searchphrase = forms.CharField()

class addForm(forms.Form):
	title = forms.CharField(label="title")
	content = forms.CharField(label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#DM 20230919
def edit(request):
	print("REQUEST FROM EDIT: ")
	print(request)
	if request.method == "POST":
		form = addForm(request.POST)
		if form.is_valid():
			stitle = form.cleaned_data["title"]			
			util.save_entry(stitle, form.cleaned_data["content"])
			strEntry = markdown2.markdown(form.cleaned_data["content"])
			#return render(request, "encyclopedia/entry.html", {"title": entry, "entry":strEntry})
			#return HttpResponseRedirect(reverse("encyclopedia/entry.html"))#, {"title": form.cleaned_data["title"], "entry":strEntry}))
			return HttpResponseRedirect("/wiki/" + stitle)
		else:
			return render(request, "encyclopedia/editentry.html", {"error": "A validation error occcured."})	
	else:
		return render(request, "encyclopedia/editentry.html")
		
	
def add(request):
	if request.method == "POST":
		listitems = util.list_entries()
		for li in listitems:
			if li.upper() == request.POST.get("title").strip().upper():
				return render(request, "encyclopedia/addentry.html", {"error": 'An entry with this title already exists', "stitle": request.POST.get("title").strip(), "scontent": request.POST.get("content") })
		form = addForm(request.POST)
		if form.is_valid():
			util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
			return render(request, "encyclopedia/entry.html", {"title": form.cleaned_data["title"], "entry":form.cleaned_data["content"]})
		#	return render(request, "form.cleaned_data['title'")
		else:
			return render(request, "encyclopedia/addentry.html", {"error": "An error occcured."})	
	else:
		return render(request, "encyclopedia/addentry.html")

def entry(request, entry):
	if request.method == "POST":
		strEntry = util.get_entry(entry)
		
		if strEntry == None:
			strEntry = f"Error: Page not found ({search})"
			entry = "Error - Page not found"	
		print("REQUEST FROM ENTRY")
		print(request)
		return render(request, "encyclopedia/editentry.html", {"title": entry, "content":strEntry})					

	else:	
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
