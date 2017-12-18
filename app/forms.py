from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import Required
from . import app_info

class LoginForm(FlaskForm):
    email = StringField("Name", validators=[Required()], render_kw={"type": "email", "placeholder": "Email"})
    password = StringField("Password", validators=[Required()], render_kw={"type": "password", "placeholder": "Password"})
    remember = BooleanField("Remember", render_kw={"class": "form-check-input"})
    submit = SubmitField("Login")


class InterfaceForm(FlaskForm):
    sniff_iface = SelectField("Sniff Interface", choices=[(x, x) for x in app_info.get_interfaces()])
    ap_iface = SelectField("AP Interface", choices=[(x, x) for x in app_info.get_interfaces()])
    submit = SubmitField("Set")

class APForm(FlaskForm):
    ssid = StringField("SSID", validators=[Required()], render_kw={"placeholder": (app_info.ssid if app_info.ssid else "-")})
    password = StringField("Password", validators=[Required()], render_kw={"type": "password", "placeholder": "Password"})
    channel = StringField("Channel", validators=[Required()], render_kw={"placeholder": app_info.channel})
    submit = SubmitField("Set")
