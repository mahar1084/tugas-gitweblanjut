# tugas6/artikel/urls.py
from django.urls import path
from artikel.views import (
    artikel_list,
    artikel_tambah,
    artikel_update,
    artikel_delete,
    admin_kategori_list,
    admin_kategori_tambah,
    admin_kategori_update,
    admin_kategori_delete,
    admin_artikel_list,
    admin_artikel_tambah,
    admin_artikel_update,
    admin_artikel_delete,
    admin_management_user_list,
    admin_management_user_edit,
    admin_management_user_delete,
    detail_artikel,
    artikel_tidak_ditemukan,
    # === Impor API Views yang baru ===
    KategoriListCreateAPIView,
    KategoriRetrieveUpdateDestroyAPIView,
    ArtikelListCreateAPIView,
    ArtikelRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    ########################## fungsi untuk user biasa #################
    path('artikel/list', artikel_list, name="artikel_list"),
    path('artikel/tambah', artikel_tambah, name="artikel_tambah"),
    path('artikel/update/<int:id_artikel>', artikel_update, name="artikel_update"),
    path('artikel/delete/<int:id_artikel>', artikel_delete, name="artikel_delete"),
    path('artikel/<int:id>', detail_artikel, name="detail_artikel"),
    path('artikel-tidak-ditemukan/', artikel_tidak_ditemukan, name='artikel_tidak_ditemukan'),

    ########################## fungsi dari Operator #################
    path('operator/kategori/list', admin_kategori_list, name="admin_kategori_list"),
    path('operator/kategori/tambah', admin_kategori_tambah, name="admin_kategori_tambah"),
    path('operator/kategori/update/<int:id_kategori>', admin_kategori_update, name="admin_kategori_update"),
    path('operator/kategori/delete/<int:id_kategori>', admin_kategori_delete, name="admin_kategori_delete"),

    path('operator/artikel/list', admin_artikel_list, name="admin_artikel_list"),
    path('operator/artikel/tambah', admin_artikel_tambah, name="admin_artikel_tambah"),
    path('operator/artikel/update/<int:id_artikel>', admin_artikel_update, name="admin_artikel_update"),
    path('operator/artikel/delete/<int:id_artikel>', admin_artikel_delete, name="admin_artikel_delete"),

    path('operator/management-user/list', admin_management_user_list, name="admin_management_user_list"),
    path('operator/management-user/edit/<int:user_id>', admin_management_user_edit, name="admin_management_user_edit"),
    path('operator/management-user/delete/<int:user_id>', admin_management_user_delete, name="admin_management_user_delete"),

    ########################## API URL Patterns ##################
    # =====================================================================
    # PENTING: HAPUS AWALAN 'api/' DARI SEMUA PATH API DI SINI!
    # =====================================================================
    # API Kategori
    path('kategori/', KategoriListCreateAPIView.as_view(), name='api_kategori_list_create'),
    path('kategori/<int:pk>/', KategoriRetrieveUpdateDestroyAPIView.as_view(), name='api_kategori_detail'),

    # API Artikel
    path('artikel/', ArtikelListCreateAPIView.as_view(), name='api_artikel_list_create'),
    path('artikel/<int:pk>/', ArtikelRetrieveUpdateDestroyAPIView.as_view(), name='api_artikel_detail'),

    # API Komentar
    path('comments/', CommentListCreateAPIView.as_view(), name='api_comment_list_create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='api_comment_detail'),
    # =====================================================================
]