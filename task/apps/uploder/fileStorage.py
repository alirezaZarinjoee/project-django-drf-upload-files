# from django.core.files.storage import Storage, FileSystemStorage
# from storages.backends.gcloud import GoogleCloudStorage

# class FileStorage(Storage):
#     def __init__(self):
#         self.local_storage = FileSystemStorage()
#         self.cloud_storage = GoogleCloudStorage()

#     def _open(self, name, mode='rb'):
#         return self.local_storage._open(name, mode)

#     def _save(self, name, content):
#         self.cloud_storage._save(name, content)
#         return self.local_storage._save(name, content)

#     def url(self, name):
#         return self.cloud_storage.url(name)

#     def exists(self, name):
#         return self.local_storage.exists(name) or self.cloud_storage.exists(name)

#     def delete(self, name):
#         self.local_storage.delete(name)
#         self.cloud_storage.delete(name)
