from django.contrib import admin
from django.urls import path, include
from django.urls import path
from mysite import views
from mysite.authentication import login, logout, registrasi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_home, name='my_home'),
    path('aboutme/', views.about_me, name='aboutme'),
    path('artikel/<int:id>/', views.detail_artikel, name='detail_artikel'),
    path('artikel-not-found/', views.not_found_artikel, name='not_found_artikel'),
    path('about/', views.about, name='about'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', include("artikel.urls")),
    path('auth-login', login, name="login"),
    path('auth-logout', logout, name="logout"),
    path('auth-registrasi', registrasi, name="registrasi"),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
