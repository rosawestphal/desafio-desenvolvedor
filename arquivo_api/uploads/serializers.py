from rest_framework import serializers
from .models import CarregarArquivo

class CarregarArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarregarArquivo
        fields = ['id', 'file', 'uploaded_at', 'file_name']