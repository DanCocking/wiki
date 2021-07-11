import os
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown
from . import util
from django import forms
from django.urls import reverse
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Contents")


    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() ,
        
    })

def title(request, title):
    return render(request, "encyclopedia/title.html", {
        "title": title, 
        "content": markdown.markdown(util.get_entry(title))
    })

def search(request):
    query = request.GET.get('q')
    if query.capitalize() in util.list_entries():
        return render(request, 'encyclopedia/title.html', {
        "title": query.capitalize(), 
        "content": markdown.markdown(util.get_entry(query.capitalize()))
        })
    matching_titles = [entry for entry in util.list_entries() if query in entry]
    return render(request, 'encyclopedia/search.html', {
        "object_list": matching_titles
    })

def create(request):
    new = False
    if request.method == "POST":
        form = NewPageForm(request.POST) 

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if os.path.isfile(f'entries/{title}.md'):
                new = True
                
            else:
                f = open(f'entries/{title}.md', "w")
                f.write(content)
                return HttpResponseRedirect(f"/wiki/{title}/")


    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm,
        "error": new
    })


def edit(request):

    if request.method == "POST":
        form = NewPageForm(request.POST) 

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            f = open(f'entries/{title}.md', "w")
            f.write(content)
            return HttpResponseRedirect(f"/wiki/{title}/")


    title = request.GET.get('q')
    form = NewPageForm({'title': f'{title}', 'content': f'{util.get_entry(title)}'})
    return render(request, "encyclopedia/edit.html", {
        "form": form
    })

def randomLink(request):
    titles = util.list_entries()
    title = titles[random.randint(0, len(titles)-1)]
    return render(request, "encyclopedia/title.html", {
        "title": title, 
        "content": markdown.markdown(util.get_entry(title))
    })
