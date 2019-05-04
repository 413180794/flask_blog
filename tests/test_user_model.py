import time
from unittest import TestCase

from app import db, create_app
from app.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    def test_password_setter(self):
        # 测试setter可用
        u = User()
        u.password = "cat"
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        # 测试getter不可用
        u = User()
        u.password = "cat"
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        # 测试密码验证功能可用
        u = User()
        u.password = 'cat'
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User()
        u.password = 'cat'
        u2 = User()
        u2.password = 'cat'
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        # 测试同一账号可以通过令牌
        u = User()
        u.password = "zhangfan"
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        # 测试不同的密码会生成不会的令牌
        u1 = User()
        u1.password = "cat"
        u2 = User()
        u2.password = "dog"
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        # 测试令牌过期时间
        u = User()
        u.password = "zhumengke"
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

