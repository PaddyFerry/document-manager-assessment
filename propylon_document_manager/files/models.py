import hashlib
from datetime import datetime

from django.db import models

from propylon_document_manager.users.models import User


class File(models.Model):
    content_md5 = models.CharField(db_index=True, max_length=32, default=hashlib.md5)
    file_name = models.fields.CharField(max_length=512)
    version_number = models.fields.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.utcnow)
    location = models.CharField(max_length=1024, default="/")
    file = models.FileField(upload_to="storage/", null=True, blank=True)
    extension = models.CharField(max_length=512, default="")

    @property
    def original_name(self):
        split = self.file.file.name.split("/")
        split[-1] = self.file_name + "." + self.extension
        return "/".join(split)

    @property
    def versions(self):
        all_versions = File.objects.filter(location=self.location, file_name=self.file_name, extension=self.extension)
        return all_versions
