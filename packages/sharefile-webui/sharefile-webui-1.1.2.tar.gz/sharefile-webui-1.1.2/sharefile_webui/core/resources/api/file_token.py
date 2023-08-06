from flask_restful import Resource
from ..web import app_auth
from ...config import Config


class FileToken(Resource):
    @app_auth.login_required
    def post(self, path: str):
        token = Config.FILES.add_file_token(path)
        Config.FILES.save_json()
        return {
            "status": True,
            "token": token
        }

    @app_auth.login_required
    def delete(self, path: str):
        Config.FILES.remove_file_token(path)
        Config.FILES.save_json()
        return {
            "status": True
        }
