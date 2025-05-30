from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Artikel, Kategori

# ===== Function-based Views =====
def artikel_list(request):
    artikels = Artikel.objects.filter(status=True).order_by('-created_at')
    paginator = Paginator(artikels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'artikels': page_obj,
        'title': 'Daftar Artikel',
    }
    return render(request, 'artikel_list.html', context)

def artikel_detail(request, id):
    artikel = get_object_or_404(Artikel, id=id, status=True)
    context = {
        'artikel': artikel,
        'title': artikel.judul,
    }
    return render(request, 'detail_artikel.html', context)

def kategori_list(request):
    kategoris = Kategori.objects.all()
    context = {
        'kategoris': kategoris,
        'title': 'Daftar Kategori',
    }
    return render(request, 'kategori_list.html', context)

def artikel_list_by_kategori(request, kategori_slug):
    kategori = get_object_or_404(Kategori, slug=kategori_slug)
    artikels = Artikel.objects.filter(kategori=kategori, status=True).order_by('-created_at')
    paginator = Paginator(artikels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'artikels': page_obj,
        'kategori': kategori,
        'title': kategori.nama,
    }
    return render(request, 'artikel_list_by_kategori.html', context)

# ===== Class-based Views =====
class ArtikelListView(ListView):
    model = Artikel
    template_name = 'artikel_list.html'
    context_object_name = 'artikels'
    queryset = Artikel.objects.filter(status=True).order_by('-created_at')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Artikel'
        return context

class ArtikelDetailView(DetailView):
    model = Artikel
    template_name = 'detail_artikel.html'
    context_object_name = 'artikel'

    def get_object(self, queryset=None):
        return get_object_or_404(Artikel, id=self.kwargs['id'], status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.judul
        return context

class KategoriListView(ListView):
    model = Kategori
    template_name = 'kategori_list.html'
    context_object_name = 'kategoris'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Kategori'
        return context
