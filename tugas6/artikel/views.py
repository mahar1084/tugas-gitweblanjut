# artikel/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group

# Import model Comment yang baru dari artikel.models
from artikel.models import Kategori, Artikel, Comment
from artikel.forms import KategoriForms, ArtikelForms

# Impor untuk Django REST Framework
from rest_framework import generics, permissions
# Impor CommentSerializer yang baru
from .serializers import KategoriSerializer, ArtikelSerializer, CommentSerializer

# Custom Permission untuk memastikan hanya pemilik objek yang bisa mengedit/menghapus
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read-only permissions are allowed for any request.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user or request.user.is_staff # Admin juga bisa edit/hapus


# Create your views here.
def in_operator(user):
    get_user = user.groups.filter(name='Operator').count()
    if get_user == 0:
        return False
    else:
        return True

######################## user bisa ###########################
@login_required(login_url='/auth-login')
def artikel_list(request):
    template_name = "dashboard/pengguna/artikel_list.html"
    artikel = Artikel.objects.filter(created_by=request.user)
    context = {
        "artikel":artikel
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil tambah artikel')
        return redirect(artikel_list)
    forms = ArtikelForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def artikel_update(request, id_artikel):
    template_name = "dashboard/artikel_forms.html"
    try:
        artikel = Artikel.objects.get(id=id_artikel, created_by=request.user)
    except Artikel.DoesNotExist:
        messages.warning(request, "halaman yang diminta tidak ditemukan")
        return redirect("/")
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES, instance=artikel)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil melakukan update artikel')
        return redirect(artikel_list)
    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
def artikel_delete(request, id_artikel):
    try:
        Artikel.objects.get(id=id_artikel, created_by=request.user).delete()
        messages.success(request, 'berhasil delete artikel')
    except Artikel.DoesNotExist:
        messages.error(request, 'artikel tidak ditemukan atau Anda tidak memiliki izin untuk menghapusnya')
    except Exception as e:
        messages.error(request, f'gagal delete artikel: {e}')

    return redirect(artikel_list)


