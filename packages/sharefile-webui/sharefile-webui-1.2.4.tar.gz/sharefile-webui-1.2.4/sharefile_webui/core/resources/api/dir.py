import os
from flask_restful import Resource, reqparse
from requests.utils import unquote
from ..web import app_auth
from ...config import Config


class Dir(Resource):
    def __init__(self):
        self.root_path = Config.SHARE_DIRECTORY
        parser = reqparse.RequestParser()
        parser.add_argument('rename', type=str, help='New filename for directory rename')
        self.args = parser.parse_args()

    @app_auth.login_required
    def get(self, path: str) -> dict:
        """
        List of directory files and subdirectories
        :param path: Direcotory to be listed
        """
        path = unquote(path)
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
                "path": os.path.sep.join(path.split(os.path.sep)[:-1]),
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
                    "token": Config.FILE_TOKENS.data.get(context_item_path, None)
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
    def delete(self, path: str) -> dict:
        path = unquote(path)
        full_path = os.path.join(self.root_path, path)
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

    @app_auth.login_required
    def post(self, path: str) -> dict:
        """
        Create new directory. If exists it will add number suffix
        :param path: New directory path
        """
        path = unquote(path)
        full_path: str = os.path.join(self.root_path, path)
        dir_tail: str = ""
        tail_counter: int = 1
        while os.path.exists(full_path_tail := f"{full_path}{dir_tail}"):
            dir_tail = f" {tail_counter}"
            tail_counter += 1
        os.mkdir(full_path_tail)
        return {
            "status": True,
            "dir": full_path_tail
        }

    @app_auth.login_required
    def put(self, path: str) -> dict:
        """
        Rename existing directory. New name comes in `rename` GET param
        :param path: Path to existing directory
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
                if Config.FILE_TOKENS.remove_file_tokes_beginig(path):
                    Config.FILE_TOKENS.save_json()
            except Exception as ex:
                return {
                    "status": False,
                    "message": f"Dir.update: {ex}"
                }
        return {
            "status": True,
            "dir": full_path_rename
        }


class DirRoot(Dir):
    @app_auth.login_required
    def get(self) -> dict:
        return super().get("")
