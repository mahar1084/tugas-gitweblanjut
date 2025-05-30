from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(request):
    template_name = "login.html"
    pesan = "" 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            pesan ="Username atau Password wajib diisi"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                pesan = "Berhasil Login"
                return redirect("/")
            else:
                pesan ="Username atau Password salah"
       
    context = {
        'pesan':pesan
    }
    return render(request, template_name, context)


def registrasi(request):
    template_name = "registrasi.html"
    pesan = ""
    if request.method == "POST":
        username = request.POST.get('username')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not username or not password or not nama_depan or not nama_belakang or not password or not password2:
            pesan ="Semua data wajib diisi yah"
        else: 
            if password != password2:
                pesan = "password 1 dan 2 berbeda"
            else:
                user = User.objects.filter(username=username)
                if user.exists():
                    pesan = "username sudah digunakan"
                else:
                    user = User.objects.create(
                    username = username,
                    first_name = nama_depan,
                    last_name = nama_belakang,
                    password = password
                    )
                    user.set_password(password)
                    user.save()
                    return redirect("/auth-login")
    context = {
        'pesan':pesan
    }
    return render(request, template_name, context)

def logout(request):
    auth_logout(request)
    return redirect ('/')