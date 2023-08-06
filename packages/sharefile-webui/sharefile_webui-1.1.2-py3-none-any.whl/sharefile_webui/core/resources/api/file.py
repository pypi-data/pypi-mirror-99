import os
from flask_restful import Resource
from ..web import app_auth
from ...config import Config


class File(Resource):
    @app_auth.login_required
    def delete(self, path: str):
        Config.FILES.remove_file_token(path)
        Config.FILES.save_json()
        full_path = os.path.join(Config.SHARE_DIRECTORY, path)
        os.remove(full_path)
        return {
            "status": True
        }
