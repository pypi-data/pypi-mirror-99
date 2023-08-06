from flask_restful import Resource
from ..web import app_auth
from ...config import Config


class FileToken(Resource):
    @app_auth.login_required
    def post(self, path: str):
        token = Config.FILE_TOKENS.add_file_token(path)
        Config.FILE_TOKENS.save_json()
        return {
            "status": True,
            "token": token
        }

    @app_auth.login_required
    def delete(self, path: str):
        Config.FILE_TOKENS.remove_file_token(path)
        Config.FILE_TOKENS.save_json()
        return {
            "status": True
        }
