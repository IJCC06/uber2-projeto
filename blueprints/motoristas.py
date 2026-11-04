from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

motoristas = Blueprint(
    "motoristas",
    __name__,
    url_prefix="/motorista"
)


@motoristas.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "motorista":
        abort(403)

    return render_template("motoristas/home_motorista.html")