###################### ADMIN #########################
@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_list(request):
    template_name = "dashboard/admin/kategori_list.html"
    kategori = Kategori.objects.all()
    context = {
        "kategori":kategori
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_tambah(request):
    template_name = "dashboard/admin/kategori_forms.html"
    if request.method == "POST":
        forms = KategoriForms(request.POST)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil tambah kategori')
        return redirect(admin_kategori_list)
    forms = KategoriForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_update(request, id_kategori):
    template_name = "dashboard/admin/kategori_forms.html"
    try:
        kategori = Kategori.objects.get(id=id_kategori)
    except Kategori.DoesNotExist:
        messages.warning(request, "Kategori yang diminta tidak ditemukan.")
        return redirect(admin_kategori_list)

    if request.method == "POST":
        forms = KategoriForms(request.POST, instance=kategori)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil update kategori')
        return redirect(admin_kategori_list)
    forms = KategoriForms(instance=kategori)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_delete(request, id_kategori):
    try:
        Kategori.objects.get(id=id_kategori).delete()
        messages.success(request, 'berhasil delete kategori')
    except Kategori.DoesNotExist:
        messages.error(request, 'kategori tidak ditemukan')
    except Exception as e:
        messages.error(request, f'gagal delete kategori: {e}')

    return redirect(admin_kategori_list)

############## Artikel Blog ##################
@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_list(request):
    template_name = "dashboard/admin/artikel_list.html"
    artikel = Artikel.objects.all()
    context = {
        "artikel":artikel
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil tambah artikel')
            print("Artikel berhasil disimpan di database!") 
            return redirect(admin_artikel_list)
        else:
            print("Form tidak valid saat tambah artikel:") 
            print(forms.errors) 
    forms = ArtikelForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_update(request, id_artikel):
    template_name = "dashboard/admin/artikel_forms.html"
    try:
        artikel = Artikel.objects.get(id=id_artikel)
    except Artikel.DoesNotExist:
        messages.warning(request, "Artikel yang diminta tidak ditemukan.")
        return redirect(admin_artikel_list)

    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES, instance=artikel)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil melakukan update artikel')
        return redirect(admin_artikel_list)
    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_delete(request, id_artikel):
    try:
        Artikel.objects.get(id=id_artikel).delete()
        messages.success(request, 'berhasil delete artikel')
    except Artikel.DoesNotExist:
        messages.error(request, 'artikel tidak ditemukan')
    except Exception as e:
        messages.error(request, f'gagal delete artikel: {e}')

    return redirect(admin_artikel_list)


# Fungsi view baru untuk artikel tidak ditemukan
def artikel_tidak_ditemukan(request):
    template_name = "artikel_not_found.html"
    context = {
        "message": "Artikel yang Anda cari tidak ditemukan.",
        "title": "Artikel Tidak Ditemukan"
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = "landingpage/detail_artikel.html"
    try:
        artikel = Artikel.objects.get(id=id)
    except Artikel.DoesNotExist:
        return redirect('artikel_tidak_ditemukan')

    artikel_lainnya = Artikel.objects.all().exclude(id=id)

    context = {
        "title":"Artikel",
        "artikel": artikel,
        "artikel_lainnya":artikel_lainnya
    }
    return render(request, template_name, context)

################### Management User Oleh Operator ###################

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_list(request):
    template_name = "dashboard/admin/user_list.html"
    daftar_user = User.objects.all()
    context = {
        "daftar_user": daftar_user
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_edit(request, user_id):
    template_name = "dashboard/admin/user_edit.html"
    user = get_object_or_404(User, pk=user_id)

    all_groups = Group.objects.all()
    group_user = []
    for group in user.groups.all():
        group_user.append(group.name)

    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        is_staff_input = request.POST.get("is_staff")
        groups_checked = request.POST.getlist('groups')

        if is_staff_input is None:
            is_staff = False
        else:
            is_staff = True

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.groups.set(Group.objects.filter(id__in=groups_checked))
        user.save()

        messages.success(request, f"Berhasil update user {user.username}")
        return redirect('admin_management_user_list')

    context = {
        'user': user,
        'all_groups': all_groups,
        'group_user': group_user,

    }
    return render(request, template_name, context)

# Fungsi view baru untuk menghapus user dari antarmuka website
@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_delete(request, user_id):
    try:
        user_to_delete = get_object_or_404(User, pk=user_id)

        # Pencegahan: Jangan biarkan admin menghapus dirinya sendiri jika tidak ada admin lain
        # Atau admin tidak boleh menghapus superuser
        if request.user.pk == user_to_delete.pk:
            messages.error(request, "Anda tidak dapat menghapus akun Anda sendiri melalui antarmuka ini.")
            return redirect('admin_management_user_list')

        if user_to_delete.is_superuser:
            messages.error(request, "Anda tidak dapat menghapus Superuser.")
            return redirect('admin_management_user_list')

        user_to_delete.delete()
        messages.success(request, f"Pengguna {user_to_delete.username} berhasil dihapus.")
    except User.DoesNotExist:
        messages.error(request, "Pengguna tidak ditemukan.")
    except Exception as e:
        messages.error(f"Gagal menghapus pengguna: {e}")

    return redirect('admin_management_user_list')


############## API Views ##############
# API untuk Kategori
class KategoriListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KategoriRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# API untuk Artikel
class ArtikelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Artikel.objects.all()
    serializer_class = ArtikelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ArtikelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artikel.objects.all()
    serializer_class = ArtikelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# API untuk Komentar
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self): # Tambahkan metode ini!
        artikel_id = self.request.query_params.get('artikel')
        print(f"Mengambil komentar untuk artikel ID: {artikel_id}") # Debugging
        if artikel_id:
            try:
                # Memfilter komentar berdasarkan ID artikel dan mengurutkan dari yang terbaru
                return Comment.objects.filter(artikel__id=artikel_id).order_by('-created_at')
            except ValueError: # Jika artikel_id bukan integer
                return Comment.objects.none() # Kembalikan queryset kosong
        return Comment.objects.all().order_by('-created_at') # Default: kembalikan semua komentar jika tidak ada filter artikel

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]