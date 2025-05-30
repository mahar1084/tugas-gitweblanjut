from django.db import models
from django.contrib.auth.models import User

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
    konten = models.TextField(blank=True, null=True)
    gambar = models.ImageField(upload_to="artikel", blank=True, null=True)
    status = models.BooleanField(default=False)  # jika True, maka nanti akan muncul ditampilan depan

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.judul
    
    class Meta:
        verbose_name_plural = "2. Artikel Blog"



