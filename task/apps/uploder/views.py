from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import ImageFileMetadata,FileMetadataFactory,DocumentFileMetadata
from .serializers import ImageFileMetadataSerializer,DocumentFileMetadataSerializer
from rest_framework.decorators import action
from django.http import FileResponse
import os
from django.core.exceptions import ValidationError



class ImageFileMetadataView(viewsets.ModelViewSet):
    serializer_class = ImageFileMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return ImageFileMetadata.objects.filter(user=self.request.user)
    

    def perform_create(self, serializer):
        file = self.request.data.get('upload_file')
        user = self.request.user
        extension = os.path.splitext(file.name)[1].lower()
        if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
            return Response({'message':'The file format is not acceptable'},status=status.HTTP_400_BAD_REQUEST)
        
        
        if file.size > 5 * 1024 * 1024: 
            return Response({'message':'File size should not exceed 5 MB'},status=status.HTTP_400_BAD_REQUEST)
        
        metadata_type = 'image'
        try:
            metadata = FileMetadataFactory.create_metadata(user, file, metadata_type)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=user, upload_file=metadata.upload_file, width=metadata.width, height=metadata.height)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.user == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        imagefile = self.get_object()
        if not imagefile.user == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        file_handle = imagefile.upload_file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename="%s"' % imagefile.upload_file.name
        return response


#--------------------------------------------------------------------------------------------

class DocumentFileMetadataView(viewsets.ModelViewSet):
    serializer_class = DocumentFileMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DocumentFileMetadata.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        file = self.request.data.get('upload_file')
        user = self.request.user
        extension = os.path.splitext(file.name)[1].lower()
        if extension not in ['.pdf']:
            return Response({'message':'The file format is not acceptable'},status=status.HTTP_400_BAD_REQUEST)
        
        if file.size > 5 * 1024 * 1024:  
            return Response({'message':'File size should not exceed 5 MB'},status=status.HTTP_400_BAD_REQUEST)
        
        metadata_type = 'document'
        try:
            metadata = FileMetadataFactory.create_metadata(user, file, metadata_type)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=user, upload_file=metadata.upload_file, page_count=metadata.page_count)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.user == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        documentfile = self.get_object()
        if not documentfile.user == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        file_handle = documentfile.upload_file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename="%s"' % documentfile.upload_file.name
        return response



