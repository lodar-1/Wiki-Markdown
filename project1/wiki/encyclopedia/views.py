from django.shortcuts import render
import markdown2
import random
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

def edit(request):
	try:
		if request.method == "POST":
			form = addForm(request.POST)
			if form.is_valid():
				stitle = form.cleaned_data["title"]			
				util.save_entry(stitle, form.cleaned_data["content"])
				return HttpResponseRedirect("/wiki/" + stitle)
			else:
				return render(request, "encyclopedia/editentry.html", {"Error": "A validation error occcured."})	
		else:
			return render(request, "encyclopedia/editentry.html")
	except:
		return render(request, "encyclopedia/editentry.html", {"Error": "An error occcured. Please try again."})	
				
def randomentry(request):
	listitems = util.list_entries()
	if listitems:
		sTitle 	= random.choice(listitems)
		return HttpResponseRedirect("/wiki/" + sTitle)
	else:	
		return render(request, "encyclopedia/editentry.html", {"Error": "There are no wiki entries."})
		
def add(request):
	try:
		if request.method == "POST":
			listitems = util.list_entries()
			for li in listitems:
				if li.upper() == request.POST.get("title").strip().upper():
					return render(request, "encyclopedia/addentry.html", {"Error": 'An entry with this title already exists', "stitle": request.POST.get("title").strip(), "scontent": request.POST.get("content") })
			form = addForm(request.POST)
			if form.is_valid():
				sTitle = form.cleaned_data["title"]
				util.save_entry(sTitle, form.cleaned_data["content"])
				return HttpResponseRedirect("/wiki/" + sTitle)
			else:
				return render(request, "encyclopedia/addentry.html", {"Error": "An error occcured."})	
		else:
			return render(request, "encyclopedia/addentry.html")
	except: 
		return render(request, "encyclopedia/addentry.html", {"Error": "An error occcured."})	
		
def entry(request, entry):
	try: 
		error = ""
		if request.method == "POST":
			sContent = util.get_entry(entry)
			if sContent == None:
				error = True
				sContent = "<font class='error'>Error: Page not found</font>"
				entry = "<font class='error'>Error - Page not found</font>"	
			return render(request, "encyclopedia/editentry.html", {"title": entry, "content":sContent, "error": error})					

		else:	
			sContent = util.get_entry(entry)
			if sContent is not None:
				sContent = markdown2.markdown(sContent)
			else:
				error = True
				sContent = "<font class='error'>Error: Page not found</font>"
				entry = "Error - Page not found"	
			return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent, "error": error})
	except: 
		sContent = "<font class='error'>Error - An error occured. Please try again./font>"
		entry = f"Error: {search}"	
		return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent})	

def search(request):
	try:
		if request.method == "POST":
			search = request.POST.get("q").strip()
			if len(search):
				entries = util.list_entries()
				bfound = False
				entrylist = []
				for entry in entries:
					if search.upper() == entry.upper():
						bfound = True
						sContent = util.get_entry(entry)
						if sContent is not None:
							sContent = markdown2.markdown(sContent)
						else:
							sContent = f"Error: Page not found ({search})"
							entry = "<font class='error'>Error - Page not found</font>"	
						return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent})					
					else: 
						if search.upper() in entry.upper():
							entrylist.append(entry)
				if not entrylist:
					sContent = "Search returned no results"
					entry = "Search"
					return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent})
				else:
					return render(request, "encyclopedia/search.html", {"title": "Search Results", "entries":entrylist})
			else:
				sContent = "Invalid Search Entry"
				entry = "Search"
				return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent})						
	except: 
		sContent = "<font class='error'>Error - An error occured. Please try again./font>"
		entry = f"Error: {search}"	
		return render(request, "encyclopedia/entry.html", {"title": entry, "entry":sContent})					
		
