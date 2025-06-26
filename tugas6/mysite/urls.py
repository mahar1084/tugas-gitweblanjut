from django.contrib import admin
from django.urls import path, include
from mysite import views
from django.conf import settings

# Untuk Media
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Impor dari mysite.views
from mysite.views import (
    my_home,
    about,
    dashboard,
    not_found_artikel,
    UserProfileListAPIView,
    UserProfileRetrieveUpdateAPIView
)
# Impor dari authentication
from mysite.authentication import login, logout, registrasi
# Impor dari artikel.views
from artikel.views import detail_artikel, artikel_tidak_ditemukan, artikel_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_home, name="my_home"),
    path('artikel/<int:id>', detail_artikel, name="detail_artikel"),
    path('artikel-tidak-ditemukan/', artikel_tidak_ditemukan, name="artikel_tidak_ditemukan"),
    path('about', about, name="about"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/artikel_list', artikel_list, name="artikel_list"),

    # Ini adalah include untuk URL DASHBOARD yang ada di aplikasi 'artikel'
    # Misal: /dashboard/operator/kategori/list
    path('dashboard/', include("artikel.urls")),

    # === BARIS PENTING YANG DITAMBAHKAN UNTUK API SECARA GLOBAL ===
    # Ini akan mengarahkan SEMUA URL API dari aplikasi 'artikel'
    # ke awalan /api/ (misal: /api/comments/, /api/artikel/, /api/kategori/)
    path('api/', include("artikel.urls")), # <--- TAMBAHKAN BARIS INI ATAU PASTIKAN SUDAH ADA


    ###### Authentication ######
    path('auth-login', login, name="login"),
    path('auth-login/', login, name="login"),
    path('auth-logout', logout, name="logout"),
    path('auth-registrasi', registrasi, name="registrasi"),

    ########################## API URL Patterns for User Profiles ##################
    path('api/users/', UserProfileListAPIView.as_view(), name='api_user_list'),
    path('api/users/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='api_user_detail'),
    path('api/me/', UserProfileRetrieveUpdateAPIView.as_view(), name='api_my_profile'),
]

# Untuk Media
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)