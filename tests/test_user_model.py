from unittest import TestCase

from app.models import User


class UserModelTestCase(TestCase):
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
