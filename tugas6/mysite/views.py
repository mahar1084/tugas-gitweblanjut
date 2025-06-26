from django.shortcuts import render, redirect
# Impor model User
from django.contrib.auth.models import User # Tambahkan ini

from artikel.models import Kategori, Artikel

# Impor untuk Django REST Framework
from rest_framework import generics, permissions # Tambahkan ini
from mysite.serializers import UserProfileSerializer # Impor Serializer yang sudah Anda buat


def about_me(request):
    template_name = "aboutme.html"
    context = {
        "title": "About Me",
    }
    return render(request, template_name, context)

def my_home(request):
    template_name = "landingpage/index.html"
    kategori_list = Kategori.objects.all()
    artikel = Artikel.objects.all()
    print(artikel)

    context = {
        "title": "My Home",
        "Kategori": kategori_list,
        "artikel": artikel
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = "landingpage/detail_artikel.html"
    try:
        artikel = Artikel.objects.get(id=id)
    except Artikel.DoesNotExist:
        return redirect('artikel_tidak_ditemukan') # Gunakan nama URL 'artikel_tidak_ditemukan'

    artikel_lainnya = Artikel.objects.all().exclude(id=id)

    context = {
        "title": "Artikel",
        "artikel": artikel,
        "artikel_lainnya":artikel_lainnya
    }
    return render(request, template_name, context)

def not_found_artikel(request):
    template_name = "artikel_not_found.html"
    return render(request, template_name)

def about(request):
    template_name = "about.html"
    context = {
        "title": "CV Maharani Sabrina"
    }
    return render(request, template_name, context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/auth-login')
    
    template_name = "dashboard/index.html"
    context = {
        "title":"Selamat Datang"
    }
    return render(request, template_name, context)

def artikel_list(request):
    template_name = "dashboard/artikel_list.html"
    context = {
        "title":"Selamat Datang"
    }
    return render(request, template_name, context)

############## API Views for User Profile ##############

# API untuk menampilkan daftar semua profil pengguna (biasanya hanya untuk admin)
class UserProfileListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser] # Hanya pengguna dengan is_staff=True yang bisa melihat semua profil

# API untuk mengambil dan memperbarui profil pengguna yang sedang login
class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # Hanya pengguna yang sudah login yang bisa mengakses ini

    def get_object(self):
        # Jika pengguna adalah staff/admin, mereka bisa mengambil profil pengguna lain berdasarkan ID (pk)
        if self.request.user.is_staff:
            return super().get_object()
        # Untuk pengguna biasa, mereka hanya bisa mengakses profil mereka sendiri
        # Ini memastikan bahwa URL /api/me/ (jika kita buat) akan mengarah ke profil mereka
        # Atau jika menggunakan /api/users/<id>/, pengguna biasa hanya bisa akses ID mereka sendiri
        if self.kwargs.get('pk') and self.kwargs['pk'] != self.request.user.pk and not self.request.user.is_staff:
             raise permissions.PermissionDenied("You are not allowed to access this user's profile.")
        return self.request.user
    
    # get_queryset ini hanya diperlukan jika ada filter khusus pada queryset,
    # tapi untuk get_object() yang di-override di atas, ini tidak terlalu krusial
    # namun baik untuk kejelasan.
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)