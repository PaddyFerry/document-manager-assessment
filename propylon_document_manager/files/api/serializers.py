import hashlib
import uuid

from rest_framework import serializers

from propylon_document_manager.files.models import File
from propylon_document_manager.users.api.serializers import UserSerializer
from propylon_document_manager.users.models import User


class FileSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(read_only=True)
    version_number = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    owner = UserSerializer(read_only=True)
    file = serializers.FileField(allow_empty_file=False, use_url=False, write_only=True)
    location = serializers.CharField(default="/")  # todo add regex validation for folder paths
    content_md5 = serializers.CharField(read_only=True)
    extension = serializers.CharField(read_only=True)

    def validate(self, data):
        if not self._health_check_file(data["file"]):
            raise serializers.ValidationError({"file": "File not allowed"})

        data["file_name"], data["extension"] = self._get_name_and_extension(data["file"].name)
        data["version_number"] = self._get_file_version(data["location"], data["file_name"], data["extension"])
        data["owner"] = User.objects.get(email=self.context["request"].user.email)
        data["content_md5"] = self._get_md5_hash(data["file"])
        data["file"].name = str(uuid.uuid4())

        return data

    class Meta:
        model = File
        fields = "__all__"

    @staticmethod
    def _get_file_version(location, file_name, extension):
        previous_version = (
            File.objects.all()
            .filter(location=location, file_name=file_name, extension=extension)
            .order_by("-version_number")
            .first()
        )
        file_version = previous_version.version_number + 1 if previous_version else 1
        return file_version

    @staticmethod
    def _get_md5_hash(file):
        return hashlib.file_digest(file.file, "md5").hexdigest()

    @staticmethod
    def _health_check_file(file):
        # Some sort of healthcheck done here
        if file.name is None or file.name == "":
            return False
        return True

    @staticmethod
    def _get_name_and_extension(name):
        split = name.split(".")
        # If no file extension
        if len(split) == 1:
            return name, ""
        return ".".join(split[:-1]), split[-1]
