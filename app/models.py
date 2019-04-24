from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # ��ӵ�Roleģ���е�users���Դ��������ϵ����������ӽǡ�����һ��
    # Role���ʵ������users���Խ��������ɫ��������û���ɵ��б�
    # db.relationship()�ĵ�һ���������������ϵ����һ�����ĸ�ģ�͡����ģ������δ���壬��ʹ���ַ�����ʽָ����

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
