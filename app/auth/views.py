import re

from flask import render_template, redirect, request, url_for, flash, json
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from .forms import LoginForm, RegistrationForm
from . import auth
from ..models import User
from ..email import send_email


@auth.before_app_request
def before_request():
    # 如果用户已经登录且没有确认且访问非认证路由与非静态资源，则强制用户去认证
    print("request.endpoint",request.endpoint)
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    # 如果该用户是匿名的或者已经被确认
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


# 对于蓝本来说，before_request钩子只能应用到属于蓝本的请求上。若想在蓝本中使用针对程序全局请求的钩子，必须使用before_app_request修饰器
# 如果before_request或before_app_request的回调返回响应或重定向，Flask会直接将其发送至客户端，而不会调用请求的视图函数。因此，这些回调
# 可在必要时拦截请求

@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "Confirm Yout Account", "auth/email/confirm", user=current_user, token=token)
    flash("A new confirmation email has been sent to you by email")
    return redirect(url_for("main.index"))


@auth.route("/login", methods=['GET', "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password")
    return render_template('auth/login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()  # 先添加到数据库中，之后使用令牌校验，让confirmed为True，问题，如果用户一直不确认怎么办？
        token = user.generate_confirmation_token()
        print("token",token)
        send_email(user.email, "Comfirm Your Account", "auth/email/confirm", user=user, token=token)
        flash("一封确认邮件将会放松到您的邮箱")
        return redirect(url_for('main.index'))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    print("jiaoyan",token)
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    print(current_user.confirm(token))
    if current_user.confirm(token):
        flash("账号已经通过确认！")
    else:
        flash("该链接已经失效！")
    return redirect(url_for("main.index"))

# @auth.route("/api/register", methods=['POST'])
# def apiRegister():
#     # 利用ajax通信，有点繁琐
#     print(request.form)
#     print(request.get_data())
#     print(request.data)
#     formData = request.form  # 拿到前端传过来的表格数据，如果是通过这种方法拿到的数据，那么就需要自己在检验一次用户名是否符合要求，等等
#     username = formData['username']
#     password1 = formData['password']
#     password2 = formData['password2']
#     email = formData['email']
#     # usernameMatch = re.compile(r"/^[a-zA-Z\d]\w{5,15}[a-zA-Z\d]$/")
#     passwordMatch = re.compile(r"^[a-zA-Z]\w{6,18}")
#     # if not usernameMatch.match(username):
#     #     return json.dumps({"error": "用户名不符合要求", "id": "username"})
#     if User.query.filter_by(username=username).first():
#         return json.dumps({"error": "该用户已注册", "id": "username"})
#     if User.query.filter_by(email=email).first():
#         return json.dumps({"error": "该邮箱已经注册", "id": "email"})
#     if password1 != password2:
#         return json.dumps({"error": "两次输入密码不同", "id": "password1"})
#     if not passwordMatch.match(password1):
#         return json.dumps({"error": "密码不符合规范", "id": "password"})
#     user = User(email=email,username=username,password=password1)
#     db.session.add(user)
#     return json.dumps({"success": 1})
