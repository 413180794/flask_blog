from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1.64), Email()])
    password = PasswordField("Password", validators={DataRequired()})
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[Length(1, 64), DataRequired(), Email()])
    username = StringField("Username",
                           validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo("password2", message="密码必须要相同")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField(u"注册")

    # 注意这里对邮箱校验，对密码校验，对用户名校验是为了防止用户直接通过request登录
    # 前端需要在校验一次
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已经被注册。")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在。")
