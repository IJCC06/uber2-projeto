
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

usuarios = Blueprint("usuarios", __name__, url_prefix="/usuario")


@usuarios.route("/home", methods=["GET"])
@login_required
def home():
    if current_user.tipo != "usuario":
        abort(403)

    return render_template("usuarios/home_usuarios.html")
