from rest_framework import serializers
from .models import ImageFileMetadata, DocumentFileMetadata


# class ImageFileMetadataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageFileMetadata
#         fields = ['id', 'upload_file', 'width', 'height']

#     def to_representation(self, instance):      
#         representation = super().to_representation(instance)
#         representation['user'] = instance.user.email  
#         return representation


class ImageFileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFileMetadata
        fields = ['id', 'upload_file', 'width', 'height']

    def to_representation(self, instance):
        representation = super().to_representation(instance)        
        if isinstance(instance, self.Meta.model):
            representation['user'] = instance.user.email
        return representation



class DocumentFileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFileMetadata
        fields = ['id', 'upload_file']

    def to_representation(self, instance):      
        representation = super().to_representation(instance)
        if isinstance(instance, self.Meta.model):
            representation['user'] = instance.user.email 
        return representation



