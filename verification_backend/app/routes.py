import os
import time
from json import dumps
from flask import send_from_directory, current_app, request, render_template, Blueprint, g
from .logging import get_logger

HTTP_METHODS = ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]

bp = Blueprint("main", __name__)

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
            os.path.join(bp.root_path, 'static'),
           'favicon.ico',
           mimetype='image/vnd.microsoft.icon')


@bp.route("/", defaults={"path": ""}, methods=HTTP_METHODS)
@bp.route("/<path:path>", methods=HTTP_METHODS)
def all_get_requests(path):
    data = {}
    id = current_app.config["SECRET_UUID_ID"]
    value = current_app.config["SECRET_UUID_VALUE"]
    data["url"] = request.base_url
    data["method"] = request.method
    data["iframe"] = id in request.args
    data["args"] = dumps(request.args)
    data["form"] = dumps(request.form)
    data["json"] = dumps(request.get_json(silent=True, force=True) or "")
    data["cookies"] = dumps(request.cookies)
    data["headers"] = dumps(dict(request.headers))
    data["time"] = time.time()
    g.data = data
    return render_template(
            "success.html",
            id=id,
            value=value,
            url=data["url"],
            method=data["method"],
            iframe=data["iframe"],
            args=data["args"],
            form=data["form"],
            json=data["json"],
            cookies=data["cookies"],
            headers=data["headers"],
            time=data["time"])

@bp.after_request
def log_request(response):
    if "data" in g:
        data = g.pop("data", None)
        if not (data["method"] == "HEAD" and "python-requests" in data["headers"]):
            logger = get_logger("backend")
            logger.info(dumps(data))
    return allow_cors(response)

def allow_cors(response):
    response.headers["Access-Control-Allow-Origin"] =  "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response
