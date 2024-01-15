import mimetypes
import urllib.parse

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from propylon_document_manager.files.models import File

from .serializers import FileSerializer


@extend_schema_view(
    list=extend_schema(
        description="Return all uploaded files belonging to the user. Filter by location"
                    ", file_name, extension, and/or content_md5.",
        parameters=[
          OpenApiParameter("location", OpenApiTypes.STR, OpenApiParameter.QUERY),
          OpenApiParameter("file_name", OpenApiTypes.STR, OpenApiParameter.QUERY),
          OpenApiParameter("extension", OpenApiTypes.STR, OpenApiParameter.QUERY),
          OpenApiParameter("content_md5", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ]
    ),
    create=extend_schema(description="Upload a new file to the user."),
    retrieve=extend_schema(description="Get information about a specific file."),
    download=extend_schema(description="Download file of given id.")
)
class FileViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet, CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer
    queryset = File.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        search_fields = ["content_md5", "file_name", "extension", "location"]

        filter_by = {
            query: self.request.query_params.get(query)
            for query in search_fields
            if self.request.query_params.get(query)
        }

        if location := filter_by.get("location"):
            filter_by["location"] = urllib.parse.unquote(location)

        queryset = File.objects.filter(**filter_by, owner=self.request.user)

        return self.serializer_class(queryset, many=True).data

    @action(methods=["get"], detail=True, name="download", permission_classes=[IsAuthenticated])
    def download(self, *args, **kwargs):
        queryset = File.objects.filter(owner=self.request.user)
        file = get_object_or_404(queryset, pk=kwargs["id"])
        open_file = open(file.file.path, "rb")
        response = FileResponse(
            open_file,
            filename=file.original_name,
            as_attachment=True,
            content_type=mimetypes.guess_type(file.original_name)[0],
        )
        return response

    @action(
        methods=["get"], detail=True, url_path="compare/(?P<file_version>[^/d]+)", permission_classes=[IsAuthenticated]
    )
    def compare_files(self, *args, **kwargs):
        """
        Compare two files to show if they have the same content or not
        """
        queryset = File.objects.filter(owner=self.request.user)
        file = get_object_or_404(queryset, pk=kwargs["id"])
        version_to_compare = kwargs.get("file_version")
        all_versions = file.versions.filter(owner=self.request.user)
        if int(version_to_compare) not in all_versions.values_list("version_number", flat=True):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Not a valid version for comparison"})

        file2 = all_versions.filter(version_number=version_to_compare).first()
        return Response(status=status.HTTP_200_OK, data={"is_diff": file.content_md5 != file2.content_md5})

    @action(methods=["get"], detail=True, url_path="versions", permission_classes=[IsAuthenticated])
    def get_file_versions(self, *args, **kwargs):
        queryset = File.objects.filter(owner=self.request.user)
        file = get_object_or_404(queryset, pk=kwargs["id"])
        all_versions = file.versions.filter(owner=self.request.user)
        return Response(self.serializer_class(all_versions, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        queryset = File.objects.filter(owner=self.request.user)
        file = get_object_or_404(queryset, pk=kwargs["id"])
        return Response(self.serializer_class(file).data)


file_list_view = FileViewSet.as_view({"get": "list"})
