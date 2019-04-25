from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 添加到Role模型中的users属性代表这个关系的面向对象视角。对于一个
    # Role类的实例，其users属性将返回与角色相关联的用户组成的列表。
    # db.relationship()的第一个参数表明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("Role", backref=db.backref("users", lazy='dynamic'))

    @property
    def password(self):
        # 默认不可以获得密码的铭文
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username
