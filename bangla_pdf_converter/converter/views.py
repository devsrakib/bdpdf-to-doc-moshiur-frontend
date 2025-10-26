
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
from .models import PDFConversion
from .serializers import PDFConversionSerializer, ConversionStatusSerializer
from .services import PDFProcessingService
import threading


class PDFConversionViewSet(viewsets.ModelViewSet):
    queryset = PDFConversion.objects.all()
    serializer_class = PDFConversionSerializer
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return ConversionStatusSerializer
        return PDFConversionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        conversion = serializer.save()
        
        processing_service = PDFProcessingService()
        thread = threading.Thread(
            target=processing_service.process_pdf,
            args=(conversion,)
        )
        thread.daemon = True
        thread.start()
        
        return Response(
            ConversionStatusSerializer(conversion).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        """Download converted file"""
        conversion = self.get_object()
        
        if conversion.status != 'completed':
            return Response(
                {'error': f'Conversion not completed yet. Status: {conversion.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        format_type = request.query_params.get('format', 'docx')
        
        if format_type == 'docx':
            if not conversion.docx_file:
                return Response(
                    {'error': 'DOCX file not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            file_field = conversion.docx_file
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif format_type == 'txt':
            if not conversion.txt_file:
                return Response(
                    {'error': 'TXT file not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            file_field = conversion.txt_file
            content_type = 'text/plain'
        else:
            return Response(
                {'error': 'Invalid format. Use "docx" or "txt"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            response = FileResponse(
                file_field.open('rb'),
                content_type=content_type
            )
            filename = file_field.name.split('/')[-1]
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
