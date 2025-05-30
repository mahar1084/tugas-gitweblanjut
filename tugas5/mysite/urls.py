from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_home, name='my_home'),
    path('aboutme/', views.about_me, name='aboutme'),
    path('artikel/<int:id>/', views.detail_artikel, name='detail_artikel'),
    path('artikel-not-found/', views.not_found_artikel, name='not_found_artikel'),
    path('about/', views.about, name='about'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
