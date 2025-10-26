from rest_framework import serializers
from .models import PDFConversion

class PDFConversionSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)
    
    class Meta:
        model = PDFConversion
        fields = [
            'id', 
            'file',
            'original_filename',
            'status',
            'total_pages',
            'word_count',
            'error_message',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'original_filename',
            'status',
            'total_pages',
            'word_count',
            'error_message',
            'created_at',
            'updated_at'
        ]
    
    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed")
        
        if value.size > 52428800:
            raise serializers.ValidationError("File size must be less than 50MB")
        
        return value
    
    def create(self, validated_data):
        file = validated_data.pop('file')
        conversion = PDFConversion.objects.create(
            uploaded_file=file,
            original_filename=file.name,
            **validated_data
        )
        return conversion


class ConversionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFConversion
        fields = [
            'id',
            'original_filename',
            'status',
            'total_pages',
            'word_count',
            'error_message',
            'created_at'
        ]