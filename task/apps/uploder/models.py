from django.db import models
from apps.accounting.models import CustomUser
from PIL import Image
from utils import FileUpload
# from . import fileStorage


#در صورت وصل بود گوگل کلود برای ذخیره سازی فایل ها میتونیم این کلاس رو وصل کنیم و ماگریشن و ماگرت رو انجام بدیم
# class BaseFileMetadata(models.Model):
#     """
#     کلاس پایه برای متادیتا فایل‌ها
#     """
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     dir_upload=FileUpload('uploads','dir_upload')
#     upload_file = models.FileField(upload_to=dir_upload.upload_to, storage=fileStorage()) 

#     class Meta:
#         abstract = True
        



class BaseFileMetadata(models.Model):
    """
    کلاس پایه برای متادیتا فایل‌ها
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dir_upload=FileUpload('uploads','dir_upload')
    upload_file = models.FileField(upload_to=dir_upload.upload_to)  

    class Meta:
        abstract = True
        
        

class ImageFileMetadata(BaseFileMetadata):
    """
    کلاس متادیتای تصویر
    """
    width = models.PositiveIntegerField(null=True,blank=True)
    height = models.PositiveIntegerField(null=True,blank=True)

class DocumentFileMetadata(BaseFileMetadata):
    """
    کلاس متادیتای سند
    """
    page_count = models.PositiveIntegerField(null=True,blank=True)


#-----------------------------------

# Factory Method
class FileMetadataFactory:
    @staticmethod
    def create_metadata(user, file, metadata_type):
        """
        ایجاد متادیتا بر اساس نوع فایل
        """
        if metadata_type == 'image':
            image = Image.open(file)
            width, height = image.size
            return ImageFileMetadata(user=user, upload_file=file, width=width, height=height)
        elif metadata_type == 'document':
            # استخراج تعداد صفحات از فایل
            return DocumentFileMetadata(user=user, upload_file=file, page_count=0)
        else:
            raise ValueError("The metadata type is not valid.")








