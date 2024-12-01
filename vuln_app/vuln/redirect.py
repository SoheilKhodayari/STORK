import functools
import base64

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

bp = Blueprint('redirect', __name__, url_prefix='/')

DEFAULT_URL = "https://example.com"

@bp.route("/")
def index():
    form = RedirectForm()
    urls = {
        "backend": url_for("redirect.backend", _external=True, url=""),
        "html5": url_for("redirect.frontend", _external=True, url=""),
        "javascript": url_for("redirect.javascript", _external=True, url=""),
    }
    return render_template("redirect/index.html", form=form, urls=urls)

@bp.route("/redirect/backend")
def backend():
    url = request.args.get("url") 
    noenc = request.args.get("noenc")
    if not url:
        flash("No redirect URL specified", "warning")
        return redirect(url_for("redirect.index"))
    else:
        if not noenc:
            url = base64.b64decode(url).decode("utf-8");
        return redirect(url)

@bp.route("/redirect/frontend")
def frontend():
    url = request.args.get("url")
    noenc = request.args.get("noenc")
    if not url:
        flash("No redirect URL specified", "warning")
        return redirect(url_for("redirect.index"))
    else:
        if not noenc:
            url = base64.b64decode(url).decode("utf-8");
        return render_template("redirect/frontend.html", url=url)

@bp.route("/redirect/javascript")
def javascript():
    url = request.args.get("url")
    noenc = request.args.get("noenc")
    if not url:
        flash("No redirect URL specified", "warning")
        return redirect(url_for("redirect.index"))
    else:
        if not noenc:
            url = base64.b64decode(url).decode("utf-8");
        return render_template("redirect/javascript.html", url=url)

class RedirectForm(FlaskForm):
    url = StringField("URL", default=DEFAULT_URL)
    submit = SubmitField("Redirect")
