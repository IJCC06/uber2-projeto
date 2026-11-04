from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

admins = Blueprint(
    "admins",
    __name__,
    url_prefix="/admin"
)


@admins.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "admin":
        abort(403)

    return render_template("admins/home_admin.html")
