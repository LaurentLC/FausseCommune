import os.path
import uuid
import zipfile

from google.cloud import storage


class StorageClient:
    project_name = "fausse-commune"
    default_bucket_name = "fausses_communes_bucket"

    _client = None
    _default_bucket = None

    @classmethod
    def get_client(cls) -> storage.Client:
        if cls._client is None:
            cls._client = storage.Client(project=cls.project_name)
        return cls._client

    @classmethod
    def get_default_bucket(cls) -> storage.Bucket:
        client = cls.get_client()
        return client.bucket(cls.default_bucket_name)

    @classmethod
    def upload_file(cls, gs_path: str, local_path: str,
                    content_type: str = None, make_public: bool = False) -> None:
        """
        If content_type is None, it will be guessed from the file extension.
        """
        bucket = cls.get_default_bucket()
        blob = bucket.blob(cls.clean_path(gs_path))
        blob.upload_from_filename(local_path, content_type=content_type, timeout=300)
        if make_public:
            blob.make_public()

    @classmethod
    def zip_and_upload_to_storage(cls, filepaths: list[str], gs_path: str,
                                  make_public: bool):
        """
        Return storage path of zip.
        """
        zip_filename = f"{uuid.uuid4()}.zip"
        zip_filepath = os.path.join(os.getcwd(), zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath in filepaths:
                zipf.write(filepath, arcname=os.path.basename(filepath))

        # Upload the zip file to storage
        cls.upload_file(cls.clean_path(gs_path), zip_filepath, content_type="application/zip", make_public=make_public)

        # Clean up the local zip file
        os.remove(zip_filepath)

    @classmethod
    def download_string_file(cls, gs_path: str) -> str:
        """Downloads a blob into memory."""
        bucket = cls.get_default_bucket()
        blob = bucket.blob(cls.clean_path(gs_path))
        return blob.download_as_text()

    @classmethod
    def clean_path(cls, path: str):
        """
        Return any gs path cleaned from prefixes.
        """
        if path.startswith('/'):
            path = path[1:]
        elif path.startswith('gs://'):
            path = path[5:]
        if path.startswith(f"{cls.default_bucket_name}/"):
            path = path[len(f"{cls.default_bucket_name}/"):]
        return path
