from django.shortcuts import render
from artikel.models import Kategori, Artikel

def home(request) :
    template_name = "index.html"
    context = {
        "title": "Home",
    }
    return render(request, template_name, context)

def aboutme(request) :
    template_name = "aboutme.html"
    context = {
        "title": "About Me",
    }
    return render(request, template_name, context)