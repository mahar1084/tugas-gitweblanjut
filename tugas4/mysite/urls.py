"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Untuk Media
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from mysite.views import *

from django.contrib import admin
from django.urls import path
from mysite import views  # Ganti sesuai nama folder project kamu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_home, name='home'),
    path('aboutme/', views.about_me, name='aboutme'),  # ← ini penting!
    path('artikel/<int:id>/', views.detail_artikel, name='detail_artikel'),
    path('artikel-not-found/', views.not_found_artikel, name='not_found_artikel'),
    path('about/', views.about_me, name='about'),
]



# Untuk Media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
