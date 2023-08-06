import os
from flask import Flask, request, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from ..datafiles.file_tokens import FileTokens
from ..config import Config

templates_path = os.path.join(os.path.dirname(__file__), "../../templates/")
static_path = os.path.join(os.path.dirname(__file__), "../../static/")

app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
app_auth = HTTPBasicAuth()


@app_auth.verify_password
def verify_password(username, password):
    users = Config.USERS
    return users.check_user(username, password)


@app.route('/')
@app_auth.login_required
def index() -> Flask.response_class:
    data = {
        "version": Config.VERSION,
        "user": app_auth.current_user()
    }
    return render_template("index.html", data=data)


@app.route('/share/<path:path>')
def share(path) -> Flask.response_class:
    args = request.args
    token = args.get("token", None)
    file_tokens: FileTokens = Config.FILES
    if path not in file_tokens.data:
        return f"File '{path}' not found", 404
    if file_tokens.check_token(path, token):
        full_path = os.path.join(Config.SHARE_DIRECTORY, path)
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
    return f"Unauthorized access to file '{path}'", 401
