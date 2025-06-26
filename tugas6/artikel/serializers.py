# tugas6/artikel/serializers.py
from rest_framework import serializers
from .models import Kategori, Artikel, Comment

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class ArtikelSerializer(serializers.ModelSerializer):
    kategori = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Artikel
        fields = '__all__'

# Serializer baru untuk Komentar
class CommentSerializer(serializers.ModelSerializer):
    # HAPUS BARIS INI: artikel = serializers.StringRelatedField()
    # Biarkan ModelSerializer menanganinya secara otomatis sebagai PrimaryKeyRelatedField

    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        # Pastikan 'content' adalah nama field yang benar dari model Comment Anda.
        # Dan sertakan 'user_username' untuk dikembalikan ke front-end
        # Pastikan 'artikel' ada di 'fields' agar bisa ditulis
        fields = ['id', 'artikel', 'user', 'user_username', 'content', 'created_at', 'is_approved']
        
        # 'user' dan 'created_at' bersifat read-only.
        read_only_fields = ['created_at', 'user']