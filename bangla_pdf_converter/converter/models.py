from django.db import models
import uuid

class PDFConversion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploads/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    docx_file = models.FileField(upload_to='outputs/', null=True, blank=True)
    txt_file = models.FileField(upload_to='outputs/', null=True, blank=True)
    
    total_pages = models.IntegerField(null=True, blank=True)
    word_count = models.IntegerField(null=True, blank=True)
    
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'PDF Conversion'
        verbose_name_plural = 'PDF Conversions'
    
    def __str__(self):
        return f"{self.original_filename} - {self.status}"