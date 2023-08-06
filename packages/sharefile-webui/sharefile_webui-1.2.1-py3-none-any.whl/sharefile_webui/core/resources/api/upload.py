import os
from flask_restful import Resource, request
from requests.utils import unquote
from ..web import app_auth
from ...config import Config


class Upload(Resource):
    @app_auth.login_required
    def post(self, path: str):
        path = unquote(path)
        uploaded = []
        files = request.files
        for file_item in files.items():
            _, file_storage = file_item
            filename = file_storage.filename
            file_storage.save(os.path.join(Config.SHARE_DIRECTORY, path, filename))
            uploaded.append(filename)
        return {
            "status": True,
            "filename": uploaded,
        }


class UploadRoot(Upload):
    @app_auth.login_required
    def post(self):
        return super().post("")
