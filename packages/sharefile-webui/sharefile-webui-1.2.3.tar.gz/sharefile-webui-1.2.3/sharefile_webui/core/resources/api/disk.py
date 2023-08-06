import shutil
from flask_restful import Resource
from ..web import app_auth
from ...config import Config


class Disk(Resource):
    @app_auth.login_required
    def get(self):
        usage = shutil.disk_usage(Config.SHARE_DIRECTORY)
        return {
            "status": True,
            "diskUsage": {
                "total": usage.total,
                "free": usage.free,
                "used": usage.used,
            }
        }
