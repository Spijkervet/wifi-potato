from flask import render_template, Blueprint
from flask_login import login_required, current_user
from .. import app_info
from .. import interface
from ..forms import InterfaceForm, APForm

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
@login_required
def index():
    data = {
        "data": [x for x in range(10)]
    }
    return render_template('index.html', app_info=app_info, user=current_user, data=data)


@index_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    interface_form = InterfaceForm()
    ap_form = APForm()
    return render_template('settings.html', app_info=app_info, user=current_user, interface_form=interface_form, ap_form=ap_form)

@index_bp.route('/logs', methods=['GET'])
@login_required
def logs():
    return render_template('logs.html', app_info=app_info, user=current_user)
