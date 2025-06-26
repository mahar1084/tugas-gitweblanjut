from rest_framework import serializers
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined'] # Contoh field yang ingin diekspos
        read_only_fields = ['username', 'email', 'is_staff', 'date_joined'] # Field yang hanya bisa dibaca, tidak bisa diubah lewat API ini