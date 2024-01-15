import hashlib
import io

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from propylon_document_manager.files.models import File
from propylon_document_manager.users.tests.factories import FileFactory, UserFactory


class TestFileListView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        super().setUp()

    def test_token_authentication(self):
        self.client.force_authenticate()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {str(token)}")
        response = self.client.get("/api/files/")
        assert response.status_code == 200

    def test_not_authenticated1(self):
        self.client.force_authenticate()
        response = self.client.get("/api/files/")
        assert response.status_code == 401

    def test_create_file(self):
        file = io.BytesIO(b"some data")
        post_body = {"file": file, "location": "/test/"}
        response = self.client.post("/api/files/", data=post_body)
        md5 = hashlib.file_digest(file, "md5").hexdigest()

        assert response.status_code == 201
        assert File.objects.count() == 1
        uploaded_file = File.objects.first()
        assert uploaded_file.file_name == "file"
        assert uploaded_file.content_md5 == md5

    def test_create_file_with_type(self):
        file = io.BytesIO(b"some data")
        file.name = "test.pdf"
        post_body = {"file": file, "location": "/test/"}
        response = self.client.post("/api/files/", data=post_body)
        md5 = hashlib.file_digest(file, "md5").hexdigest()

        assert response.status_code == 201
        assert File.objects.count() == 1
        uploaded_file = File.objects.first()
        assert uploaded_file.file_name == "test"
        assert uploaded_file.extension == "pdf"
        assert uploaded_file.content_md5 == md5

    def test_create_file_version(self):
        file = io.BytesIO(b"some data")
        file.name = "test.pdf"
        post_body = {"file": file, "location": "/test/"}
        self.client.post("/api/files/", data=post_body)

        file = io.BytesIO(b"some data")
        file.name = "test.pdf"
        post_body = {"file": file, "location": "/test/"}

        response = self.client.post("/api/files/", data=post_body)
        print(response)
        uploaded_file_version_2 = File.objects.get(id=response.data["id"])
        assert response.status_code == 201
        assert uploaded_file_version_2.extension == "pdf"

    def test_user_cant_access_other_files(self):
        user1 = UserFactory()
        user2 = UserFactory()
        self.client.force_authenticate(user=user2)
        FileFactory(owner=user1, version_number=1)
        response = self.client.get("/api/files/")
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_file_versions(self):
        user1 = UserFactory()
        self.client.force_authenticate(user=user1)
        version_1 = FileFactory(owner=user1, version_number=1, location="/files/", file_name="test", extension="pdf")
        version_2 = FileFactory(owner=user1, version_number=2, location="/files/", file_name="test", extension="pdf")
        version_3 = FileFactory(owner=user1, version_number=3, location="/files/", file_name="test", extension="pdf")
        # Create one other file
        FileFactory(owner=user1, version_number=1, location="/files/", file_name="blahblah", extension="pdf")
        response = self.client.get(f"/api/files/{version_1.id}/versions/")

        assert response.status_code == 200
        assert len(response.json()) == 3
        ids = [x["id"] for x in response.json()]
        assert version_1.id in ids
        assert version_2.id in ids
        assert version_3.id in ids

    def test_compare_files_same(self):
        md5 = hashlib.md5("test".encode()).hexdigest()
        version_1 = FileFactory(owner=self.user, content_md5=md5, version_number=1, file_name="test", extension="pdf")
        version_2 = FileFactory(owner=self.user, content_md5=md5, version_number=2, file_name="test", extension="pdf")
        response = self.client.get(f"/api/files/{version_1.id}/compare/{version_2.version_number}/")
        assert response.status_code == 200
        assert not response.data["is_diff"]

    def test_compare_files_diff(self):
        md5 = hashlib.md5("test".encode()).hexdigest()
        md5_2 = hashlib.md5("test2".encode()).hexdigest()
        version_1 = FileFactory(owner=self.user, content_md5=md5, version_number=1, file_name="test", extension="pdf")
        version_2 = FileFactory(
            owner=self.user, content_md5=md5_2, version_number=2, file_name="test", extension="pdf"
        )
        response = self.client.get(f"/api/files/{version_1.id}/compare/{version_2.version_number}/")
        assert response.status_code == 200
        assert response.data["is_diff"]

    def test_compare_files_invalid_version(self):
        version_1 = FileFactory(
            owner=self.user, version_number=1, location="/files/", file_name="test", extension="pdf"
        )
        response = self.client.get(f"/api/files/{version_1.id}/compare/3/")

        assert response.status_code == 400
        assert response.data == {"message": "Not a valid version for comparison"}

    def test_search_by_location(self):
        file = FileFactory(owner=self.user, location="/test/")
        FileFactory(owner=self.user, location="/")
        response = self.client.get("/api/files/?location=%2Ftest%2f")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == file.id

    def test_search_by_content(self):
        md5 = hashlib.md5("test".encode()).hexdigest()
        file = FileFactory(owner=self.user, location="/test/", content_md5=md5)
        FileFactory(owner=self.user, location="/")
        response = self.client.get(f"/api/files/?content_md5={md5}")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == file.id

    def test_search_by_filename(self):
        file = FileFactory(owner=self.user, location="/test/", file_name="test1")
        FileFactory(owner=self.user, location="/")
        response = self.client.get("/api/files/?file_name=test1")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == file.id

    def test_search_by_extension(self):
        file = FileFactory(owner=self.user, location="/test/", extension="pdf")
        FileFactory(owner=self.user, location="/", extension="epub")
        response = self.client.get("/api/files/?extension=pdf")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == file.id
