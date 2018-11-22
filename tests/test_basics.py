import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        ''' 创建一个测试环境，类似运行中的程序 '''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建一个临时数据库，以备不时之需
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])