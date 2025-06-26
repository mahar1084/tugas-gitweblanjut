# artikel/models.py

from django.db import models
from django.contrib.auth.models import User

from django_ckeditor_5.fields import CKEditor5Field

# ==============================================================
# Import yang diperlukan dari django-imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
# ==============================================================

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
    status = models.BooleanField(default=False)

    # ==============================================================
    # Tambahkan ImageSpecField untuk thumbnail
    # ==============================================================
    thumbnail = ImageSpecField(source='gambar', # Sumber gambar adalah field 'gambar' Anda
                               processors=[ResizeToFill(300, 200)], # Contoh: resize ke 300x200 pixel
                               format='JPEG', # Format output
                               options={'quality': 80}) # Kualitas JPEG

    # Anda bisa membuat spec lain jika perlu, misalnya gambar berukuran sedang untuk tampilan detail
    gambar_sedang = ImageSpecField(source='gambar',
                                   processors=[ResizeToFill(600, 400)],
                                   format='JPEG',
                                   options={'quality': 90})
    # ==============================================================

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "2. Artikel"

# Model baru untuk Komentar
class Comment(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.artikel.judul[:30]}...'

    class Meta:
        verbose_name_plural = "3. Komentar"
        ordering = ['created_at']