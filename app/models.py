from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 添加到Role模型中的users属性代表这个关系的面向对象视角。对于一个
    # Role类的实例，其users属性将返回与角色相关联的用户组成的列表。
    # db.relationship()的第一个参数表明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("Role", backref=db.backref("users", lazy='dynamic'))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User %r>" % self.username
