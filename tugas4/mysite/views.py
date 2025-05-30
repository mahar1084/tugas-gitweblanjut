from django.shortcuts import render, redirect
from artikel.models import Kategori, Artikel

def home(request):
    template_name = "index.html"
    context = {
        "title": "Home",
    }
    return render(request, template_name, context)

def about_me(request):
    template_name = "aboutme.html"
    context = {
        "title": "About Me",
    }
    return render(request, template_name, context)

def my_home(request):
    template_name = "index.html"
    kategori_list = Kategori.objects.all()
    artikel = Artikel.objects.all()
    print(artikel)

    context = {
        "title": "My Home",
        "kategori": kategori_list,
        "artikel": artikel
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = "detail_artikel.html"
    try:
        artikel = Artikel.objects.get(id=id)
    except Artikel.DoesNotExist:
        return redirect('not_found_artikel')  # atau redirect(not_found_artikel) jika di-import langsung

    print(artikel)

    context = {
        "title": "Artikel",
        "artikel": artikel
    }
    return render(request, template_name, context)

def not_found_artikel(request):
    template_name = "artikel_not_found.html"
    return render(request, template_name)

def about(request):
    template_name = "about.html"
    context = {
        "title": "CV Sendy Ahmad"
    }
    return render(request, template_name, context)
