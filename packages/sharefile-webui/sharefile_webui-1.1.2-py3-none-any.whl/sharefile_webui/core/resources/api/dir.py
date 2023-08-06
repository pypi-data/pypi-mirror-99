import os
from flask_restful import Resource
from ..web import app_auth
from ...config import Config


class Dir(Resource):
    def __init__(self):
        self.root_path = Config.SHARE_DIRECTORY

    @app_auth.login_required
    def get(self, path: str):
        result_list_files = []
        result_list_dirs = []
        dir_path = os.path.join(self.root_path, path)
        dir_list: list = os.listdir(dir_path)
        dir_list.sort()

        if path:
            result_list_dirs.append({
                "type": "dir",
                "name": "/",
                "path": "",
            })
            result_list_dirs.append({
                "type": "dir",
                "name": "..",
                "path": "/".join(path.split(os.path.sep)[:-1]),
            })
        for dir_item in dir_list:
            full_path = os.path.join(dir_path, dir_item)
            context_item_path = os.path.join(path, dir_item)
            if os.path.isfile(full_path):
                result_list_files.append({
                    "type": "file",
                    "name": dir_item,
                    "path": context_item_path,
                    "size": os.path.getsize(full_path),
                    "token": Config.FILES.data.get(context_item_path, None)
                })
            elif os.path.isdir(full_path):
                result_list_dirs.append({
                    "type": "dir",
                    "name": dir_item,
                    "path": context_item_path,
                })
        return {
            "status": True,
            "context": path,
            "result": result_list_dirs + result_list_files
        }

    @app_auth.login_required
    def delete(self, path: str):
        full_path = os.path.join(Config.SHARE_DIRECTORY, path)
        try:
            os.rmdir(full_path)
        except Exception as ex:
            return {
                "status": False,
                "message": f"Dir.delete: {ex}"
            }
        return {
            "status": True
        }


class DirRoot(Dir):
    @app_auth.login_required
    def get(self):
        return super().get("")
