from flask import request, render_template, redirect, url_for, Blueprint

from blueprintapp.app import db

bp_core = Blueprint('bp_core',__name__,template_folder='templates')

@bp_core.route("/")
def index():
    return render_template('core/index.html')