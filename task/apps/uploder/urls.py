from django.urls import path
from .views import ImageFileMetadataView, DocumentFileMetadataView

app_name='uploder'
urlpatterns = [
    path('images/', ImageFileMetadataView.as_view({'get': 'list', 'post': 'create'}), name='image-list-create'),
    path('images/<int:pk>/', ImageFileMetadataView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='image-detail'),
    path('images/<int:pk>/download/', ImageFileMetadataView.as_view({'get': 'download'}), name='image-download'),
    
    path('documents/', DocumentFileMetadataView.as_view({'get': 'list', 'post': 'create'}), name='document-list-create'),
    path('documents/<int:pk>/', DocumentFileMetadataView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='document-detail'),
    path('documents/<int:pk>/download/', DocumentFileMetadataView.as_view({'get': 'download'}), name='document-download'),
]
