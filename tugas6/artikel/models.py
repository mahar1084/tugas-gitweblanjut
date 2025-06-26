from django.db import models
from django.contrib.auth.models import User

from django_ckeditor_5.fields import CKEditor5Field


class Kategori(models.Model):
    nama = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "1. Kategori"

class Artikel(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)
    konten = CKEditor5Field('Text', config_name='extends')
    gambar = models.ImageField(upload_to="artikel", blank=True, null=True)
    status = models.BooleanField(default=False) # Jika True, maka nanti akan muncul ditampilkan

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "2. Artikel"

# Model baru untuk Komentar
class Comment(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE, related_name='comments') # Komen pada artikel mana
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Siapa yang berkomentar
    # UBAH NAMA FIELD DARI 'text' MENJADI 'content'
    content = models.TextField() # Isi komentar
    created_at = models.DateTimeField(auto_now_add=True) # Waktu komentar dibuat
    is_approved = models.BooleanField(default=True) # Untuk moderasi komentar (opsional, default langsung disetujui)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.artikel.judul[:30]}...'

    class Meta:
        verbose_name_plural = "3. Komentar"
        ordering = ['created_at'] # Mengurutkan komentar berdasarkan waktu pembuatan