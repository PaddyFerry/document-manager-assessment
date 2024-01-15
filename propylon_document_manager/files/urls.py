from django.urls import path

from propylon_document_manager.files.api.views import file_list_view

app_name = "files"

urlpatterns = [
    path("", view=file_list_view, name="file_list"),
]
