import os
from flask_restful import Resource, reqparse
from requests.utils import unquote
from ..web import app_auth
from ...config import Config


class File(Resource):
    def __init__(self):
        self.root_path = Config.SHARE_DIRECTORY
        parser = reqparse.RequestParser()
        parser.add_argument('rename', type=str, help='New filename for directory rename')
        self.args = parser.parse_args()

    @app_auth.login_required
    def delete(self, path: str):
        path = unquote(path)
        if Config.FILE_TOKENS.remove_file_token(path):
            Config.FILE_TOKENS.save_json()
        full_path = os.path.join(self.root_path, path)
        os.remove(full_path)
        return {
            "status": True
        }

    @app_auth.login_required
    def put(self, path: str) -> dict:
        """
        Rename existing file. New name comes in `rename` GET param
        :param path: Path to existing file
        """
        path = unquote(path)
        rename = self.args.get("rename")
        if rename:
            path__1 = os.path.sep.join(path.split(os.path.sep)[:-1])
            full_path = os.path.join(self.root_path, path)
            full_path_rename = os.path.join(self.root_path, path__1, rename)
            try:
                os.rename(full_path, full_path_rename)
                # delete all tokens under prevoius path name
                if Config.FILE_TOKENS.remove_file_token(path):
                    Config.FILE_TOKENS.save_json()
            except Exception as ex:
                return {
                    "status": False,
                    "message": f"File.update: {ex}"
                }
        return {
            "status": True,
            "file": full_path_rename
        }
